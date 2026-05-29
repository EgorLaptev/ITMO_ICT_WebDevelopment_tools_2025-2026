"""FastAPI приложение для парсера веб-сайтов."""
import asyncio
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import uvicorn

from async_scraper import run_async_scraper
from multiprocessing_scraper import run_multiprocessing_scraper
from threading_scraper import run_threading_scraper
from models import init_db


app = FastAPI(
    title="Web Scraper API",
    description="API для парсинга веб-сайтов с различными методами",
    version="1.0.0",
)


class URLList(BaseModel):
    """Модель для списка URL"""
    urls: list[str] = Field(..., description="Список URL для парсинга")
    method: Optional[str] = Field(
        "async",
        description="Метод парсинга: 'async', 'threading', или 'multiprocessing'"
    )


class ScrapeResponse(BaseModel):
    """Модель ответа при парсинге"""
    status: str = Field(..., description="Статус выполнения")
    method: str = Field(..., description="Используемый метод")
    urls_count: int = Field(..., description="Количество обработанных URL")
    message: str = Field(..., description="Сообщение о результате")


class URLResponse(BaseModel):
    """Модель для отдельного URL"""
    id: Optional[int] = None
    url: str
    title: str
    method: str
    scraped_at: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Инициализация БД при запуске приложения"""
    await asyncio.to_thread(init_db)


@app.get("/", tags=["root"])
async def read_root():
    """Корневой endpoint с информацией об API"""
    return {
        "message": "Web Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "parse": "/parse",
            "parse_single": "/parse/single",
            "health": "/health"
        }
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}


@app.post("/parse", response_model=ScrapeResponse, tags=["scraping"])
async def parse_urls(request: URLList):
    """
    Парсить множество URL с выбранным методом.
    
    - **urls**: Список URL для парсинга
    - **method**: Метод парсинга (async, threading, multiprocessing)
    """
    if not request.urls:
        raise HTTPException(status_code=400, detail="Список URL не может быть пустым")
    
    if request.method not in ["async", "threading", "multiprocessing"]:
        raise HTTPException(
            status_code=400,
            detail="Неподдерживаемый метод. Используйте 'async', 'threading' или 'multiprocessing'"
        )
    
    try:
        if request.method == "async":
            await run_async_scraper(request.urls)
        elif request.method == "threading":
            await asyncio.to_thread(run_threading_scraper, request.urls)
        elif request.method == "multiprocessing":
            await asyncio.to_thread(run_multiprocessing_scraper, request.urls)
        
        return ScrapeResponse(
            status="success",
            method=request.method,
            urls_count=len(request.urls),
            message=f"Парсинг {len(request.urls)} URL завершён методом '{request.method}'"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка парсинга: {str(e)}")


@app.post("/parse/single", response_model=ScrapeResponse, tags=["scraping"])
async def parse_single_url(
    url: str = Query(..., description="URL для парсинга"),
    method: str = Query("async", description="Метод парсинга")
):
    """
    Парсить одиночный URL.
    
    - **url**: URL для парсинга
    - **method**: Метод парсинга (async, threading, multiprocessing)
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL не может быть пустым")
    
    return await parse_urls(URLList(urls=[url], method=method))


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
