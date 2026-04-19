from datetime import datetime
import math

INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"

FREE_MINUTES = 30
FIRST_PHASE_MINUTES = 3 * 60
FIRST_PHASE_RATE = 300        
SECOND_PHASE_RATE = 500       
DAILY_CAP = 10000             


def calculate_fee(start: datetime, end: datetime) -> int:
    if end < start:
        return -1

    total_minutes = (end - start).total_seconds() / 60

    full_days = int(total_minutes // (24 * 60))
    remaining_minutes = total_minutes % (24 * 60)

    total_cost = full_days * DAILY_CAP

    if remaining_minutes <= FREE_MINUTES:
        return int(total_cost)

    remaining_minutes -= FREE_MINUTES

    first_phase = min(remaining_minutes, FIRST_PHASE_MINUTES)
    cost_first = math.ceil(first_phase / 60) * FIRST_PHASE_RATE

    second_phase = max(0, remaining_minutes - FIRST_PHASE_MINUTES)
    cost_second = math.ceil(second_phase / 60) * SECOND_PHASE_RATE

    total_cost += cost_first + cost_second

    if total_cost > (full_days + 1) * DAILY_CAP:
        total_cost = (full_days + 1) * DAILY_CAP

    return int(total_cost)


def parse_line(line: str):
    parts = line.split()
    if len(parts) < 5:
        return None

    plate = parts[0]
    start_str = parts[1] + " " + parts[2]
    end_str = parts[3] + " " + parts[4]

    try:
        start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
    except:
        return None

    return plate, start, end


def main():
    results = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        if not line or line.startswith("RENDSZAM") or line.startswith("="):
            continue

        parsed = parse_line(line)
        if not parsed:
            results.append(f"HIBAS_BEMENET")
            continue

        plate, start, end = parsed
        fee = calculate_fee(start, end)

        if fee == -1:
            results.append(f"{plate}: HIBAS_IDO")
        else:
            results.append(f"{plate}: {fee} Ft")

    for r in results:
        print(r)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in results:
            f.write(r + "\n")


if __name__ == "__main__":
    main()