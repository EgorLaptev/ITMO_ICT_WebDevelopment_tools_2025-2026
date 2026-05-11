import asyncio
import multiprocessing

from async_scraper import run_async_scraper
from multiprocessing_scraper import run_multiprocessing_scraper
from threading_scraper import run_threading_scraper


def print_comparison(results: dict[str, float]) -> None:
    fastest = min(results.values())

    print("\nExecution time comparison:")
    print("-" * 58)
    print(f"{'Approach':<20}{'Time, seconds':<18}{'Speedup':<12}")
    print("-" * 58)

    for approach, elapsed in results.items():
        speedup = elapsed / fastest if fastest else 0
        print(f"{approach:<20}{elapsed:<18.2f}{speedup:<12.2f}x")


def main() -> None:
    results = {
        "Threading": run_threading_scraper(),
        "Multiprocessing": run_multiprocessing_scraper(),
        "Async": asyncio.run(run_async_scraper()),
    }

    print_comparison(results)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
