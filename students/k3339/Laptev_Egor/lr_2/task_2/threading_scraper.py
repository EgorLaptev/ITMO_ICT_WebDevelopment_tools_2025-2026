import threading
import time

import requests
from bs4 import BeautifulSoup

from models import URLS, init_db, save_page, split_urls


METHOD = "threading"
THREADS_COUNT = 3


def parse_and_save(url: str) -> None:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "No title"

    save_page(url, title, METHOD)
    print(f"[{METHOD}] {url} -> {title}")


def parse_urls(urls: list[str]) -> None:
    for url in urls:
        try:
            parse_and_save(url)
        except Exception as exc:
            print(f"[{METHOD}] {url} -> error: {exc}")


def run_threading_scraper(urls: list[str] | None = None) -> float:
    init_db()
    started_at = time.perf_counter()
    url_chunks = split_urls(urls or URLS, THREADS_COUNT)

    threads = [
        threading.Thread(target=parse_urls, args=(chunk,))
        for chunk in url_chunks
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - started_at
    print(f"[{METHOD}] completed in {elapsed:.2f} seconds")
    return elapsed


if __name__ == "__main__":
    run_threading_scraper()
