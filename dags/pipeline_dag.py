from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
import requests
import pandas as pd


default_args = {
    'owner': 'nexus',
    'start_date': datetime(2026, 4, 20),
    'retries': 1,
}

dag = DAG(
    'wired_data_pipeline',
    default_args=default_args,
    schedule='@daily',
    catchup=False
)

def fetch_and_clean_data(**kwargs):
    response = requests.get('http://host.docker.internal:8000/articles')
    raw_data = response.json()['data']
    
    df = pd.DataFrame(raw_data)
    df['scraped_at'] = pd.to_datetime(df['scraped_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    kwargs['ti'].xcom_push(key='cleaned_data', value=df.to_dict('records'))

def load_to_db(**kwargs):
    # 1. Pulling Data dari XCom
    data = kwargs['ti'].xcom_pull(key='cleaned_data', task_ids='extract_and_transform')
    pg_hook = PostgresHook(postgres_conn_id='wired_db_conn')
    
    # 2. Setup Schema (Pastikan Tabel Ada)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS wired_articles (
        id SERIAL PRIMARY KEY,
        title TEXT,
        url TEXT,
        description TEXT,
        author VARCHAR(255),
        scraped_at TIMESTAMP
    );
    """
    pg_hook.run(create_table_query) # <-- WAJIB: Pastikan tabel di-render dulu
    
    # 3. Wipe Out (Bersihkan Data Lama + Reset ID Counter)
    # Gunakan RESTART IDENTITY agar kolom 'id' balik lagi ke angka 1
    pg_hook.run("TRUNCATE TABLE wired_articles RESTART IDENTITY;")
    
    # 4. Mass Infiltration (Insert Data)
    insert_query = """
    INSERT INTO wired_articles (title, url, description, author, scraped_at)
    VALUES (%s, %s, %s, %s, %s)
    """
    for row in data:
        pg_hook.run(insert_query, parameters=(
            row['title'], 
            row['url'], 
            row['description'], 
            row['author'], 
            row['scraped_at']
        ))

task_extract = PythonOperator(
    task_id='extract_and_transform',
    python_callable=fetch_and_clean_data,
    dag=dag,
)

task_load = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_db,
    dag=dag,
)

task_extract >> task_load