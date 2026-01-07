import asyncio
from fastapi import FastAPI
from app.parsers.hh_ru import HHParser
from app.core.clickhouse import insert_vacancies
from app.tasks.hh_parser import parse_hh_vacancies_task
#from app.parsers.calorizator import fetch_product_data
#from app.parsers.hh_ru import fetch_all_hh_vacancies


app = FastAPI(title="Job Analytics API")


""" это код для калоризатора
@app.get("/search")
async def search_product(q: str):
    try:
        results = fetch_product_data(q)
        return {"query": q, "results": results}
    except Exception as e:
        return {"error": str(e)}, 400
"""

""" # код для hh парсера версия 1
@app.get("/hh-vacancies")
def get_hh_vacancies(pages: int = 1):

#    Парсит вакансии с hh.ru (осторожно: блокировка при частых запросах!)

    try:
        data = fetch_all_hh_vacancies(max_pages=pages)
        return {"count": len(data), "vacancies": data}
    except Exception as e:
        return {"error": str(e)}, 500
"""


@app.post("/scan-hh")    # код hh-parser v.2
def trigger_hh_scan(max_pages: int = 3):
    # Запускает фоновое сканирование hh.ru (до max_pages)
    task_ids = []
    for page in range(max_pages):
        task = parse_hh_vacancies_task.delay(page=page)
        task_ids.append(task.id)
    return {"message": f"Запущено {max_pages} задач", "task_ids": task_ids}


async def main():   #асинхронный запуск hh-parser v.2.1
    async with HHParser(max_pages=2) as parser:
        vacancies = await parser.parse_all()
        print(f"Собрано: {len(vacancies)} вакансий")
        if vacancies:
            insert_vacancies(vacancies)
            print("Сохранено в ClickHouse")


if __name__ == "__main__":
    asyncio.run(main())