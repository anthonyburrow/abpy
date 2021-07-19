import numpy as np
from os.path import splitext
from astropy.io import fits


def prune(data, wave_range):
    mask = (wave_range[0] <= data[:, 0]) & (data[:, 0] <= wave_range[1])
    return data[mask]


def read_spectrum(filename, z=None, wave_range=None, normalize=False):
    print(f'Reading from {filename}...')
    _, ext = splitext(filename)

    if ext == '.dat':
        data = np.loadtxt(filename)
    elif ext == '.fits':
        hdul = fits.open(filename)
        data = hdul[0].data.T

    # De-reshift and prune based on wavelength range
    if z is not None:
        data[:, 0] /= 1. + z

    # Prune to wavelength range
    if wave_range is not None:
        data = prune(data, wave_range)

    # Normalize
    if normalize:
        max_flux = data[:, 1].max()
        data[:, 1] /= max_flux
        try:
            data[:, 2] = data[:, 2] / max_flux
        except IndexError:
            pass

    return data
