import numpy as np
import GPy
import time


def regression(x, y, y_err=None, x_pred=None, optimize_noise=False, ls=300,
               var=0.001, noise=0.01, verbose=True):
    """Calculates GPy model for given data.

    Uses GPy to determine a Gaussian process model (Matern32 kernel) based on given
    training data and optimized hyperparameters.  Returns mean and variance
    prediction at input prediction values.

    Args:
        x (ndarray): Input training set.
        y (ndarray): Output training set.
        y_err (ndarray): Uncertainty in y.
        x_pred (ndarray): Input prediction values. Defaults to 'x' parameter, so
                          a change is suggested.
        optimize_noise (ndarray): Optimize single-valued noise parameter.
        ls (float): Starting lengthscale. Defaults to 300 (for astronomy purposes).
        var (float): Starting variance. Defaults to 0.001 (for astronomy purposes).
        noise (float): Starting noise. Defaults to 0.01 (for astronomy purposes).
        verbose (bool): Display printed output.

    Returns:
        mean (ndarray): Prediction of model at given input prediction values.
        variance (ndarray): Variance of model at input pred. values.
        m (GPy.models.GPRegression): Fitted GPy model.
        kernel (GPy.kern): Kernel with optimized hyperparameters.

    """
    kernel = GPy.kern.Matern32(1, lengthscale=ls, variance=var)

    model_uncertainty = False
    if y_err is not None and np.any(y_err):
        model_uncertainty = True
    else:
        optimize_noise = True
        if verbose:
            msg = ('No uncertainty detected - optimizing noise parameter.')
            print(msg)

    # Add flux errors as noise to kernel
    kern = kernel
    if model_uncertainty:
        diag_vars = y_err**2 * np.eye(len(y_err))
        kern_uncertainty = GPy.kern.Fixed(1, diag_vars)
        kern = kernel + kern_uncertainty
        if verbose:
            print('Uncertainty added to GPy kernel')

    # Create model
    m = GPy.models.GPRegression(x[:, np.newaxis], y[:, np.newaxis], kern)
    m['Gaussian.noise.variance'][0] = noise

    if verbose:
        print('Created GP')

    # Optimize model
    if model_uncertainty:
        m['.*fixed.variance'].constrain_fixed()

    if not optimize_noise:
        m.Gaussian_noise.fix(1e-6)

    t0 = time.time()
    m.optimize(optimizer='bfgs')

    if verbose:
        print('Optimised in %.2f s.' % (time.time() - t0))
        print(m)

    # Predict from model
    if model_uncertainty:
        # Use optimized hyperparameters with original kernel
        kernel.lengthscale = kern.Mat32.lengthscale
        kernel.variance = kern.Mat32.variance

    t0 = time.time()

    if x_pred is None:
        x_pred = x
        if verbose:
            print('Predicting at training points')

    mean, var = m.predict(x_pred[:, np.newaxis], kern=kernel.copy())

    if verbose:
        print('Predicted in %.2f s.\n' % (time.time() - t0))

    return mean.squeeze(), var.squeeze(), m, kernel
