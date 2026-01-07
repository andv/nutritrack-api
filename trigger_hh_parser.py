# trigger_hh_parser.py
from app.tasks.hh_parser import parse_hh_vacancies_task

if __name__ == "__main__":
    # Ставим задачу в очередь — возвращаетAsyncResult, но не ждёт выполнения
    result = parse_hh_vacancies_task.delay(page=0, max_pages=5)
    print(f"Задача запущена: {result.id}")