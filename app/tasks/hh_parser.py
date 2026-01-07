import logging
from celery import Celery
from app.parsers.hh_ru import fetch_hh_vacancies
from app.core.clickhouse import get_clickhouse_client

logger = logging.getLogger(__name__)

# Настройка Celery
celery_app = Celery(
    'hh_parser',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

@celery_app.task(bind=True, max_retries=2)
def parse_hh_vacancies_task(self, page: int = 0):
    """
    Фоновая задача: парсит одну страницу и сохраняет в ClickHouse
    """
    try:
        logger.info(f"Начало парсинга страницы {page}")
        vacancies = fetch_hh_vacancies(page=page)   #список словарей с данными

        if not vacancies:
            logger.info(f"Страница {page} пуста — завершаем.")
            return {"page": page, "count": 0, "status": "empty"}

        # Очищаем каждую строку
        cleaned_vacancies = [sanitize_row(vac) for vac in vacancies]

        # Подготовка данных для вставки
        data = [
            (v['title'], v['company'], v['salary_raw'], v['work_format'], v['url'], page)
            for v in cleaned_vacancies
        ]

        client = get_clickhouse_client()
        client.insert(
            table='job_analytics.hh_vacancies',
            data=data,
            column_names=['title', 'company', 'salary_raw', 'work_format', 'url', 'page']
        )

        logger.info(f"Сохранено {len(vacancies)} вакансий со страницы {page}")
        return {"page": page, "count": len(vacancies), "status": "success"}

    except Exception as exc:
        logger.error(f"Ошибка на странице {page}: {exc}")
        raise self.retry(exc=exc, countdown=60)
    

def sanitize_row(row: dict) -> dict:
    """Заменяет все None на пустые строки в словаре."""
    return {key: (value if value is not None else "") for key, value in row.items()}