from fastapi import FastAPI
#from app.parsers.calorizator import fetch_product_data
from app.parsers.hh_ru import fetch_all_hh_vacancies

app = FastAPI(title="NutriTrack API с hh.ru анализом")
"""
@app.get("/search")
async def search_product(q: str):
    try:
        results = fetch_product_data(q)
        return {"query": q, "results": results}
    except Exception as e:
        return {"error": str(e)}, 400
"""
@app.get("/hh-vacancies")
def get_hh_vacancies(pages: int = 1):
    """
    Парсит вакансии с hh.ru (осторожно: блокировка при частых запросах!)
    """
    try:
        data = fetch_all_hh_vacancies(max_pages=pages)
        return {"count": len(data), "vacancies": data}
    except Exception as e:
        return {"error": str(e)}, 500
