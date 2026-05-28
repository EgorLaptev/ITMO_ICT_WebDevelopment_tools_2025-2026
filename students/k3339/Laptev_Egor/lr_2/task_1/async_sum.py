import asyncio
import time
import os


N = 100_000_000
WORKERS = os.cpu_count() or 4


async def calculate_sum(start: int, end: int) -> int:
    total = 0

    for number in range(start, end + 1):
        total += number

    return total


def split_range(n: int, parts: int) -> list[tuple[int, int]]:
    chunk_size = n // parts
    ranges = []

    start = 1
    for i in range(parts):
        end = start + chunk_size - 1

        if i == parts - 1:
            end = n

        ranges.append((start, end))
        start = end + 1

    return ranges


async def main() -> None:
    start_time = time.perf_counter()

    ranges = split_range(N, WORKERS)

    tasks = [
        asyncio.create_task(calculate_sum(start, end))
        for start, end in ranges
    ]

    results = await asyncio.gather(*tasks)

    total = sum(results)
    elapsed = time.perf_counter() - start_time

    print(f"Approach: async")
    print(f"Workers: {WORKERS}")
    print(f"Result: {total}")
    print(f"Time: {elapsed:.6f} seconds\n\n")


if __name__ == "__main__":
    asyncio.run(main())