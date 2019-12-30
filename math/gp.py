import numpy as np
import GPy
import time


class GPR:
    """Simple single-variable Gaussian process regression.

    Uses GPy to determine a Gaussian process model (Matern32 kernel) based on given
    training data and optimized hyperparameters. Can include uncertainties in
    output.

    """

    def __init__(self, X, Y, eY=None, ls=300, var=0.001, noise=0.01, verbose=True):
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
        if eY is not None and np.any(eY):
            model_uncertainty = True
        else:
            model_uncertainty = False
            optimize_noise = True
            self._report('No uncertainty detected - optimizing noise parameter.')

        # Create kernel
        self.kernel = GPy.kern.Matern32(1, lengthscale=ls, variance=var)

        if model_uncertainty:
            kern_uncertainty = GPy.kern.Fixed(1, np.diag(eY**2))
            kern = self.kernel + kern_uncertainty
            self._report('Uncertainty added to GPy kernel')
        else:
            kern = self.kernel

        # Create model
        self._report('Creating model...')
        self.model = GPy.models.GPRegression(
            X.reshape(-1, 1), Y.reshape(-1, 1), kern)
        self.model['Gaussian.noise.variance'][0] = noise

        # Optimize model
        if model_uncertainty:
            self.model['.*fixed.variance'].constrain_fixed()

        if not optimize_noise:
            self.model.Gaussian_noise.fix(1e-6)

        t0 = time.time()
        self.model.optimize(optimizer='bfgs')

        self._report('Optimised in %.2f s.' % (time.time() - t0))
        self._report(self.model)

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

        self._report('Predicted in %.2f s.\n' % (time.time() - t0))

        mean = mean.squeeze()
        var = var.squeeze()

        return mean, var
