from pathlib import Path

def is_palindrome(n: int) -> bool:
    s = str(n)
    return s == s[::-1]

def next_magic_num(num: int) -> int:
    if num < 0:
        return 0
    candidate = num + 1
    while not is_palindrome(candidate):
        candidate += 1
    return candidate
print("next_magic_num(808)  =>", next_magic_num(808))
print("next_magic_num(999)  =>", next_magic_num(999))   
print("next_magic_num(2133) =>", next_magic_num(2133)) 


if __name__ == "__main__":
    main()
