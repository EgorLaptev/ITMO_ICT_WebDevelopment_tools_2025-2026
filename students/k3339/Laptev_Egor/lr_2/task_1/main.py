import subprocess
import sys
from pathlib import Path


PROGRAMS = [
    "threading_sum.py",
    "multiprocessing_sum.py",
    "async_sum.py",
]


def run_program(program: str) -> None:
    program_path = Path(__file__).with_name(program)

    if not program_path.exists():
        print(f"\n[ERROR] File not found: {program_path}")
        return

    print("=" * 60)
    print(f"Running: {program}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(program_path)],
        text=True,
        capture_output=True,
    )

    if result.stdout:
        print(result.stdout, end="")

    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr, end="")

    if result.returncode != 0:
        print(f"\n[ERROR] {program} exited with code {result.returncode}")


def main() -> None:
    for program in PROGRAMS:
        run_program(program)


if __name__ == "__main__":
    main()