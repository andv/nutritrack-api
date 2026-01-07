# nutritrack-api

STATUS: WIP:
1. ok - python-приложение работает
2. ok - поиск работает
3. ok - docker-контейнеры работают
4. ok - clickhouse сохраняет данные

nutritrack-api/
├── app/                 # Исходный код приложения
│   ├── parsers/         # Модули парсинга
│   ├── api/             # FastAPI-эндпоинты
│   └── core/            # (пока пусто, позже — настройки, логика)
├── docker/app/          # Docker-файлы для Python-приложения
├── docker-compose.yml   # Оркестрация сервисов
├── requirements.txt     # Зависимости
└── README.md

 hh парсер — только для личного анализа рынка труда, не для коммерческого использования.

 архитектура:
 FastAPI (API) 
   │
   └──► Celery task ("parse_hh_vacancies") 
           │
           ├──► Парсинг hh.ru (requests + BeautifulSoup)
           └──► Сохранение в ClickHouse

## Установка зависимостей
```bash
source .venv/bin/activate
pip install -r requirements.txt

## заполнение БД
1. зайти в контейнер через VS code или через bash:
docker-compose exec clickhouse bash
clickhouse-client

2. создать таблицы:
CREATE DATABASE IF NOT EXISTS job_analytics;
CREATE TABLE job_analytics.hh_vacancies
(
    id UUID DEFAULT generateUUIDv4(),
    title String,
    company String,
    salary_raw Nullable(String),
    work_format String,
    url String,
    parsed_at DateTime DEFAULT now(),
    page UInt8
)
ENGINE = MergeTree
ORDER BY (parsed_at, company);


## Запуск для отладки
docker-compose up --build 
docker-compose exec nutritrack-api celery -A app.tasks.hh_parser worker --loglevel=info
http://localhost:8000/docs

#очистка контейнеров
docker-compose down -v

## проверка clickhouse
clickhouse-client

-- Посмотреть базы
SHOW DATABASES;
-- Переключиться на свою
USE job_analytics;
-- Посмотреть таблицы
SHOW TABLES;
-- Посмотреть данные
SELECT * FROM hh_vacancies LIMIT 10;
-- Посчитать общее число
SELECT count() FROM hh_vacancies;