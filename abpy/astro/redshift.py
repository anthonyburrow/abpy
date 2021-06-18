
def correct_redshift(array, z):
    ''' Put some array into rest frame.

    Array could be wavelength, epoch, etc.
    '''
    if z is None:
        return

    return array / (z + 1.)