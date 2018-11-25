def Derivative(func, x, eps=0.00001, dx0=1, direction='symmetric'):
    dx = dx0
    fp0 = 0
    count = 0
    while True:
        if direction == 'right':
            x0, x1 = (x, x + dx)
            fp1 = (func(x1) - func(x0)) / dx
        elif direction == 'left':
            x0, x1 = (x - dx, x)
            fp1 = (func(x1) - func(x0)) / dx
        elif direction == 'symmetric':
            x0, x1 = (x - dx, x + dx)
            fp1 = (func(x1) - func(x0)) / (2 * dx)

        if count != 0:
            if abs(fp1 - fp0) < eps:
                return fp1

        fp0 = fp1
        dx /= 2
        count += 1


def nDerivative(func, x, order, eps=0.00001, dx0=1):
    if order < 0:
        print('Order of derivative must be a nonnegative integer.')
        return
    if order == 0:
        return func(x)

    from .combinatorics import Combination

    dx = dx0
    fp0 = 0
    count = 0
    while True:
        s = 0
        for k in range(order + 1):
            s += (-1)**(k + 1) * Combination(order, k) * func(x + k * dx)

        fp1 = s / (dx**order)

        if count != 0:
            if abs(fp1 - fp0) < eps:
                return fp1

        fp0 = fp1
        dx /= 2
        count += 1
