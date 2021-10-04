import numpy as np
from ..astro.redshift import deredshift
from snpy.utils.deredden import unred


MW_RV = 3.1


def prune(data, wave_range):
    mask = (wave_range[0] <= data[:, 0]) & (data[:, 0] <= wave_range[1])
    return data[mask]


def scale_flux(data, flux_range=(0, 1)):
    '''
    `data` formatted by:
        data[: 0] -> wavelength
        data[: 1] -> flux
        data[: 2] -> flux_err
    '''
    _min, _max = flux_range

    min_flux = data[:, 1].min()
    max_flux = data[:, 1].max()

    data[:, 1] = (data[:, 1] - min_flux) / (max_flux - min_flux)
    data[:, 1] = data[:, 1] * (_max - _min) + _min

    try:
        data[:, 2] *= (_max - _min) / (max_flux - min_flux)
    except IndexError:
        pass

    return data


def normalize_flux(data):
    '''
    `data` formatted by:
        data[: 0] -> wavelength
        data[: 1] -> flux
        data[: 2] -> flux_err
    '''
    max_flux = data[:, 1].max()
    data[:, 1] /= max_flux

    try:
        data[:, 2] /= max_flux
    except IndexError:
        pass

    return data


def preprocess(data, z=None, wave_range=None, normalize=False, scale=False,
               E_BV=None):
    '''
    `data` formatted by:
        data[: 0] -> wavelength
        data[: 1] -> flux
        data[: 2] -> flux_err
    '''
    # Get rid of NaN values
    data = data[~np.isnan(data).any(axis=1)]

    # Put wavelength in rest frame
    data[:, 0] = deredshift(data[:, 0], z)

    # Prune to wavelength range
    if wave_range is not None:
        data = prune(data, wave_range)

    # Correct for MW reddening
    if E_BV is not None:
        data[:, 1], _, _0 = unred(data[:, 0], data[:, 1], E_BV, MW_RV)

    if scale:
        data = scale_flux(data)
    elif normalize:
        data = normalize_flux(data)

    return data