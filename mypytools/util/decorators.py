def timing(f):
    """Time a function."""
    import time

    def wrapper(*args, **kwargs):
        t1 = time.time()
        ret = f(*args, **kwargs)
        t2 = time.time()
        print('%s took %.3f ms' % (f.__name__, (t2 - t1) * 1000.0))
        return ret
    return wrapper
