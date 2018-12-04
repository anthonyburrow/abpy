class Binomial:

    def __init__(self, k, n, p):
        self.k = k
        self.n = n
        self.p = p

    def CheckParams(k=None, n=None, p=None):
        if k is not None:
            if not isinstance(k, int):
                print('Number of successes must be an integer.')
        if n is not None:
            if not isinstance(n, int):
                print('Number of trials must be an integer.')
        if k is not None and n is not None and k > n:
            print('Number of successes must not exceed total number of trials.')
        if p is not None:
            if p < 0:
                print('Probability of success must be nonnegative.')

    def Probability(self, k=None, n=None, p=None):
        if k is None:
            k = self.k
        if n is None:
            n = self.n
        if p is None:
            p = self.p

        self.CheckParams(k=k, n=n, p=p)

        from .combinatorics import Combination

        f = Combination(n, k) * \
            p**k * (1 - p)**(n - k)

        return f

    def ExpectedValue(self, n=None, p=None):
        if n is None:
            n = self.n
        if p is None:
            p = self.p

        self.CheckParams(n=n, p=p)

        return n * p

    def Variance(self, n=None, p=None):
        if n is None:
            n = self.n
        if p is None:
            p = self.p

        self.CheckParams(n=n, p=p)

        return n * p * (1 - p)


class Poisson:

    def __init__(self, k, lam):
        self.k = k
        self.lam = lam

    def CheckParams(k=None, lam=None):
        if k is not None:
            if not isinstance(k, int) or k < 0:
                print('Number of events must be a positive integer.')
        if lam is not None:
            if lam < 0:
                print('Rate must be a positive real number.')

    def Probability(self, k=None, lam=None):
        if k is None:
            k = self.k
        if lam is None:
            lam = self.lam

        self.CheckParams(k=k, lam=lam)

        from math import exp, log
        from .combinatorics import Factorial, lGamma

        f = lam**k * exp(-lam) / Factorial(k)
        f = exp(k * log(lam) - lam - lGamma(k + 1))

        return f

    def ExpectedValue(self, lam=None):
        if lam is None:
            lam = self.lam

        self.CheckParams(lam=lam)

        return lam

    def Variance(self, lam=None):
        if lam is None:
            lam = self.lam

        self.CheckParams(lam=lam)

        return lam
