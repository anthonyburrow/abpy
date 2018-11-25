def NewtonMethod(func, args, var_index, set_value=0, eps=0.0001,
                 init_dx=1):
    x0, x1 = (0, init_dx)
    new_args = args[:]
    new_args.insert(var_index, x0)
    f0 = func(*new_args) - set_value
    while True:
        new_args = args[:]
        new_args.insert(var_index, x1)
        f1 = func(*new_args) - set_value

        if abs(f1) < eps:
            return x1

        fprime = (f1 - f0) / (x1 - x0)

        x0 = x1
        x1 = x1 - (f1 / fprime)
        f0 = f1

    return x1
