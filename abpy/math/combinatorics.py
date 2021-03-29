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
def factorial(n: int) -> int:
    """Factorial (!) of a nonnegative integer."""
    assert n >= 0

    if n == 0:
        return 1

    return n * factorial(n - 1)


def combination(n: int, k: int) -> int:
    """Combinations of n things taken k at a time with no repetition."""
    if k > n:
        return 0

    return int(factorial(n) / (factorial(k) * factorial(n - k)))
