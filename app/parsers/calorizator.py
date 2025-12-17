import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def fetch_product_data(product_name: str) -> List[Dict]:
    #url = f"https://calorizator.ru/search/node/{product_name}"
    url = f"https://hh.ru/search/vacancy?professional_role=36&professional_role=125&professional_role=104&professional_role=157&professional_role=107&salary=450000&currency_code=RUR&work_format=REMOTE&search_period=1&items_on_page=100&L_save_area=true&hhtmFrom=vacancy_search_filter"
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
