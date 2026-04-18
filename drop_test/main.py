from pathlib import Path

def min_num_of_drops(n, h):
    dp = [0] * (n + 1)
    moves = 0

    while dp[n] < h:
        moves += 1
        for i in range(n, 0, -1):
            dp[i] = dp[i] + dp[i - 1] + 1

    return moves


def main():
    lines = Path("input.txt").read_text().splitlines()

    for line in lines:
        if not line.strip():
            continue

        n, h = map(int, line.split(","))
        print(min_num_of_drops(n, h))


if __name__ == "__main__":
    main()