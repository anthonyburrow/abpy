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


def Gamma(n):
    if isinstance(n, int):
        return Factorial(n - 1)
    # elif not isinstance(n, int) and n > 0:


def lGamma(n):
    from math import log, pi

    if n <= 13:
        return log(Gamma(n))
    else:
        lg = (n - 0.5) * log(n) - n + 0.5 * log(2 * pi)
        return lg
