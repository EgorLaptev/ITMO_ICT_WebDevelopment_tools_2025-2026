# Лабораторная работа 3. Упаковка FastAPI приложения в Docker, Работа с источниками данных и Очереди.

**Студент:** Лаптев Егор, группа K3339  
**Репозиторий:** [GitHub](https://github.com/EgorLaptev/ITMO_ICT_WebDevelopment_tools_2025-2026)


**Цель работы** —  Научиться упаковывать FastAPI приложение в Docker, интегрировать парсер данных с базой данных и вызывать парсер через API и очередь.

## Задача 1: Упаковка FastAPI приложения, базы данных и парсера данных в Docker
Были подготовлены `Dockerfile` для основного FastAPI-приложения и отдельного сервиса парсера.
В `Dockerfile` описаны базовый Python-образ, установка зависимостей, копирование исходного кода в контейнер и команда запуска приложения.

Был создан `docker-compose.yml`, в котором описаны все необходимые сервисы: FastAPI-приложение, PostgreSQL, сервис парсера, Redis и Celery worker.

Docker Compose используется для одновременного запуска всех контейнеров и настройки их взаимодействия внутри одной Docker-сети.

```yaml
version: "3.9"

services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 123
      POSTGRES_DB: hackathon_db
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build:
      context: ./lr_1
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "8080:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:123@db:5432/hackathon_db
      DEBUG: "true"
      CREATE_TABLES_ON_STARTUP: "true"
      PARSER_SERVICE_URL: http://scraper:8000
    depends_on:
      db:
        condition: service_healthy
      scraper:
        condition: service_started

  scraper:
    build:
      context: ./lr_2/task_2
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      DATABASE_URL: postgresql://postgres:123@db:5432/hackathon_db
      DEBUG: "true"
    depends_on:
      db:
        condition: service_healthy

volumes:
  db_data:
```

## Задача 2: Вызов парсера из FastAPI
В основном FastAPI-приложении был добавлен endpoint, который принимает URL от клиента и отправляет HTTP-запрос в сервис парсера.

Клиент взаимодействует только с основным API, а логика парсинга выполняется в отдельном контейнере.

```python
@router.post("/queue")
async def enqueue_parser_task(request: ParseQueueRequest) -> dict:
    task = parse_url_task.delay(str(request.url))

    return {
        "task_id": task.id,
        "status": "queued",
    }
```

Обновлённый docker-compose файл
```yaml
version: "3.9"

services:
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: 123
      POSTGRES_DB: hackathon_db
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"

  api:
    build:
      context: ./lr_1
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "8080:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:123@db:5432/hackathon_db
      DEBUG: "true"
      CREATE_TABLES_ON_STARTUP: "true"
      PARSER_SERVICE_URL: http://scraper:8000
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/1
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
      scraper:
        condition: service_started

  scraper:
    build:
      context: ./lr_2/task_2
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "8001:8001"
    environment:
      DATABASE_URL: postgresql://postgres:123@db:5432/hackathon_db
      DEBUG: "true"
    depends_on:
      db:
        condition: service_healthy

  celery_worker:
    build:
      context: ./lr_1
      dockerfile: Dockerfile
    restart: unless-stopped
    command: celery -A app.celery_app.celery_app worker --loglevel=info
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:123@db:5432/hackathon_db
      DEBUG: "true"
      CREATE_TABLES_ON_STARTUP: "false"
      PARSER_SERVICE_URL: http://scraper:8001
      CELERY_BROKER_URL: redis://redis:6379/0
      CELERY_RESULT_BACKEND: redis://redis:6379/1
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
      scraper:
        condition: service_started

volumes:
  db_data:
```

## Задача 3: Вызов парсера из FastAPI через очередь
Дополнительно был реализован асинхронный вариант запуска парсера через очередь задач.

Основное приложение создаёт задачу Celery, задача помещается в Redis, а Celery worker забирает её из очереди и выполняет обращение к сервису парсера.

```python
celery_app = Celery(
    "hackathon_parser_queue",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1"),
    include=["app.tasks.parser_tasks"],
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)
```

## Результат 
В результате лабораторной работы было создано контейнеризированное приложение из нескольких сервисов. Основное FastAPI-приложение может вызывать парсер напрямую по HTTP или асинхронно через очередь задач Celery с использованием Redis.
Такой подход упрощает развёртывание приложения, разделяет ответственность между сервисами и позволяет выполнять длительные операции в фоне.
