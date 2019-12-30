import numpy as np
from scipy.optimize import curve_fit


def gauss(x, mu, sig, A):
    """1-D Gaussian function"""
    arg = (x - mu) / sig
    return A * np.exp(-0.5 * arg**2)


def gauss_fit(X, mu0=0, sig0=1, hist_bins=40, fit_bounds=(-np.inf, np.inf)):
    """Retrieve a 1-D Gaussian fit.

    Args:
        X (numpy.ndarray): Data to be fit.
        mu0 (float): Initial mean to start approximation.
        sig0 (float): Initial deviation to start approximation.
        hist_bins (int): Number of bins to use for histogram.

    Returns:
        params (array): Optimal values of parameters for fit (mu, sigma, amplitude).
        cov (array): 2D covariance matrix for parameters.

    """
    h, x = np.histogram(X, bins=hist_bins, normed=False)
    x = (x[1:] + x[:-1]) / 2  # get centers of bins

    p0 = [mu0, sig0, h.max()]
    params, cov = curve_fit(gauss, x, h, p0=p0, bounds=fit_bounds)

    return params, cov
