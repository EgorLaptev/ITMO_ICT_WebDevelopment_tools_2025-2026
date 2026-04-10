# Практика 2 — SQLModel

Подключение PostgreSQL через SQLModel.

## Подключение к БД (`db.py`)

```python
DATABASE_URL = "postgresql://postgres:123@db/warriors_db"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

## Модели (`models.py`)

```python
class RaceType(Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class SkillWarriorLink(SQLModel, table=True):
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    warrior_id: Optional[int] = Field(default=None, foreign_key="warrior.id", primary_key=True)
    level: int | None


class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = ""
    warriors: Optional[List["Warrior"]] = Relationship(
        back_populates="skills", link_model=SkillWarriorLink
    )


class Profession(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    warriors_prof: List["Warrior"] = Relationship(back_populates="profession")


class WarriorDefault(SQLModel):
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")


class Warrior(WarriorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    skills: Optional[List[Skill]] = Relationship(
        back_populates="warriors", link_model=SkillWarriorLink
    )


class WarriorProfessions(WarriorDefault):
    profession: Optional[Profession] = None
```

## API Endpoints

- GET / — hello
- GET /warriors_list
- GET /warrior/{warrior_id}
- POST /warrior
- PATCH /warrior/{warrior_id}
- DELETE /warrior/{warrior_id}
- GET /professions_list
- GET /profession/{profession_id}
- POST /profession


## Запуск

```bash
pip install fastapi[all] sqlmodel psycopg2-binary
uvicorn main:app --reload
```
