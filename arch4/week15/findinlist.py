def find_in_list(n: any, lst: list) -> bool:
    return n in lst


def rec_find_in_list(n: any, lst: list) -> bool:
    if not lst:
        return False
    return lst[0] == n or rec_find_in_list(n, lst[1:])


if __name__ == "__main__":
    lst = [42, 'abc', 'smile', 8910, (12, 22, 32)]
    print(find_in_list(42, lst))
    print(rec_find_in_list("smile", lst))
    print(rec_find_in_list("2", lst))
