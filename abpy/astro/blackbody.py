import numpy as np
from scipy.optimize import curve_fit
from .const import h, c, k_B
from ..io import read_spectrum


_initial_temp = 1.e4
_initial_scale = 1.e-8



def planck(wave, T):
    ''' Give wave in Angstrom and T in K '''
    if isinstance(wave, float):
        wave = np.array([wave])

    planck = np.zeros_like(wave)

    wave_cm = 1.e-8 * wave   # Angstrom to cm

    factor = np.exp(h * c / (wave_cm * k_B * T))
    mask = factor > 1.    

    planck[mask] = (2.* h * c**2 / wave_cm[mask]**5) / (factor[mask] - 1.)
    planck *= 1.e-8   # To -per Angstrom

    return planck


def scaled_planck(wave, T, scale):
    return scale * planck(wave, T)


def fit(data, init_temp=None, init_scale=None):
    if init_temp is None:
        init_temp = _initial_temp
    if init_scale is None:
        init_scale = _initial_scale

    wave = data[:, 0]
    flux = data[:, 1]
    try:
        flux_err = data[:, 2]
    except IndexError:
        flux_err = 0.05 * flux

    p0 = init_temp, init_scale

    params, pcov = curve_fit(scaled_planck, wave, flux, p0=p0,
                             sigma=flux_err)

    return params
