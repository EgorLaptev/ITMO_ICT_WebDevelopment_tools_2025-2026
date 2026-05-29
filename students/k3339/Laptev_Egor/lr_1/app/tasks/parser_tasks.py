import os

import requests

from app.celery_app import celery_app


PARSER_SERVICE_URL = os.getenv("PARSER_SERVICE_URL", "http://scraper:8001")


@celery_app.task(name="parser.parse_url")
def parse_url_task(url: str) -> dict:
    response = requests.post(
        f"{PARSER_SERVICE_URL}/parse/single",
        params={"url": url, "method": "async"},
        timeout=60,
    )

    response.raise_for_status()
    return response.json()