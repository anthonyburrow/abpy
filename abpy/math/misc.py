def gamma(z):
    """Gamma function."""
    from combinatorics import factorial

    if isinstance(z, int):
        return factorial(z - 1)

    # if z not int...


def lgamma(n):
    """Log-Gamma approximation for large `n`."""
    from numpy import log, pi

    lg = (n - 0.5) * log(n) - n + 0.5 * log(2 * pi)
    return lg
