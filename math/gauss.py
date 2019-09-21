import numpy as np
from scipy.optimize import curve_fit


def Gauss(x, mu, sigma, A):
    return A * np.exp(-(x - mu)**2 / 2 / sigma**2)


def bimodal(x, mu1, sigma1, A1, mu2, sigma2, A2):
    return Gauss(x, mu1, sigma1, A1) + Gauss(x, mu2, sigma2, A2)


def Gauss2D(data, mux, muy, sigx, sigy, A, ravel=True):
    x, y = data
    argx = ((x - mux) / sigx)**2
    argy = ((y - muy) / sigy)**2
    g = A * np.exp(-0.5 * (argx + argy))
    if ravel:
        g = g.ravel()
    return g


def hist_fit(x_arr, p0=[0, 0.5], hist_bins=10, hist_range=None,
             fit_bounds=(-np.inf, np.inf)):
    # p0 has the form mu, sigma
    h, x = np.histogram(x_arr, bins=hist_bins, range=hist_range, normed=False)
    x = (x[1:] + x[:-1]) / 2  # get centers of bins

    p0 = p0 + [h.max()]

    params, cov = curve_fit(Gauss, x, h, p0=p0, bounds=fit_bounds)

    return params


def hist_fit_bimodal(x_arr, p0=[0, 0.5, 10, 0.5], hist_bins=50, hist_range=None,
                     fit_bounds=(-np.inf, np.inf)):
    # p0 has the form mu1, sigma1, m2, sigma2
    h, x = np.histogram(x_arr, bins=hist_bins, range=hist_range, normed=False)
    x = (x[1:] + x[:-1]) / 2  # get centers of bins

    p0 = p0[0:2] + [h.max() / 2] + p0[2:4] + [h.max()]

    params, cov = curve_fit(bimodal, x, h, p0=p0, bounds=fit_bounds)

    return params


def hist_fit_2d(x_arr, y_arr, p0=[0, 0, 0.5, 0.5], hist_bins=50, hist_range=None,
                fit_bounds=(-np.inf, np.inf)):
    # p0 has the form mux, muy, sigma_x, sigma_y
    h, x, y = np.histogram2d(x_arr, y_arr, bins=hist_bins, range=hist_range,
                             normed=False)
    x = np.array((x[1:] + x[:-1]) / 2)
    y = np.array((y[1:] + y[:-1]) / 2)
    x, y = np.meshgrid(x, y)
    h = h.ravel()

    p0 = p0 + [h.max()]

    params, cov = curve_fit(Gauss2D, (x, y), h, p0=p0)

    return params, cov
