import matplotlib as mpl
from cycler import cycler


def paper_plot():
    '''Setup matplotlib rcParams for paper plots.'''
    # Figure
    mpl.rcParams['figure.figsize'] = (6.4, 4.8)
    mpl.rcParams['figure.dpi'] = 400
    mpl.rcParams['figure.autolayout'] = False

    # Axes and Ticks
    tick_fontsize = 12
    tick_major_length = 5
    tick_minor_length = 2.5
    label_fontsize = 13

    mpl.rcParams['axes.labelsize'] = label_fontsize

    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['xtick.top'] = True
    mpl.rcParams['xtick.major.top'] = True
    mpl.rcParams['xtick.minor.top'] = True
    mpl.rcParams['xtick.labelsize'] = tick_fontsize
    mpl.rcParams['xtick.major.size'] = tick_major_length
    mpl.rcParams['xtick.minor.size'] = tick_minor_length

    mpl.rcParams['ytick.direction'] = 'in'
    mpl.rcParams['ytick.right'] = True
    mpl.rcParams['ytick.major.right'] = True
    mpl.rcParams['ytick.minor.right'] = True
    mpl.rcParams['ytick.labelsize'] = tick_fontsize
    mpl.rcParams['ytick.major.size'] = tick_major_length
    mpl.rcParams['ytick.minor.size'] = tick_minor_length

    # Markers and Lines
    mpl.rcParams['scatter.marker'] = 'o'

    mpl.rcParams['lines.linewidth'] = 1
    mpl.rcParams['lines.markersize'] = 3.5
    mpl.rcParams['lines.markeredgewidth'] = 1

    mpl.rcParams['errorbar.capsize'] = 1.5

    colors = [
        '#212121',
        'tab:blue',
        'tab:orange'
    ]
    mpl.rcParams['axes.prop_cycle'] = cycler(color=colors)

    # Legend
    mpl.rcParams['legend.frameon'] = False
    mpl.rcParams['legend.fontsize'] = label_fontsize - 1

    # Fonts
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['mathtext.fontset'] = 'dejavuserif'
