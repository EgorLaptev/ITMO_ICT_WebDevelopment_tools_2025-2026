import asyncio
import time

import aiohttp
from bs4 import BeautifulSoup

from models import URLS, init_db, save_page, split_urls


METHOD = "async"
CONNECTIONS_COUNT = 3


async def parse_and_save(url: str) -> None:
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else "No title"

    await asyncio.to_thread(save_page, url, title, METHOD)
    print(f"[{METHOD}] {url} -> {title}")


async def parse_urls(urls: list[str]) -> None:
    for url in urls:
        try:
            await parse_and_save(url)
        except Exception as exc:
            print(f"[{METHOD}] {url} -> error: {exc}")


async def run_async_scraper(urls: list[str] | None = None) -> float:
    await asyncio.to_thread(init_db)
    started_at = time.perf_counter()
    url_chunks = split_urls(urls or URLS, CONNECTIONS_COUNT)

    await asyncio.gather(*(parse_urls(chunk) for chunk in url_chunks))

    elapsed = time.perf_counter() - started_at
    print(f"[{METHOD}] completed in {elapsed:.2f} seconds")
    return elapsed


if __name__ == "__main__":
    asyncio.run(run_async_scraper())
