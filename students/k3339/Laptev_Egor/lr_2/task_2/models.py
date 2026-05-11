import math
import os
from datetime import datetime
from typing import Iterable, Optional

from sqlmodel import Field, Session, SQLModel, create_engine
from sqlalchemy.engine import Engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123@localhost:5432/hackathon_db",
)
_engine: Engine | None = None

URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://github.com",
    "https://www.google.com",
]


class ParsedPage(SQLModel, table=True):
    __tablename__ = "parsed_pages"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True)
    title: str
    method: str = Field(index=True)
    scraped_at: datetime = Field(default_factory=datetime.utcnow)


def get_engine():
    global _engine

    if _engine is not None:
        return _engine

    connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    _engine = create_engine(DATABASE_URL, connect_args=connect_args)
    return _engine


def init_db() -> None:
    SQLModel.metadata.create_all(get_engine())


def save_page(url: str, title: str, method: str) -> ParsedPage:
    page = ParsedPage(url=url, title=title, method=method)
    with Session(get_engine()) as session:
        session.add(page)
        session.commit()
        session.refresh(page)
    return page


def split_urls(urls: Iterable[str], parts: int) -> list[list[str]]:
    url_list = list(urls)
    if not url_list:
        return []

    chunk_size = math.ceil(len(url_list) / max(1, parts))
    return [
        url_list[index:index + chunk_size]
        for index in range(0, len(url_list), chunk_size)
    ]
