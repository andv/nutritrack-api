from fastapi import FastAPI
#from app.parsers.calorizator import fetch_product_data
#from app.parsers.hh_ru import fetch_all_hh_vacancies
from app.tasks.hh_parser import parse_hh_vacancies_task

app = FastAPI(title="Job Analytics API")

@app.post("/scan-hh")
def trigger_hh_scan(max_pages: int = 3):
    """
    Запускает фоновое сканирование hh.ru (до max_pages)
    """
    task_ids = []
    for page in range(max_pages):
        task = parse_hh_vacancies_task.delay(page=page)
        task_ids.append(task.id)
    return {"message": f"Запущено {max_pages} задач", "task_ids": task_ids}

""" это код для калоризатора
@app.get("/search")
async def search_product(q: str):
    try:
        results = fetch_product_data(q)
        return {"query": q, "results": results}
    except Exception as e:
        return {"error": str(e)}, 400
"""

"""
# код для hh парсера
@app.get("/hh-vacancies")
def get_hh_vacancies(pages: int = 1):
"""
#    #Парсит вакансии с hh.ru (осторожно: блокировка при частых запросах!)
"""
    try:
        data = fetch_all_hh_vacancies(max_pages=pages)
        return {"count": len(data), "vacancies": data}
    except Exception as e:
        return {"error": str(e)}, 500
"""