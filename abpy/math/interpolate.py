import numpy as np


def linear(x_new, x, y, y_err=None):
    '''

    '''
    if isinstance(x_new, (float, int)):
        x_new = np.array([x_new])

    x_new = np.asarray(x_new)
    x = np.asarray(x)
    y = np.asarray(y)
    if y_err is not None:
        y_err = np.asarray(y_err)

    lower_mask = x[0] < x_new
    upper_mask = x_new < x[-1]
    total_mask = lower_mask * upper_mask
    x_check = x_new[total_mask]

    y_new = np.zeros_like(x_new)
    y_new[~lower_mask] = y[0]
    y_new[~upper_mask] = y[-1]

    if y_err is not None:
        y_var = y_err**2
        y_var_new = np.zeros_like(x_new)
        y_var_new[~lower_mask] = y_var[0]
        y_var_new[~upper_mask] = y_var[-1]

    ind_upper = np.searchsorted(x, x_check)
    ind_lower = ind_upper - 1

    dx_total = x[ind_upper] - x[ind_lower]
    slope = (y[ind_upper] - y[ind_lower]) / dx_total

    dx = x_check - x[ind_lower]
    y_new[total_mask] = y[ind_lower] + dx * slope

    if y_err is not None:
        upper_dx = x[ind_upper] - x_check
        upper_err_mask = upper_dx < dx
        lower_err_mask = ~upper_err_mask

        slope_var = (y_var[ind_upper] + y_var[ind_lower]) / dx_total**2

        # some absolute BS to do nested masking
        lower_err_ind = tuple([a[lower_err_mask] for a in np.where(total_mask)])
        upper_err_ind = tuple([a[upper_err_mask] for a in np.where(total_mask)])

        y_var_new[lower_err_ind] = \
            y_var[ind_lower][lower_err_mask] + \
            dx[lower_err_mask]**2 * slope_var[lower_err_mask]
        y_var_new[upper_err_ind] = \
            y_var[ind_upper][upper_err_mask] + \
            upper_dx[upper_err_mask]**2 * slope_var[upper_err_mask]

        return y_new, y_var_new

    return y_new


def power_law(X: float | np.ndarray, data: np.ndarray) -> float:
    x_data = data[:, 0]
    y_data = data[:, 1]

    return_float = isinstance(X, float)
    if return_float:
        X = np.array([X])

    Y = np.zeros_like(X)

    ind_X = np.searchsorted(x_data, X) - 1

    # Check if X lie outside x_data
    N = len(x_data)

    Y[ind_X == -1] = y_data[0]
    Y[ind_X == N - 1] = y_data[-1]
    interp_mask = (ind_X != -1) & (ind_X != N - 1)
    ind_X = ind_X[interp_mask]
    ind_X_next = ind_X + 1

    N_interp = len(ind_X)
    if N_interp == 0:
        return Y[0] if return_float else Y

    Y_interp = np.zeros(N_interp)

    # Look for a sign change
    do_log = x_data[ind_X] * x_data[ind_X_next] > 0.

    # Power law interpolation
    y_rat = y_data[ind_X_next][do_log] / y_data[ind_X][do_log]
    x_rat = x_data[ind_X_next][do_log] / x_data[ind_X][do_log]
    power = np.log(y_rat) / np.log(x_rat)

    x_rat_x = X[interp_mask][do_log] / x_data[ind_X][do_log]

    Y_interp[do_log] = y_data[ind_X][do_log] * x_rat_x**power

    if np.all(do_log):
        Y[interp_mask] = Y_interp
        return Y[0] if return_float else Y

    # Linear interpolate across sign changes
    slope = (y_data[ind_X_next][~do_log] - y_data[ind_X][~do_log]) / \
            (x_data[ind_X_next][~do_log] - x_data[ind_X][~do_log] + 1.e-70)

    Y_interp[~do_log] = \
        y_data[ind_X][~do_log] + \
        slope * (X[interp_mask][~do_log] - x_data[ind_X][~do_log])

    Y[interp_mask] = Y_interp

    return Y[0] if isinstance(X, float) else Y


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    N = 20
    sigma = 0.1

    x_data = np.linspace(-10., 10., N)
    y_data = x_data**3. + np.random.normal(scale=sigma, size=N)
    data = np.c_[x_data, y_data]

    x_interp = np.linspace(0, 10, 15)
    y_interp = interp_power_law(x_interp, data)

    fig, ax = plt.subplots()

    ax.plot(x_data, y_data, 'ko')
    ax.plot(x_interp, y_interp, 'ro')

    plt.show()
