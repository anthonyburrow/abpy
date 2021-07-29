
def deredshift(array, z):
    ''' Put some array into rest frame.

    Array could be wavelength, epoch, etc.
    '''
    if z is None:
        return array

    return array / (z + 1.)