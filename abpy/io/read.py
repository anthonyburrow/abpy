from os.path import splitext
from astropy.io import fits


def read_spectrum(filename):
    root, ext = splitext(filename)

    if ext == '.dat':
        data = np.loadtxt(filename)
    elif ext == '.fits':
        hdul = fits.open(filename)
        data = hdul[0].data.T

    return data