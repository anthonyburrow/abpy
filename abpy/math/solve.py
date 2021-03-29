def newton(func, eps=0.00001, *args, **kwargs):
    """Calculate root using Newton's method.

    Finds the closest root to 0; does not return multiple roots.

    Args:
        func: Function set to zero. Must have input as first parameter.
        eps (float): Accuracy/limit for appoximation.

    Returns:
        x0 (float): Root of the function.

    """
    x0, x1 = (0, 0.1)
    f0 = func(0, *args, **kwargs)

    max_iter = 1000
    count = 0

    while count < max_iter:
        if abs(f0) < eps:
            return x0

        f1 = func(x1, *args, **kwargs)
        fprime = (f1 - f0) / (x1 - x0)

        x0 = x1
        x1 = x1 - (f1 / fprime)
        f0 = f1

        count += 1

    return x0
