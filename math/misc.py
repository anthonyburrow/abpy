def gamma(z):
    """Gamma function."""
    from combinatorics import factorial

    if isinstance(z, int):
        return factorial(z - 1)

    # if z not int...


def lgamma(n):
    """Log-Gamma function."""
    from numpy import log, pi

    if isinstance(n, int) and n <= 13:
        return log(gamma(n))
    else:
        lg = (n - 0.5) * log(n) - n + 0.5 * log(2 * pi)
        return lg
