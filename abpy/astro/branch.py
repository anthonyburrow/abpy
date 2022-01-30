import numpy as np
import matplotlib.pyplot as plt
from spextractor import Spextractor
from SNIaDCA import gmm

from ..plot.setup import paper_plot


si6530 = 'Si II 6150A'
si5972 = 'Si II 5800A'


def get_branch_props(data):
    # Fit with spextractor to find Si II pEWs
    spex = Spextractor(data)
    spex.create_model(downsampling=3.)
    spex.process()

    branch_props = {} 

    branch_props['p6150'] = (spex.pew[si6530], spex.pew_err[si6530])
    branch_props['p5800'] = (spex.pew[si5972], spex.pew_err[si5972])
    branch_props['v6150'] = (spex.vel[si6530], spex.vel_err[si6530])

    return branch_props


def make_branch_plot(data, background_data, out_filename: str = None,
                     label='', bg_label='', *args, **kwargs):
    if out_filename is None:
        out_filename = './branch_diagram.pdf'

    branch_props = get_branch_props(data, *args, **kwargs)

    p6, p6_err = branch_props['p6150']
    p5, p5_err = branch_props['p5800']

    bg_p5 = background_data['p5800']
    bg_p5_err = background_data['p5800_err']
    bg_p6 = background_data['p6150']
    bg_p6_err = background_data['p6150_err']

    # Plot
    paper_plot()

    fig, ax = plt.subplots()

    ax.plot(bg_p6, bg_p5, 'o', label=bg_label)
    ax.errorbar(bg_p6, bg_p5, xerr=bg_p6_err, yerr=bg_p5_err, fmt='none')

    ax.errorbar(p6, p5, xerr=p6_err, yerr=p5_err, fmt='none', c='red')
    ax.plot(p6, p5, '*', ms=14, c='red', mec='k', label=label)

    ax.set_xlabel(r'$\mathrm{Si\ II\ \lambda 6355\ pEW\ [Å]}$')
    ax.set_ylabel(r'$\mathrm{Si\ II\ \lambda 5972\ pEW\ [Å]}$')

    ax.legend()

    plt.tight_layout()
    fig.savefig(out_filename, format='pdf')

    plt.close('all')
