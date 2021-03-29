from numpy import exp, log

from .misc import lgamma
from .combinatorics import factorial, combination


class binomial:

    @staticmethod
    def pdf(k: int, n: int, p: float) -> float:
        if k == 0:
            return (1 - p)**n

        f = combination(n, k) * p**k * (1 - p)**(n - k)

        return f

    @staticmethod
    def mean(n: int, p: float):
        return n * p

    @staticmethod
    def var(n: int, p: float):
        return n * p * (1 - p)


class poisson:

    @staticmethod
    def pdf(k: int, lam: float):
        f = lam**k * exp(-lam) / factorial(k)
        f = exp(k * log(lam) - lam - lgamma(k + 1))

        return f

    @staticmethod
    def mean(lam: float):
        return lam

    @staticmethod
    def var(lam: float):
        return lam
