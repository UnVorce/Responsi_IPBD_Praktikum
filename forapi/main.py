from fastapi import FastAPI
import json
import os

app = FastAPI(title="Wired Scraper API")

@app.get("/articles")
def get_articles():
    file_path = os.path.join(os.path.dirname(__file__), '../data/scraped_data.json')
    
    if not os.path.exists(file_path):
        return {"error": "Loot tidak ditemukan. Jalankan scraper terlebih dahulu."}
        
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    return {"status": "success", "total_data": len(data), "data": data}