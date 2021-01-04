import numpy as np
from itertools import product, repeat


class MultiGauss:
    """Generalized multivariate Gaussian object."""

    def __init__(self, mu, cov, cov_inv=None, cov_det=None):
        """Setup distribution.

        Args:
            mu (numpy.ndarray): Means of distribution (m, ).
            cov (numpy.ndarray): Covariance matrix (m, m).
            cov_inv (numpy.ndarray): Inverse of cov. matrix, if already calc'd
                                     (m, m).
            cov_det (numpy.ndarray): Determinant of cov. matrix, if aleady calc'd.

        """
        self.m = len(mu)   # Number of dimensions
        self.mu = np.asarray(mu)
        self.cov = np.asarray(cov)

        if cov_inv is None:
            self.cov_inv = np.linalg.inv(cov)
        else:
            self.cov_inv = cov_inv

        if cov_det is None:
            self.cov_det = np.linalg.det(cov)
        else:
            self.cov_det = cov_det

        self.norm = np.sqrt(self.cov_det * (2 * np.pi)**self.m)

    def pdf(self, X, normalize=True):
        """Calculate PDF in an overly-generalized manner.

        Function takes a set of n points and outputs the PDF of the m-dimensional
        Gaussian distribution.

        Args:
            X (numpy.ndarray): Input data set (n, m).
            normalize (bool): Normalize the PDF.

        Returns:
            g (numpy.ndarray): The array of PDF values (n, ).

        """
        # Single-point calculation
        if isinstance(X, float) or isinstance(X, int):
            return self._gauss_single(X, normalize=normalize)

        X = np.asarray(X)

        if len(X.shape) == 1:
            assert X.shape[0] == self.m, \
                '`X` data point must be of dimension %i' % self.m
            return self._gauss_single(X, normalize=normalize)

        n = X.shape[0]

        # Get Gaussian output for each point
        g = np.zeros(n)
        for i, x in enumerate(X):
            g[i] = self._gauss_single(x, normalize)

        return g

    def pdf_outer(self, X, normalize=True, ravel=False):
        """Calculate PDF of every combination of given points.

        Function takes a set of n points and outputs the PDF of the m-dimensional
        Gaussian distribution for the tensor product of X on itself.

        Args:
            X (numpy.ndarray): Input data set (n, m).
            normalize (bool): Normalize the PDF.
            ravel (bool): Ravel the output.

        Returns:
            g (numpy.ndarray): The array of PDF values (n, n, ...).

        """
        X = np.asarray(X).T

        assert X.shape[0] == self.m, \
            'Use `pdf` for single-point calculations.'

        X_span = np.meshgrid(*X)
        X_span = np.asarray(X_span)
        g = self._gauss(X_span, normalize=normalize)

        if ravel:
            g = g.ravel()

        return g

    def proj_pdf(self, X, which=(0, 1), normalize=True, ravel=False):
        """Calculate PDF projected to 2D slice.

        Calculates the PDF at given points in two dimensions at the mean
        of each other dimension. Usually just used for plotting 2D contours.

        Args:
            X (numpy.ndarray): Input data set (n, 2).
            which (tuple): Which indices of the MultiGauss object correlate to the
                           slice
            normalize (bool): Normalize the PDF.
            ravel (bool): Ravel the output.

        Returns:
            g (numpy.ndarray): The array of PDF values (n, n).

        """
        X = np.asarray(X).T

        assert len(X.shape) > 1, \
            'Use `pdf` function for single-point calculations.'
        assert len(which) == 2, \
            '`which` parameter must list 2 dimension indices for projection'
        assert X.shape[0] == 2, \
            '`X` data can only be projected onto 2 dimensions'

        n = X.shape[1]

        g = np.zeros((n, n))
        for i, combination in zip(product(range(n), repeat=2), product(*X)):
            # Create point to plug into Gaussian
            x = np.zeros(self.m)
            for j in range(self.m):
                if j in which:
                    x[j] = combination[which.index(j)]
                else:
                    # Use mean of other dimensions for projection
                    x[j] = self.mu[j]

            g[i] = self._gauss_single(x, normalize=normalize)

        # Format
        g = g.T
        if ravel:
            g = g.ravel()

        return g

    def _gauss_single(self, x, normalize):
        """Calculate multivariate Gaussian PDF at a single point."""
        x_mu = x.T - self.mu

        arg = np.matmul(self.cov_inv, x_mu)
        arg = np.matmul(x_mu.T, arg)
        f = np.exp(-0.5 * arg)

        if normalize:
            f /= self.norm

        return f

    def _gauss(self, x, normalize):
        """Calculate multivariate Gaussian PDF for entire array."""
        mu_shape = [self.m] + list(repeat(1, self.m))
        x_mu = x - self.mu.reshape(mu_shape)

        arg = np.tensordot(self.cov_inv, x_mu, axes=1)
        arg = np.sum(x_mu * arg, axis=0)

        f = np.exp(-0.5 * arg)

        if normalize:
            f /= self.norm

        return f


def gauss_noCov(X, mu, var, A=None, normalize=False):
    """Return the PDF of a bivariate Gaussian with no covariance.

    Args:
        X (numpy.ndarray): Input data set (n, 2).
        mu (tuple): Means for input space (2, ).
        var (tuple): Variances of each input (2, ).
        A (float): Amplitude of Gaussian.
        normalize (bool): Force normalization.


    Returns:
        g (numpy.ndarray): The array of PDF values (n, ).

    """
    if normalize and A is not None:
        print('Warning: `normalize` set to True will overwrite `A`.')
    if A is None:
        normalize = True
        print('Normalizing Gaussian.')

    X = np.asarray(X)
    mu = np.asarray(mu)
    var = np.asarray(var)

    if normalize:
        A = 1 / (2 * np.pi * np.sqrt(var[0] * var[1]))

    arg = (X - mu)**2 / var
    arg = np.sum(arg, axis=1)
    g = A * np.exp(-0.5 * arg)

    return g
