# Лабораторная 1 — Система проведения хакатонов

**Папка:** `app/`

Документация и отчёт по лабораторной работе 1: серверный бэкенд для управления хакатонами.

## Описание проекта

Проект реализует REST API для управления хакатонами, командами, задачами, отправками и оценками. В сервисе используются:

- FastAPI — веб-фреймворк
- SQLModel — ORM + Pydantic
- PostgreSQL — база данных
- Alembic — миграции
- JWT-аутентификация — защита API
- passlib[bcrypt] — хеширование паролей

## Структура проекта

```
app/
├── core/
│   ├── config.py
│   └── security.py
├── database.py
├── main.py
├── models/
│   ├── user.py
│   ├── hackathon.py
│   ├── team.py
│   ├── task.py
│   ├── submission.py
│   └── evaluation.py
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── hackathons.py
│   ├── teams.py
│   ├── tasks.py
│   ├── submissions.py
│   └── evaluations.py
├── schemas/
│   ├── auth.py
│   ├── user.py
│   ├── hackathon.py
│   ├── team.py
│   ├── task.py
│   ├── submission.py
│   └── evaluation.py
└── services/
    ├── auth.py
    ├── users.py
    ├── hackathons.py
    ├── teams.py
    ├── tasks.py
    ├── submissions.py
    └── evaluations.py

.env.example
requirements.txt
alembic.ini
app/migrations/
```

## Подключение к базе данных

`app/database.py` настраивает SQLModel через `create_engine` и предоставляет зависимость `get_session`.

Конфигурация берётся из `.env`:

- `DB_URL` — URL PostgreSQL
- `SECRET_KEY` — секрет для JWT
- `ACCESS_TOKEN_EXPIRE_MINUTES` — время жизни токена

## Основные доменные модели

### User
- `id`, `email`, `name`, `password_hash`, `role`
- роли: `participant`, `organizer`, `judge`
- связи: `memberships`, `evaluations`

### Hackathon
- `id`, `title`, `description`, `start_date`, `end_date`
- связи: `teams`, `tasks`

### Team / TeamMember
- `Team` — команда участников
- `TeamMember` — член команды с полем `role_in_team`
- связь M:N между `User` и `Team`

### Task
- `id`, `title`, `description`, `hackathon_id`
- связь: `submissions`

### Submission
- `id`, `team_id`, `task_id`, `github_url`, `created_at`
- связь: `evaluations`

### Evaluation
- `id`, `submission_id`, `judge_id`, `score`, `comment`

## Безопасность и аутентификация

`app/core/security.py` реализует:

- хеширование паролей через `passlib[bcrypt]`
- создание JWT-токенов
- проверку и валидацию токена
- получение текущего пользователя
- проверку прав доступа по роли

Защищённые маршруты используют заголовок:

`Authorization: Bearer <token>`

## API / Эндпоинты

### Auth
- `POST /auth/register` — регистрация пользователя
- `POST /auth/login` — логин + получение JWT
- `GET /auth/me` — информация о текущем пользователе
- `POST /auth/change-password` — смена пароля

### Пользователи
- `GET /users/` — список пользователей
- `GET /users/{user_id}` — профиль пользователя
- `PUT /users/{user_id}` — обновление пользователя

### Хакатоны
- `GET /hackathons/` — список хакатонов
- `POST /hackathons/` — создание хакатона (`organizer`)
- `GET /hackathons/{hackathon_id}` — детали хакатона
- `PUT /hackathons/{hackathon_id}` — обновление (`organizer`)
- `DELETE /hackathons/{hackathon_id}` — удаление (`organizer`)

### Команды
- `GET /teams/` — список команд
- `POST /teams/` — создание команды
- `GET /teams/{team_id}` — детали команды
- `POST /teams/{team_id}/join` — присоединение в команду
- `PUT /teams/{team_id}` — обновление команды
- `DELETE /teams/{team_id}` — удаление команды

### Задачи
- `GET /tasks/` — список задач
- `POST /tasks/` — создание задачи (`organizer`)
- `GET /tasks/{task_id}` — детали задачи
- `PUT /tasks/{task_id}` — обновление (`organizer`)
- `DELETE /tasks/{task_id}` — удаление (`organizer`)

### Отправки
- `GET /submissions/` — список отправок
- `POST /submissions/` — создание отправки
- `GET /submissions/{submission_id}` — детали отправки
- `PUT /submissions/{submission_id}` — обновление отправки
- `DELETE /submissions/{submission_id}` — удаление отправки

### Оценки
- `GET /evaluations/` — список оценок
- `POST /evaluations/` — создание оценки (`judge`)
- `GET /evaluations/{evaluation_id}` — детали оценки
- `PUT /evaluations/{evaluation_id}` — редактирование оценки (`judge`)
- `DELETE /evaluations/{evaluation_id}` — удаление оценки

