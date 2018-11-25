def memoize(func):
    import functools
    cache = func.cache = {}

    @functools.wraps(func)
    def wrapper(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]
    return wrapper


@memoize
def Factorial(n):
    if not isinstance(n, int):
        print('Parameter must be an integer.')
        return
    elif n < 0:
        print('Parameter must be a nonnegative integer.')
        return
    elif n == 0:
        return 1

    return n * Factorial(n - 1)


def Combination(n, k):
    if not isinstance(n, int) or not isinstance(k, int):
        print('Parameters must be integers.')
        return
    if k > n:
        return 0

    return int(Factorial(n) / (Factorial(k) * Factorial(n - k)))
