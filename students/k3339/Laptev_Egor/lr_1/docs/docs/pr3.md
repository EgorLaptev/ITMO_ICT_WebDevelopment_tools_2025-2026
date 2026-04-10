# Практика 3 — Alembic, .env

Добавлены миграции через Alembic, переменные окружения через .env

## Структура

```
practice/
├── app/
│   ├── main.py
│   ├── db.py
│   └── models.py
├── migrations/
│   ├── env.py
│   ├── versions/
│   └── script.py.mako
├── alembic.ini
├── .env.example
└── .gitignore
```

## Подключение к БД через .env (`app/db.py`)

```python
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

## migrations/env.py

```python
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from app.models import *  

load_dotenv()
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", ""))
target_metadata = SQLModel.metadata
```

## Сущность с дополненным полем

```python
class SkillWarriorLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    warrior_id: Optional[int] = Field(default=None, foreign_key="warrior.id", primary_key=True)
    level: int | None
```

## .gitignore

```
*.pyc
*.pyo
.DS_Store
**/.idea/
**/.vscode/
venv
**/__pycache__/
*.env
.env.local
.env.*.local
*.log
dist/
build/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/
instance/
.mypy_cache/
.ruff_cache/

```

## Миграции

```bash
pip install alembic python-dotenv
alembic revision --autogenerate -m "new"
alembic upgrade head
```
