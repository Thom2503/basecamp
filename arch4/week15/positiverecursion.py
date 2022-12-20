def rec_print(n: int) -> None:
    if n < 0:
        return
    rec_print(n - 1)
    print(n)


if __name__ == "__main__":
    rec_print(10)
