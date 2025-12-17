import time
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HH_SEARCH_URL = (
    "https://hh.ru/search/vacancy"
    "?professional_role=36"
    "&professional_role=125"
    "&professional_role=104"
    "&professional_role=157"
    "&professional_role=107"
    "&salary=450000"
    "&currency_code=RUR"
    "&work_format=REMOTE"
    "&search_period=1"
    "&items_on_page=100"
    "&L_save_area=true"
    "&hhtmFrom=vacancy_search_filter"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
}

def extract_compensation(text: str) -> Optional[str]:
    """Очистка и нормализация зарплаты (оставляем как есть — для анализа позже)"""
    return text.strip() if text else None

def parse_vacancy(item) -> Optional[Dict]:
    try:
        title_tag = item.select_one('a[data-qa="serp-item__title"]')
        if not title_tag:
            return None

        title = title_tag.get_text(strip=True)
        link = title_tag['href']

        company_tag = item.select_one('[data-qa="vacancy-serp__vacancy-employer"]')
        company = company_tag.get_text(strip=True) if company_tag else "Не указана"

        salary_tag = item.select_one('[data-qa="vacancy-serp__vacancy-compensation"]')
        salary = extract_compensation(salary_tag.get_text()) if salary_tag else None

        work_format_tag = item.select_one('[data-qa="vacancy-serp__vacancy-work-format"]')
        work_format = work_format_tag.get_text(strip=True) if work_format_tag else ""

        return {
            "title": title,
            "company": company,
            "salary_raw": salary,
            "work_format": work_format,
            "url": link
        }
    except Exception as e:
        logger.warning(f"Ошибка при парсинге элемента: {e}")
        return None

def fetch_hh_vacancies(page: int = 0) -> List[Dict]:
    """
    Загружает одну страницу вакансий с hh.ru
    page=0 → первая страница, page=1 → вторая и т.д.
    """
    params = {}
    if page > 0:
        params['page'] = page

    logger.info(f"Запрос страницы {page}...")
    #resp = requests.get(HH_SEARCH_URL, headers=HEADERS, """params=params,""" timeout=10)
    resp = requests.get(HH_SEARCH_URL, headers=HEADERS, params='', timeout=10)
    logger.info(f"код ответа от страницы hh: {resp.status_code} и сам ответ: {resp}")

    # Проверить статус
    if resp.status_code == 200:
        resp.raise_for_status()
    else:
        logger.warning(f"Ошибка при запросе страницы: {resp.status_code}")


    soup = BeautifulSoup(resp.text, 'html.parser')
    #vacancy_items = soup.select('div.vacancy-serp-item__layout')
    vacancy_items = soup.select('div[data-qa="vacancy-serp__vacancy"]')

    results = []
    for item in vacancy_items:
        vacancy = parse_vacancy(item)
        if vacancy:
            results.append(vacancy)

    logger.info(f"Найдено {len(results)} вакансий на странице {page}")
    return results

def fetch_all_hh_vacancies(max_pages: int = 3) -> List[Dict]:
    """
    Загружает до max_pages страниц (по 100 вакансий)
    """
    all_vacancies = []
    for page in range(max_pages):
        try:
            vacancies = fetch_hh_vacancies(page)
            if not vacancies:
                logger.info("Больше вакансий нет. Остановка.")
                break
            all_vacancies.extend(vacancies)
            # ⏱️ Уважаем сервер — пауза между запросами
            time.sleep(2)
        except Exception as e:
            logger.error(f"Ошибка на странице {page}: {e}")
            break
    return all_vacancies
