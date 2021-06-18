import numpy as np
from ..astro.redshift import correct_redshift


def preprocess_SNe(data, z=None, wave_range=None):
    '''
    `data` formatted by:
        data[: 0] -> wavelength
        data[: 1] -> flux
        data[: 2] -> flux_err
    '''
    # Put wavelength in rest frame
    data[:, 0] = correct_redshift(data[:, 0], z)

    # Prune to wavelength range
    if wave_range is not None:
        wave_mask = (wave_range[0] < data[:, 0]) & (data[:, 0] < wave_range[1])
        data = data[wave_mask]

    # If there are negatives, adjust flux to make lowest the zeropoint
    if np.any(data[:, 1] < 0):
        min_flux = data[:, 1].min()
        data[:, 1] -= min_flux

    # deredden flux

    return data