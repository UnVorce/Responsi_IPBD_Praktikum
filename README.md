PROJECT WIRED

1. OVERVIEW
Sistem ETL modular untuk scraping Wired.com. Data diambil oleh scraper, disediakan melalui FastAPI, dan dikelola otomatis oleh Airflow ke PostgreSQL.

2. TECH STACK
- Python 3.13
- FastAPI & Uvicorn
- Apache Airflow 3.2.0 (Dockerized)
- PostgreSQL 16
- Docker Compose, BeautifulSoup4, Pandas, pgAdmin 4

3. DEPLOYMENT STEPS

A. API SETUP
Jalankan API di terminal lokal:
uvicorn main:app --reload
Endpoint: http://127.0.0.1:8000/articles

B. DOCKER DEPLOYMENT
Nyalakan armada kontainer di latar belakang:
docker-compose up -d

C. AIRFLOW EXECUTION
- Buka http://localhost:8080
- Credentials: airflow / airflow
- Aktifkan DAG 'wired_data_pipeline' (Unpause) dan klik Trigger.
- Pantau hingga semua node berwarna hijau (Success).

4. DATABASE QUERIES (PGADMIN)

A. CLEAN AUTHOR NAME (MENGHAPUS KATA "BY")
SELECT title, REGEXP_REPLACE(author, '^By\s+', '', 'i') AS author_clean 
FROM wired_articles;

B. TOP 3 MVP AUTHORS (PENULIS TERAKTIF)
SELECT author, COUNT(*) AS total 
FROM wired_articles 
GROUP BY author 
ORDER BY total DESC 
LIMIT 3;

C. KEYWORD SCOUTING (AI/CLIMATE/SECURITY)
SELECT * FROM wired_articles 
WHERE title ~* 'AI|Climate|Security' 
OR description ~* 'AI|Climate|Security';

5. TACTICAL NOTES
- TRUNCATE: Sistem menggunakan 'TRUNCATE TABLE ... RESTART IDENTITY' tiap eksekusi untuk mencegah duplikasi data dan mereset ID ke angka 1.
- DOCKER TUNNEL: Menggunakan 'host.docker.internal' untuk komunikasi kontainer ke host Windows.
- MODULAR DESIGN: Pemisahan scraper/API dari orchestrator untuk menjaga stabilitas penggunaan RAM dan CPU.
