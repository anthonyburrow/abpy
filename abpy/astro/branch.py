import numpy as np
import matplotlib.pyplot as plt
from spextractor import Spextractor
from SNIaDCA import gmm


z = 0.014023
spectrum_file = '../spectra/56647_7.dat'   # Nearest to max light
spextractor_plot = './spextractor.png'
wave_range = (4000., 8000.)


# Fit with spextractor to find Si II pEWs
spex = Spextractor(spectrum_file, z=z, prune_window=wave_range)
spex.create_model(downsampling=3.)
spex.process(plot=True)

si6530 = 'Si II 6150A'
pew6530 = spex.pew[si6530]
pew6530_err = spex.pew_err[si6530]
print(f'pew(6530) = {pew6530:.3f} +- {pew6530_err:.3f}')

si5972 = 'Si II 5800A'
pew5972 = spex.pew[si5972]
pew5972_err = spex.pew_err[si5972]
print(f'pew(5972) = {pew5972:.3f} +- {pew5972_err:.3f}')


# Plot spextractor
fig, ax = spex.plot

plt.tight_layout()
fig.savefig(spextractor_plot, dpi=300)

plt.close('all')


# Predict Branch group
model = gmm(p5=pew5972, p6=pew6530)
probs = model.predict_group(model='p5_p6')
model.get_group_name(probs.squeeze())
