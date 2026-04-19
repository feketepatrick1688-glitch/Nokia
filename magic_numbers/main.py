from pathlib import Path

def next_magic_num(n: int) -> int:
    s = list(str(n))
    l = len(s)

    p = s[:]
    for i in range(l // 2):
        p[-1 - i] = p[i]

    palindrom = int("".join(p))
    if palindrom > n:
        return palindrom

    i = (l - 1) // 2
    while i >= 0 and p[i] == '9':
        p[i] = '0'
        p[-1 - i] = '0'
        i -= 1

    if i < 0:
        return int("1" + ("0" * (l - 1)) + "1")

    p[i] = str(int(p[i]) + 1)
    p[-1 - i] = p[i]

    return int("".join(p))


def parse_line(line: str) -> int:
    line = line.strip()
    if "^" in line:
        a, b = line.split("^")
        return pow(int(a), int(b))
    return int(line)


def main():
    lines = Path("input.txt").read_text().splitlines()

    for line in lines:
        if not line.strip():
            continue
        n = parse_line(line)
        print(next_magic_num(n))


if __name__ == "__main__":
    main()
#test