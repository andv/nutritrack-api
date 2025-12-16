import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def fetch_product_data(product_name: str) -> List[Dict]:
    url = f"https://calorizator.ru/search/node/{product_name}"
    headers = {"User-Agent": "NutriTrack Bot 1.0"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Пример парсинга — адаптируйте под структуру сайта
    results = []
    for item in soup.select('.search-item'):
        name = item.select_one('h3 a').text.strip()
        kcal = item.select_one('.kcal').text.strip()
        results.append({"name": name, "kcal": kcal})
    return results