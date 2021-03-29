import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
from pathlib import Path


_sep = os.sep

_parent_path = Path(__file__).parent
_atomic_filename = '%s%sdata%sagabund.f' % (_parent_path, _sep, _sep)
_sol_filename = '%s%sdata%slatest_solar.dat' % (_parent_path, _sep, _sep)

_sym_to_ind = {}
_model_sym = ('He', 'C', 'O', 'Ne', 'Mg', 'Si',
              'S', 'Ar', 'Ca', 'Fe', 'Ni', 'Zn')

_neglect = ('H', 'He')

_H_frac = 0.7381
_H_mass = 1.0079


def read_atomic_mass(file):
    for _ in range(208):
        file.readline()

    atomic_mass = {}

    for _ in range(89):
        line = file.readline().split(',')

        mass = float(line[2].replace(" ", ''))

        symbol = line[3]
        symbol = symbol.replace(" ", '')
        symbol = symbol.replace("'", '')

        atomic_mass[symbol] = mass

    return atomic_mass


def abund_to_n_frac(z, amu):
    return amu * 10**(z - 12)


def read_sol(file, atomic_mass):
    for _ in range(7):
        file.readline()

    sol_abund = []

    count = 0
    for _ in range(83):
        line = file.readline().split()

        symbol = line[7]
        symbol = symbol.split("'")[0]
        symbol = symbol.split()[0]

        try:
            mass = atomic_mass[symbol]
        except KeyError:
            continue

        abund = float(line[3][:-1])
        mass_frac = abund_to_n_frac(abund, mass)

        sol_abund.append(mass_frac)
        if symbol == 'H':
            continue
        _sym_to_ind[symbol] = count
        count += 1

    sol_abund = np.array(sol_abund)

    # Normalize to sum to 1 (fixes the unknown constants)
    sol_abund /= sol_abund.sum()

    return sol_abund


def read_model(filename):
    cols = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
    dtype = [(elem, np.float64) for elem in _model_sym]

    data = np.loadtxt(filename, skiprows=2, usecols=cols, dtype=dtype)

    return data


def get_adjusted(model_filename, sol_frac):
    # Read from files
    with open(_atomic_filename) as F:
        atomic_mass = read_atomic_mass(F)

    with open(_sol_filename) as F:
        sol_abund = read_sol(F, atomic_mass)

    model = read_model(model_filename)

    # Create adjusted array
    adjusted_data = np.zeros((model.shape[0], len(_sym_to_ind)))

    for elem in _model_sym:
        if elem == 'Ni':
            continue
        i = _sym_to_ind[elem]
        adjusted_data[:, i] = model[elem]

    sol_abund[_sym_to_ind['He'] + 1] = 0   # Set the He correction to 0

    adjusted_data += sol_frac * sol_abund[_sym_to_ind['He'] + 1:]

    ni56 = model['Ni']

    # Normalize
    norm = adjusted_data.sum(axis=1) + ni56
    adjusted_data = (adjusted_data.T / norm).T
    ni56 /= norm

    return adjusted_data, ni56


def plot(data, ni56, v, sol_frac, out_dir='.'):
    fig, ax = plt.subplots(figsize=(5, 3), dpi=200)

    for elem in _model_sym:
        y = data[:, _sym_to_ind[elem]]
        if elem == 'Ni':
            ax.plot(v, y + ni56, label=elem)
        else:
            ax.plot(v, y, label=elem)

    ax.set_ylim(1e-12, 1)
    ax.set_yscale('log')

    ax.set_xlabel('velocity')
    ax.set_ylabel('mass fraction')

    ax.legend(frameon=False, bbox_to_anchor=(1.04, 1), loc='upper left',
              fontsize=9)

    plt.tight_layout()

    # Save image
    fig_dir = '%s%sfigs' % (out_dir, _sep)
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)

    fn = '%s%scomps-%.3e.png' % (fig_dir, _sep, sol_frac)
    fig.savefig(fn, format='png', dpi=200)

    plt.close('all')
