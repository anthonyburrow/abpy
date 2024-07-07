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

    mask_blue = data_blue[overlap_region[0] <= data_blue[:, 0]]
    mask_red = data_red[data_red[:, 0] <= overlap_region[-1]]

    n_blue = mask_blue.sum()
    n_red = mask_red.sum()

    assert n_blue >= n_needed and n_red >= n_needed, 'Not enough overlap'

    # Scale red to blue
    scale = simps(data_blue[mask_blue, 1], data_blue[mask_blue, 0]) / \
            simps(data_red[mask_red, 1], data_red[mask_red, 0])
    data_red[:, 1] *= scale

    data_blue_overlap = data_blue[mask_blue]
    data_red_overlap = data_red[mask_red]

    wave_blue = data_blue_overlap[:, 0]
    flux_blue = data_blue_overlap[:, 1]
    wave_red = data_red_overlap[:, 0]
    flux_red = data_red_overlap[:, 1]

    spec_out_overlap = np.zeros((n_blue + n_red, 2))

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

    spec_out_overlap[:, 1] = weight_blue * interp_blue(wave_overlap) + \
                             weight_red * interp_red(wave_overlap)

    # Combine arrays
    spec_out = np.concatenate((data_blue[~mask_blue],
                               spec_out_overlap,
                               data_red[~mask_red]))

    return spec_out
