# fast number powering


def power(a, n):
    if n == 0:
        return 1
    if n % 2 == 1:
        return power(a, n - 1) * a
    else:
        return power(a ** 2, n // 2)


print(power(2, 10))
