import numpy as np
from itertools import product


class MultiGauss:

    """
    Data has m dimensions with n data points
    Read in data X in the form of (x1, x2, ...), where x1, x2, ... are (n,) arrays.
    Mu is an (m,) array
    """

    def __init__(self, mu, cov, cov_inv=None, cov_det=None):
        self.m = len(mu)   # Dimensions
        self.mu = np.asarray(mu)
        self.cov = cov

        if cov_inv is None:
            self.cov_inv = np.linalg.inv(cov)
        else:
            self.cov_inv = cov_inv

        if cov_det is None:
            self.cov_det = np.linalg.det(cov)
        else:
            self.cov_det = cov_det

    def pdf(self, X, normalize=True, ravel=False):
        X = np.asarray(X)

        if len(X.shape) == 1:
            return self._gauss(X, normalize=normalize)

        self.n = len(X[0])   # Number of data points

        for i in range(1, self.m):
            assert len(X[i]) == self.n, \
                'row %i with shape %s has different dimension from %s' % (
                i, str(X[i].shape), str(X[0].shape))

        f = []

        for combination in product(*X):
            x = np.array(combination)
            f.append(self._gauss(x, normalize=normalize))

        f = np.array(f).reshape(self.n, self.n).T

        if ravel:
            f = f.ravel()

        return f

    def _gauss(self, x, normalize):
        x_mu = x.T - self.mu

        arg = np.matmul(self.cov_inv, x_mu)
        arg = np.matmul(x_mu.T, arg)
        f = np.exp(-0.5 * arg)

        if normalize:
            f /= np.sqrt(self.cov_det * (2 * np.pi)**x.shape[0])

        return f
