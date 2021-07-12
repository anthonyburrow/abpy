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

_zero = 1e-70
_msol = 1.989e33   # grams


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

    file.readline()

    for _ in range(22):
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
            print(symbol)
            continue

        abund = float(line[3][:-1])
        mass_frac = abund_to_n_frac(abund, mass)

        sol_abund.append(mass_frac)
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

    sol_abund[_sym_to_ind['H']] = _zero   # Set the H correction to 0
    sol_abund[_sym_to_ind['He']] = _zero   # Set the He correction to 0

    adjusted_data += sol_frac * sol_abund

    ni56 = model['Ni']

    # Normalize
    norm = adjusted_data.sum(axis=1) + ni56
    adjusted_data = (adjusted_data.T / norm).T
    ni56 /= norm

    return adjusted_data, ni56


def make_plot(data, ni56, v, sol_frac, out_dir='.'):
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


def get_zmass(m_int):
    zmass = np.zeros_like(m_int)

    zmass[0] = m_int[0]   # Assuming m_int starts at 1st boundary
    zmass[1:] = m_int[1:] - m_int[:-1]

    # Ensure it's normalized
    norm = zmass.sum() / m_int[-1]
    zmass /= norm

    # Return zmass
    return zmass * _msol


def interpolate_vel(m_int, v0, v1, m0, m1):
    slope = (v1 - v0) / (m1 - m0)
    return slope * (m_int - m0) + v0


def make_monotonic(vel, m_int):
    n_zones = len(vel)
    for i in range(1, n_zones):
        adjustment = 1.
        if vel[i] == vel[i - 1]:
            vel[i] = vel[i] + adjustment
            continue
        if vel[i] > vel[i - 1]:
            continue
        # Get index j of the next one that is greater/equal in the sequence
        j = i + 1
        while j < n_zones - 1:
            if vel[j] >= vel[i - 1]:
                break
            j += 1
        
        # Fit all between (i-1) and j with linear interpolation of vel v. m_int
        if vel[i - 1] == vel[j]:
            vel[j] = vel[j] + adjustment * 3.
        v0, v1 = vel[i - 1], vel[j]
        m0, m1 = m_int[i - 1], m_int[j]
        vel[i:j] = interpolate_vel(m_int[i:j], v0, v1, m0, m1)


def gen_file(out_file, m_int, vel, adjusted_data, unstable_Ni):
    zmass = get_zmass(m_int)

    nmesh = len(vel)
    out_file.write('%03i\n' % nmesh)

    for i in range(nmesh):
        line = '%03i %.16E %.16E\n' % (i, vel[i], zmass[i])
        out_file.write(line)

    for i in range(nmesh):
        block = ''

        for j in range(0, len(_sym_to_ind), 6):
            vals = tuple(adjusted_data[i, j:j + 5])

            block += '%03i %.16E %.16E %.16E %.16E %.16E' % (i, *vals)

            if j != 78:
                block += ' %.16E' % adjusted_data[i, j + 5]

            block += '\n'

        # Radioactives
        block += '%03i %.16E %.16E %.16E %.16E %.16E %.16E\n' \
                  % (i, unstable_Ni[i], _zero, _zero, _zero, _zero, _zero)

        out_file.write(block)


def gen_model(in_filename, sol_frac, out_dir='.', plot=True):
    # Input
    mass_vel = np.loadtxt(in_filename, skiprows=2, usecols=(0, 2))
    zero_mask = mass_vel == 0
    mass_vel[zero_mask] = _zero

    m_int = mass_vel[:, 0]
    vel = mass_vel[:, 1]
    make_monotonic(vel, m_int)

    adjusted_data, unstable_Ni = get_adjusted(in_filename, sol_frac)

    # Output
    basename = '.'.join(in_filename.split('.')[:-1])
    out_filename = '%s/%s.model' % (out_dir, basename)

    with open(out_filename, 'w+') as out_file:
        gen_file(out_file, m_int, vel, adjusted_data, unstable_Ni)

    if not plot:
        return

    make_plot(adjusted_data, unstable_Ni, vel, sol_frac, out_dir=out_dir)
