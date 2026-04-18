from pathlib import Path

def next_magic_num(n: int) -> int:
    if n < 0:
        return 0
    s = str(n)
    length = len(s)
    
    def generate_palindrome(left: str, even: bool) -> int:
        pal = left
        if not even:
            pal += left[-1]
        pal += left[:-1][::-1] if even else left[::-1]
        return int(pal)
    
    half = (length + 1) // 2
    left = s[:half]
    pal = generate_palindrome(left, length % 2 == 0)
    
    if pal > n:
        return pal
    
    left_num = int(left) + 1
    left_str = str(left_num).zfill(half)
    if len(left_str) > half:
        return 10**length + 1
    return generate_palindrome(left_str, length % 2 == 0)

def main():
    data = Path("input.txt").read_text(encoding="utf-8").strip()
    for line in data.splitlines():
        if line.strip():
            num = int(line.strip())
            print(next_magic_num(num))

if __name__ == "__main__":
    main()