import numpy as np
import GPy
import time


class GPR:
    """Simple single-variable Gaussian process regression.

    Uses GPy to determine a Gaussian process model (Matern32 kernel) based on given
    training data and optimized hyperparameters. Can include uncertainties in
    output.

    """

    def __init__(self, X, y, ey=None, ls=1., var=0.001, noise=0.01,
                 verbose=False, optimize_noise=False, optimizer='bfgs'):
        """Create optimized model.

        Args:
            X (numpy.ndarray): Input of training set.
            Y (numpy.ndarray): Output of training set.
            eY (numpy.ndarray): Uncertainty in output.
            ls (float): Starting length-scale for kernel.
            var (float): Starting variance for kernel.
            noise (float): Starting noise for kernel.
            verbose (bool): Display print messages.

        """
        self.verbose = verbose

        # Check for uncertainties
        model_uncertainty = False
        if ey is not None and np.any(ey):
            model_uncertainty = True
        else:
            optimize_noise = True
            msg = ('No uncertainty detected - optimizing noise parameter.')
            self._report(msg)

        # Create kernel
        self.kernel = GPy.kern.Matern32(1, lengthscale=ls, variance=var)

        kern = self.kernel
        if model_uncertainty:
            kern_uncertainty = GPy.kern.Fixed(1, np.diag(ey**2))
            kern += kern_uncertainty

            msg = 'Uncertainty added to GPy kernel'
            self._report(msg)

        # Create model
        self.model = GPy.models.GPRegression(
            X[:, np.newaxis], y[:, np.newaxis], kern)
        self.model['Gaussian.noise.variance'][0] = noise

        # Optimize model
        if model_uncertainty:
            self.model['.*fixed.variance'].constrain_fixed()

        if not optimize_noise:
            self.model.Gaussian_noise.fix(1e-6)

        t0 = time.time()
        self.model.optimize(optimizer=optimizer)

        msg = f'Optimised in {time.time() - t0:.2f} s.'
        self._report(msg)

        if model_uncertainty:
            # Use optimized hyperparameters with original kernel
            self.kernel.lengthscale = kern.Mat32.lengthscale
            self.kernel.variance = kern.Mat32.variance

    def _report(self, msg):
        """Display print messages."""
        if self.verbose:
            print(msg)

    def predict(self, X_pred):
        """Predict at given input values using regression.

        Args:
            X_pred (numpy.ndarray): Input prediction values.

        Returns:
            mean (numpy.ndarray): Mean of regression at each point.
            var (numpy.ndarray): Variance of regression at each point.

        """
        t0 = time.time()
        mean, var = self.model.predict(
            X_pred.reshape(-1, 1), kern=self.kernel.copy())

        msg = f'Predicted in {time.time() - t0:.2f} s.'
        self._report(msg)

        return mean.squeeze(), var.squeeze()
