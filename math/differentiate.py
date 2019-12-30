def derivative(X, func, dx=0.000001, *args, **kwargs):
    """Calculate the derivative at point(s).

    Args:
        X (float, numpy.ndarray): Input points.
        func: Function of which to take derivative. Must take input as first
              parameter.
        dx (float): Step size.

    Returns:
        fprime (float, numpy.ndarray): Derivative of function at inputs.

    """
    x0 = X - dx
    x1 = X + dx
    f0 = func(x0, *args, **kwargs)
    f1 = func(x1, *args, **kwargs)
    fprime = 0.5 * (f1 - f0) / dx

    return fprime
