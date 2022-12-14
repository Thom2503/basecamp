import time

CUR_ITER = 0


def calc_time(func: callable):
    def inner(*args, **kwargs):
        global CUR_ITER
        CUR_ITER += 1

        begin_time = time.time()

        num = func(*args, **kwargs)

        end_time = time.time()

        if CUR_ITER == args[0]:
            print(end_time - begin_time)
        return num
    return inner


@calc_time
def fact(n: int) -> int:
    if n == 1 or n == 0:
        return 1
    else:
        return n * fact(n - 1)


if __name__ == "__main__":
    print(fact(400))
