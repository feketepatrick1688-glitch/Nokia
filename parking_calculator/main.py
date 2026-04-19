from pathlib import Path
from datetime import datetime
import math


def calculate_fee(start, end):
    if end < start:
        return "ERROR"

    total_minutes = int((end - start).total_seconds() // 60)

    days = total_minutes // (24 * 60)
    remaining = total_minutes % (24 * 60)

    fee = days * 10000

    if remaining <= 30:
        return fee

    remaining -= 30

    first_block = min(remaining, 180)
    fee += math.ceil(first_block / 60) * 300

    remaining -= first_block
    if remaining > 0:
        fee += math.ceil(remaining / 60) * 500

    return fee


def main():
    lines = Path("input.txt").read_text(encoding="utf-8").splitlines()
    output_lines = []

    for line in lines:
        if not line.strip() or "-" not in line or ":" not in line:
            continue

        try:
            parts = line.split()
            plate = parts[0]

            start = datetime.strptime(parts[1] + " " + parts[2], "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(parts[3] + " " + parts[4], "%Y-%m-%d %H:%M:%S")

            fee = calculate_fee(start, end)

        except Exception:
            fee = "ERROR"

        output_lines.append(f"{plate} {fee}")

    Path("output.txt").write_text("\n".join(output_lines), encoding="utf-8")

    print("\n".join(output_lines))


if __name__ == "__main__":
    main()