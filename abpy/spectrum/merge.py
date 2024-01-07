'''
Rewrite (with simplification) of:
https://github.com/DeerWhale/BYOST/blob/main/BYOST/merge_spec.py
'''
import numpy as np
from scipy.integrate import simps
from scipy import interpolate


n_needed = 2


def merge_spec(data_blue, data_red, overlap_region=None):
    '''
    Merge bluer and redder spectra, normalize to blue part
    '''
    min_red = data_red[0, 0]
    max_blue = data_blue[-1, 0]

    assert min_red <= max_blue, 'Spectra are disjointed'

    if overlap_region is None:
        overlap_region = min_red, max_blue

    mask_blue = (overlap_region[0] <= data_blue[:, 0]) & (data_blue[:, 0] <= overlap_region[-1])
    mask_red = (overlap_region[0] <= data_red[:, 0]) & (data_red[:, 0] <= overlap_region[-1])

    n_blue = mask_blue.sum()
    n_red = mask_red.sum()

    assert n_blue >= n_needed and n_red >= n_needed, 'Not enough overlap'

    # Make room for errors
    if data_blue.shape[1] == 2:
        _data_blue = np.hstack((data_blue, np.zeros((len(data_blue), 1))))
    else:
        _data_blue = data_blue

    if data_red.shape[1] == 2:
        _data_red = np.hstack((data_red, np.zeros((len(data_red), 1))))
    else:
        _data_red = data_red

    # Scale red to blue
    scale = simps(_data_blue[mask_blue, 1], _data_blue[mask_blue, 0]) / \
            simps(_data_red[mask_red, 1], _data_red[mask_red, 0])

    _data_red[:, 1] *= scale
    _data_red[:, 2] *= scale

    data_blue_overlap = _data_blue[mask_blue]
    data_red_overlap = _data_red[mask_red]

    wave_blue = data_blue_overlap[:, 0]
    flux_blue = data_blue_overlap[:, 1]
    var_blue = data_blue_overlap[:, 2]**2

    wave_red = data_red_overlap[:, 0]
    flux_red = data_red_overlap[:, 1]
    var_red = data_red_overlap[:, 2]**2

    spec_out_overlap = np.zeros((n_blue + n_red, 3))

    spec_out_overlap[:, 0] = np.concatenate((wave_blue, wave_red))
    spec_out_overlap[:, 0] = np.unique(spec_out_overlap[:, 0])
    wave_overlap = spec_out_overlap[:, 0]

    # Interpolate each and do weighted average
    total_overlap = wave_overlap[-1] - wave_overlap[0]
    weight_blue = (wave_overlap - wave_overlap[0]) / total_overlap
    weight_red = 1. - weight_blue   # Sum of weights = 1

    interp_blue = interpolate.interp1d(wave_blue, flux_blue,
                                       fill_value='extrapolate')
    interp_red = interpolate.interp1d(wave_red, flux_red,
                                      fill_value='extrapolate')

    interp_blue_var = interpolate.interp1d(wave_blue, var_blue,
                                           fill_value='extrapolate')
    interp_red_var = interpolate.interp1d(wave_red, var_red,
                                          fill_value='extrapolate')

    spec_out_overlap[:, 1] = weight_blue * interp_blue(wave_overlap) + \
                             weight_red * interp_red(wave_overlap)
    spec_out_overlap[:, 2] = weight_blue * interp_blue_var(wave_overlap) + \
                             weight_red * interp_red_var(wave_overlap)
    spec_out_overlap[:, 2] = np.sqrt(spec_out_overlap[:, 2])

    # Combine arrays
    spec_out = np.concatenate((_data_blue[data_blue[:, 0] < overlap_region[0]],
                               spec_out_overlap,
                               _data_red[overlap_region[-1] < data_red[:, 0]]))

    return spec_out
