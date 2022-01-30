from numpy import pi
from abpy.util.quantity import Quantity

# SI

# Physics Constants
c = 2.99792458e8               # m s^{-1}
h = 6.62607015e-34             # J s
h_bar = 1.054571817e-34        # J s
k_B = 1.38064852e-23           # m^2 kg s^{-2} K^{-1}
G = 6.67430e-11                # m^3 kg^{-1} s^{-2}
epsilon_0 = 8.8541878128e-12   # F m^{-1}
a_0 = 5.29177210903e-11        # m
e = 1.602176634e-19            # C
m_e = 9.1093837015e-31         # kg
m_p = 1.67262192369e-27        # kg
alpha = e**2 / (4. * pi * epsilon_0 * h_bar * c)


c = Quantity(2.99792458e8, {'m': 1., 's': -1.})
h = Quantity(6.62607015e-34, {'J': 1., 's': 1.})
h_bar = Quantity(1.054571817e-34, {'J': 1., 's': 1.})
k_B = Quantity(1.38064852e-23, {'m': 2., 'kg': 1., 's': -2., 'K': -1.})
G = Quantity(6.67430e-11, {'m': 3., 'kg': -1., 's': -2.})
epsilon_0 = Quantity(8.8541878128e-12, {'F': 1., 'm': -1.})
a_0 = Quantity(5.29177210903e-11, {'m': 1.})
e = Quantity(1.602176634e-19, {'C': 1.})
m_e = Quantity(9.1093837015e-31, {'kg': 1.})
m_p = Quantity(1.67262192369e-27, {'kg': 1.})
alpha = e**2 / (4. * pi * epsilon_0 * h_bar * c)

print(alpha)
