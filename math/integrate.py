def Trapezoidal(func, a, b, eps=0.0001, n0=1000, *args):
    n = n0
    s = 0
    while True:
        s_new = 0
        for i in range(1, n + 1):
            dx = (b - a) / n
            x_i = a + dx * i

            s_new += dx * func(x_i, *args)

        if s != 0:
            if abs(s_new - s) < eps:
                return s_new

        s = s_new
        n *= 2
