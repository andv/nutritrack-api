import os
from clickhouse_connect import get_client
from typing import List, Dict

def get_clickhouse_client():
    return get_client(
        host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),  # ← имя сервиса
        port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", "mypass123"), #"mypass123"),
        database=os.getenv("CLICKHOUSE_DB", "job_analytics")
    )


def insert_vacancies(vacancies: List[Dict]):
    client = get_clickhouse_client()
    # Преобразуем в плоский формат для вставки
    data = [
        (
            v["title"],
            v["company"],
            v["salary_raw"],
            v["work_format"],
            v["url"],
            v["source"]
        )
        for v in vacancies
    ]
    client.insert(
        "job_analytics.hh_vacancies",
        data,
        column_names=["title", "company", "salary_raw", "work_format", "url", "source"]
    )