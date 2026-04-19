def min_num_of_drops(n, h):
    dp = [0] * (n + 1)
    moves = 0

    while dp[n] < h:
        moves += 1
        for k in range(n, 0, -1):
            dp[k] = dp[k] + dp[k - 1] + 1

    return moves


def main():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        n, h = map(int, line.strip().split(","))
        print(min_num_of_drops(n, h))


if __name__ == "__main__":
    main()