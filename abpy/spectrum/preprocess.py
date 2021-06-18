from ..astro.redshift import redshift_correct


def preprocess_SNe(data, z=None):
    '''
    `data` formatted by:
        data[: 0] -> wavelength
        data[: 1] -> flux
        data[: 2] -> flux_err
    '''
    # Put wavelength in rest frame
    data[:, 0] = redshift_correct(data[:, 0], z)

    # If there are negatives, adjust flux to make lowest the zeropoint
    if np.any(data[:, 1] < 0):
        data[:, 1] -= data[:, 1].min()

    # deredden flux

    return data