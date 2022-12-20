def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def rec_factorial(n: int) -> int:
    return n * rec_factorial(n - 1) if n else 1


if __name__ == "__main__":
    print(factorial(10))
    print(rec_factorial(10))
