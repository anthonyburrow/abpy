'''
EXTENDED FROM https://github.com/DeerWhale/BYOST/BYOST/merge_spec.py
ORIG: Eric's IDL EYH_MERGE_SPEC
'''
import numpy as np
from scipy import interpolate
from scipy.integrate import simps


def merge_spec(data_b, data_r, interp_option=0.,
               normalize=None, plot_ax=None, return_norm=False):
    '''
    Merge spectra with weighted average at overlap.

    Input:
        data_b: Blue side spectrum
        data_r: Red side spectrum
        interp_option=0: wavelength grid interp, 0 as default combine the wavelength points in the overlapped region
        normalize: how flux is normalized when merging
                'blue_side'  match the flux of red spectrum to blue side in the overlapped region;
                'red_side':  match the flux of blue spectrum  to the red spectrum in the overlapped region;
        plot_ax: default None as no plot output, if given ax then will plot the spectra before and after the merging process.

    Output:
        tuple: merged_wavelength, merged_flux
    '''
    wave_b = data_b[:, 0]
    flux_b = data_b[:, 1]
    if data_b.shape[1] > 2:
        err_b = data_b[:, 2]
    else:
        err_b = np.zeros_like(flux_b)

    wave_r = data_r[:, 0]
    flux_r = data_r[:, 1]
    if data_r.shape[1] > 2:
        err_r = data_r[:, 2]
    else:
        err_r = np.zeros_like(flux_r)

    weight_lo = 0.
    w1 = np.where(wave_b >= min(wave_r))[0]
    w2 = np.where(wave_r <= max(wave_b))[0]
    if (len(w1) < 2) or (len(w2) < 2):
        print('WARNING! Not enough overlap')
        return
    else:
        # Decide what wavelegnth to use in the overlap region
        if interp_option == 0:   # combine the overlap wavelengths
            wave_overlap = np.concatenate([wave_b[w1], wave_r[w2]], axis=0)
            wave_overlap = np.sort(wave_overlap)
            wave_overlap = np.unique(wave_overlap)
        elif interp_option == 1:
            wave_overlap = wave_b[w1]
        elif interp_option == 2:
            wave_overlap = wave_r[w2]

        # Decide how to normalize
        if normalize is None or normalize == 'blue_side':
            # match the overlapping region flux based on the blue side
            norm_b = 1
            norm_r = simps(flux_b[w1], wave_b[w1]) / simps(flux_r[w2], wave_r[w2])
        elif normalize == 'red_side':
            norm_b = simps(flux_r[w2], wave_r[w2]) / simps(flux_b[w1], wave_b[w1])
            norm_r = 1
        else:
            # let the spectra merge by weight, smooothly merging together
            norm_b, norm_r = 1, 1

        # Inteplate the flux in overlapping region
        x = [min(wave_overlap), max(wave_overlap)]
        f1 = interpolate.interp1d(x, [1., weight_lo])
        f2 = interpolate.interp1d(x, [weight_lo, 1.])
        weight1 = f1(wave_overlap)
        weight2 = f2(wave_overlap)
        weight_sum = weight1 + weight2

        # Flux
        f1_f = interpolate.interp1d(wave_b[w1], norm_b * flux_b[w1],
                                    fill_value='extrapolate')
        f2_f = interpolate.interp1d(wave_r[w2], norm_r * flux_r[w2],
                                    fill_value='extrapolate')
        flux_ol = (f1_f(wave_overlap) * weight1 + f2_f(wave_overlap) * weight2) / weight_sum

        # Flux errors (linearly interpolate the variances)
        f1_f = interpolate.interp1d(wave_b[w1], (norm_b * err_b[w1])**2,
                                    fill_value='extrapolate')
        f2_f = interpolate.interp1d(wave_r[w2], (norm_r * err_r[w2])**2,
                                    fill_value='extrapolate')
        var_ol = (f1_f(wave_overlap) * weight1 + f2_f(wave_overlap) * weight2) / weight_sum
        err_ol = np.sqrt(var_ol)

        # Now combine the flux
        w1_rest = np.where(wave_b < min(wave_r))[0]
        w2_rest = np.where(wave_r > max(wave_b))[0]
        wave_out = np.concatenate([wave_b[w1_rest],
                                   wave_overlap,
                                   wave_r[w2_rest]], axis=0)
        flux_out = np.concatenate([norm_b * flux_b[w1_rest],
                                   flux_ol,
                                   norm_r * flux_r[w2_rest]], axis=0)
        err_out = np.concatenate([norm_b * err_b[w1_rest],
                                  err_ol,
                                  norm_r * err_r[w2_rest]], axis=0)

        data_out = np.c_[wave_out, flux_out, err_out]

        if return_norm:
            return data_out, norm_b, norm_r

        return data_out


def merge_spec2(data_b, data_r, overlap=None, *args, **kwargs):
    if overlap is None:
        return merge_spec(data_b, data_r, *args, **kwargs)

    mask_blue = data_b[:, 0] < overlap[-1]
    mask_red = overlap[0] < data_r[:, 0]

    return merge_spec(data_b[mask_blue], data_r[mask_red], *args, **kwargs)
