import json
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def breach_wired():
    print("Scrap ke Wired.com (Most Recent)...")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    options.add_argument('--log-level=3')
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    
    articles_data = []
    seen_urls = set()
    page = 1
    
    print("Pagination...")
    
    while len(articles_data) < 60 and page <= 5:
        print(f"Halaman {page}...")
        driver.get(f"https://www.wired.com/most-recent/?page={page}")
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='SummaryItemWrapper']"))
            )
        except:
            print(f"[!] Warning: Halaman {page} gagal memuat data atau sudah habis.")
            break

        cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='SummaryItemWrapper']")
        
        for card in cards:
            if len(articles_data) >= 60:
                break
                
            try:
                title_el = card.find_element(By.CSS_SELECTOR, "a[class*='SummaryItemHedLink']")
                title = title_el.text.strip()
                url = title_el.get_attribute('href')
                
                if not title or url in seen_urls:
                    continue
                
                try:
                    desc = card.find_element(By.CSS_SELECTOR, "div[class*='SummaryItemDek'], p[class*='SummaryItemDek']").text.strip()
                except:
                    desc = ""
                    
                try:
                    author = card.find_element(By.CSS_SELECTOR, "span[class*='BylineName'], [class*='BylinesWrapper']").text.strip()
                except:
                    author = "By Unknown"
                
                articles_data.append({
                    "title": title,
                    "url": url,
                    "description": desc,
                    "author": author,
                    "scraped_at": datetime.now().isoformat()
                })
                seen_urls.add(url)
                
            except:
                continue
        
        page += 1
        time.sleep(2)

    driver.quit()
    
    print(f"TOTAL LOOT: {len(articles_data)} artikel!")
    
    if len(articles_data) < 50:
        print(f"[!] ALERT: Data ({len(articles_data)}) masih di bawah target 50.")
    
    os.makedirs('data', exist_ok=True) 
    with open('data/scraped_data.json', 'w') as f: 
        json.dump(articles_data, f, indent=4)
        
    print("Data secured in data/scraped_data.json")

if __name__ == "__main__":
    breach_wired()