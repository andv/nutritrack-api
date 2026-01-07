import os
from clickhouse_connect import get_client

def get_clickhouse_client():
    return get_client(
        host=os.getenv("CLICKHOUSE_HOST", "clickhouse"),  # ← имя сервиса
        port=int(os.getenv("CLICKHOUSE_PORT", "8123")),
        username=os.getenv("CLICKHOUSE_USER", "default"),
        password=os.getenv("CLICKHOUSE_PASSWORD", "mypass123"), #"mypass123"),
        database=os.getenv("CLICKHOUSE_DB", "job_analytics")
    )

""" версия без переменных окружения
import clickhouse_connect

def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host='clickhouse',
        port=8123,
        username='default',
        password='mypass123'
    )
"""