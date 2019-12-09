import numpy as np
from itertools import product, repeat


class MultiGauss:

    """
    Data has m dimensions with n data points
    Read in data X in the form of (x1, x2, ...), where x1, x2, ... are (n,) arrays.
    Mu is an (m,) array
    """

    def __init__(self, mu, cov, cov_inv=None, cov_det=None):
        self.m = len(mu)   # Number of dimensions
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

        self.norm = np.sqrt(self.cov_det * (2 * np.pi)**self.m)

    def pdf(self, X, normalize=True, ravel=False):
        """Overly generalized pdf calculator"""
        X = np.asarray(X)

        # Single-point calculation
        if len(X.shape) == 1:
            return self._gauss(X, normalize=normalize)

        n = len(X[0])   # Number of data points

        # Make sure each dimension has the same number of points
        for i in range(1, self.m):
            assert len(X[i]) == n, \
                'row %i with shape %s has different dimension from %s' % (
                i, str(X[i].shape), str(X[0].shape))

        # Get Gaussian output for each point (rank 'self.m' tensor/matrix )
        g = np.zeros(tuple(repeat(n, times=self.m)))
        for i, combination in zip(
                product(range(n), repeat=self.m), product(*X)):
            x = np.array(combination)
            g[i] = self._gauss(x, normalize=normalize)

        # Format
        g = g.T
        if ravel:
            g = g.ravel()

        return g

    def proj_pdf(self, X, which=(0, 1), normalize=True, ravel=False):
        """2D-projected Gaussian pdf...usually for plotting purposes"""
        X = np.asarray(X)

        assert len(X.shape) > 1, \
            "Use 'pdf' function for single-point calculations."
        assert len(which) == 2, \
            "'which' parameter must list 2 dimension indices for projection"
        assert X.shape[0] == 2, \
            "'X' data can only be projected onto 2 dimensions"
        assert len(X[0]) == len(X[1]), \
            "'X' data have different number of points"

        n = len(X[0])   # Number of data points

        g = np.zeros((n, n))
        for i, combination in zip(product(range(n), repeat=2), product(*X)):
            # Create point to plug into Gaussian
            x = np.zeros(self.m)
            for j in range(2):
                x[which[j]] = combination[j]
            # Use means of other dimensions for projection
            for j in range(self.m):
                if j not in which:
                    x[j] = self.mu[j]

            g[i] = self._gauss(x, normalize=normalize)

        # Format
        g = g.T
        if ravel:
            g = g.ravel()

        return g

    def _gauss(self, x, normalize):
        x_mu = x.T - self.mu

        arg = np.matmul(self.cov_inv, x_mu)
        arg = np.matmul(x_mu.T, arg)
        f = np.exp(-0.5 * arg)

        if normalize:
            f /= self.norm

        return f
