import multiprocessing as mp
import time
import os


N = 10_000_000_000_000
WORKERS = os.cpu_count() or 4


def calculate_sum(start: int, end: int) -> int:
    count = end - start + 1
    return (start + end) * count // 2


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


def main() -> None:
    start_time = time.perf_counter()

    ranges = split_range(N, WORKERS)

    with mp.Pool(processes=WORKERS) as pool:
        results = pool.starmap(calculate_sum, ranges)

    total = sum(results)
    elapsed = time.perf_counter() - start_time

    print(f"Approach: multiprocessing")
    print(f"Workers: {WORKERS}")
    print(f"Result: {total}")
    print(f"Time: {elapsed:.6f} seconds\n\n")


if __name__ == "__main__":
    main()