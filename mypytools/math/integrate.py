import numpy as np


def integrate(X, y, *args, **kwargs):
    """Integrate function.

    Defaults to constant dx.

    Args:
        X (tuple, numpy.ndarray): Bounds of integral or input space.
        func: Function or output array.

    Returns:
        integral (float): Definte integral value.

    """
    n = len(X)
    assert n > 1, \
        'Must have more than one input for `X`.'
    if n == 2:
        return _gen_integral(X, y, *args, **kwargs)
    else:
        X = np.asarray(X)
        y = np.asarray(y)
        assert X.shape == y.shape, \
            '`X` and `y` must have same shape.'
        return _spec_integral(X, y, *args, **kwargs)


def _gen_integral(bounds, func, N=1000, eps=0.0001, *args, **kwargs):
    """Generic definite integral from `a` to `b`.

    Used with no set input values. Currently forces constant dx.

    Args:

        bounds (tuple): Lower and upper bounds of integration.
        func: Function to integrate over (a, b). Must accept array inputs. Must
            have input variable as first parameter.
        N (int): Number of intervals (not points).
        eps (float): Limit of accuracy.

    Returns:
        integral (float): Definte integral value.

    """
    a, b = bounds
    dx = (b - a) / N
    x = np.linspace(a, b, N)
    f = func(x, *args, **kwargs)
    integral = _int_const_dx(dx, f)

    return integral


def _spec_integral(X, y, uniform_input=True):
    """Integrate with specified domain and output.

    Args:
        X (numpy.ndarray): Input values.
        y (numpy.ndarray): Output values.
        const_dx (bool): Input values are uniformly spaced. Assumed True.

    Returns:
        integral (float): Definte integral value.

    """
    if uniform_input:
        dx = X[1] - X[0]
        integral = _int_const_dx(dx, y)
        return integral

    integral = _int_var_dx(X, y)
    return integral


def _int_const_dx(dx, y):
    """Integral algorithm for uniform input space."""
    integral = np.sum(y[1:-1]) + 0.5 * (y[0] + y[-1])
    integral *= dx

    return integral


def _int_var_dx(X, y):
    """Integral algorithm for variable input space."""
    f = y[1:] + y[:-1]
    dx = X[1:] - X[:-1]
    integral = 0.5 * np.dot(f, dx)

    return integral
