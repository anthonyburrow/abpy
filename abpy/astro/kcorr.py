import numpy as np


def kcorr(spec, z, filter1, filter2):
    # spec is the non-redshifted spectrum

    # May need to read response -> interpolate at response wavelength
    # (or maybe more beneficial to GPy response and pickle that for all use)

    m_0 = synth_phot(spec[:, 0], spec[:, 1], filter1, normalize=False)
    m_r = synth_phot(spec[:, 0] * (1. + z), spec[:, 1], filter2, normalize=False)

    K = 2.5 * np.log10(1. + z) + m_0 - m_r

    return K


def synth_phot(wave, flux, filt, normalize=True):
    # Load filter response
    response = None

    # Load zeropoint spectrum/mag for filt
    spec_zp = None
    zp_mag = None   # What the integrated mag is defined as (e.g. B_Vega=0)

    # Calculate zeropoint = -2.5 * integral(T * S_z)
    zp = -2.5 * np.log10(response_int(spec_zp, response, normalize=True)) + zp_mag

    mag = -2.5 * np.log10(response_int(wave, flux, response, normalize=normalize)) + zp

    return mag


def response_int(wave, flux, response, method='trapz', normalize=True):
    integrand = wave * flux * response

    integral = np.trapz(integrand, wave)

    if normalize:
        norm = np.trapz(response, wave)
        integral /= norm
