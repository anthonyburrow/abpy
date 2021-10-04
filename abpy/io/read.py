import numpy as np
from os.path import splitext
from astropy.io import fits

from ..spectrum import preprocess


def read_spectrum(filename, **kwargs):
    print(f'Reading from {filename}...')
    _, ext = splitext(filename)

    if ext == '.dat':
        data = np.loadtxt(filename)
    elif ext == '.fits':
        hdul = fits.open(filename)
        data = hdul[0].data.T

    data = preprocess(data, **kwargs)

    return data
