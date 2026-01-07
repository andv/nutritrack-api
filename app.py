from clickhouse_connect import get_client  # или clickhouse-driver

def get_clickhouse_client():
    return get_client(
        host='localhost',
        port=8123,
        username='default',
        password='mypass123',
        database='job_analytics'
    )

client = get_clickhouse_client()
result = client.query("SELECT company, count() FROM job_analytics.hh_vacancies GROUP BY company ORDER BY count() DESC LIMIT 10")
print(result.result_rows)