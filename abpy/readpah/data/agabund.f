c
c
c
      module AGabund
c     -------------------
cALLOC-ON      use atomsmod_param    !ALLOC-ON
cALLOC-ON      use atomsmod_real    !ALLOC-ON
cALLOC-ON      use atomsmod_integer    !ALLOC-ON
cALLOC-ON      use atomsmod_character    !ALLOC-ON
cALLOC-ON      use atomsmod_scalar    !ALLOC-ON
      implicit none
************************************************************************
*  Abundances of Anders & Grevesse as listed in Jaschek+Jaschek enlarged
* 18/Mar/2006 by PHH
* Added Asplund, Grevesse, & Sauval Cosmic Abundances
* as Records of Stellar Evolution and Nucleosynthesis in honor of David
* L. Lambert, ASP Conference Series, Vol. 336, Proceedings of a
* symposium held 17-19 June, 2004 in Austin, Texas. Edited by Thomas
* G. Barnes III and Frank N. Bash. San Francisco: Astronomical Society
* of the Pacific, 2005., p.25
************************************************************************
      integer :: fnome(100),nome_AGS(100)
      real*8 :: feheu(100),eheu_AGS(100)
      integer, private :: i
      integer, parameter :: z_max=111
      integer      :: el_code(z_max)
      real*8       :: elmass(z_max)
      character*2  :: elsymbol(z_max)
      character*16 :: elname(z_max)
c
c
      data (fnome(i), feheu(i), i=1,84) /
     &    100,           12.00d0  !  H, solar
     &,   200,           10.99d0  ! He, solar
     &,   300,            1.16d0  ! Li, solar
     &,   400,            1.15d0  ! Be, solar
     &,   500,            2.60d0  !  B, solar
     &,   600,            8.55d0  !  C, solar
     &,   700,            7.97d0  !  N, solar
     &,   800,            8.87d0  !  O, solar
     &,   900,            4.56d0  !  F, solar
     &,  1000,            8.09d0  ! Ne, solar
     &,  1100,            6.33d0  ! Na, solar
     &,  1200,            7.58d0  ! Mg, solar
     &,  1300,            6.47d0  ! Al, solar
     &,  1400,            7.55d0  ! Si, solar
     &,  1500,            5.45d0  !  P, solar
     &,  1600,            7.21d0  !  S, solar
     &,  1700,            5.50d0  ! Cl, solar
     &,  1800,            6.52d0  ! Ar, solar
     &,  1900,            5.12d0  !  K, solar
     &,  2000,            6.36d0  ! Ca, solar
     &,  2100,            3.17d0  ! Sc, solar
     &,  2200,            5.02d0  ! Ti, solar
     &,  2300,            4.00d0  !  V, solar
     &,  2400,            5.67d0  ! Cr, solar
     &,  2500,            5.39d0  ! Mn, solar
     &,  2600,            7.50d0  ! Fe, solar
     &,  2700,            4.92d0  ! Co, solar
     &,  2800,            6.25d0  ! Ni, solar
     &,  2900,            4.21d0  ! Cu, solar
     &,  3000,            4.60d0  ! Zn, solar
     &,  3100,            2.88d0  ! Ga, solar
     &,  3200,            3.41d0  ! Ge, solar
     &,  3300,            2.37d0  ! As, meteor.
     &,  3400,            3.35d0  ! Se, meteor.
     &,  3500,            2.63d0  ! Br, meteor.
     &,  3600,            3.23d0  ! Kr, meteor.
     &,  3700,            2.60d0  ! Rb, solar
     &,  3800,            2.90d0  ! Sr, solar
     &,  3900,            2.24d0  !  Y, solar
     &,  4000,            2.60d0  ! Zr, solar
     &,  4100,            1.42d0  ! Nb, solar
     &,  4200,            1.92d0  ! Mo, solar
!     &,  4300,          -99.00d0  ! Tc, unknown
     &,  4400,            1.84d0  ! Ru, solar
     &,  4500,            1.12d0  ! Rh, solar
     &,  4600,            1.69d0  ! Pd, solar
     &,  4700,            1.24d0  ! Ag, meteor.
     &,  4800,            1.77d0  ! Cd, solar
     &,  4900,            0.82d0  ! In, solar
     &,  5000,            2.00d0  ! Sn, solar
     &,  5100,            1.00d0  ! Sb, solar
     &,  5200,            2.24d0  ! Te, meteor.
     &,  5300,            1.51d0  !  I, meteor.
     &,  5400,            2.23d0  ! Xe, meteor.
     &,  5500,            1.12d0  ! Cs, meteor.
     &,  5600,            2.13d0  ! Ba, solar
     &,  5700,            1.22d0  ! La, solar
     &,  5800,            1.55d0  ! Ce, solar
     &,  5900,            0.71d0  ! Pr, solar
     &,  6000,            1.50d0  ! Nd, solar
!     &,  6100,          -99.00d0  ! Pm, unknown
     &,  6200,            1.01d0  ! Sm, solar
     &,  6300,            0.51d0  ! Eu, solar
     &,  6400,            1.12d0  ! Gd, solar
     &,  6500,            0.33d0  ! Tb, meteor.
     &,  6600,            1.14d0  ! Dy, solar
     &,  6700,            0.50d0  ! Ho, meteor.
     &,  6800,            0.93d0  ! Er, solar
     &,  6900,            0.13d0  ! Tm, meteor.
     &,  7000,            1.08d0  ! Yb, solar
     &,  7100,            0.12d0  ! Lu, meteor.
     &,  7200,            0.88d0  ! Hf, solar
     &,  7300,            0.13d0  ! Ta, meteor.
     &,  7400,            0.68d0  !  W, meteor.
     &,  7500,            0.27d0  ! Re, meteor.
     &,  7600,            1.45d0  ! Os, solar
     &,  7700,            1.35d0  ! Ir, solar
     &,  7800,            1.80d0  ! Pt, solar
     &,  7900,            0.83d0  ! Au, meteor.
     &,  8000,            1.09d0  ! Hg, meteor.
     &,  8100,            0.82d0  ! Tl, meteor.
     &,  8200,            1.95d0  ! Pb, solar
     &,  8300,            0.71d0  ! Bi, meteor.
     &,  9000,            0.08d0  ! Th, meteor.
     &,  9200,            0.49d0  !  U, meteor.
     &,     0,         -999.00d0/
c
      data (nome_AGS(i),eheu_AGS(i), i=1,84) /
     &  100,             12.00d0  !  H, solar
     &, 200,             10.93d0  ! He, solar
     &, 300,              1.05d0  ! Li, solar
     &, 400,              1.38d0  ! Be, solar
     &, 500,              2.70d0  !  B, solar
     &, 600,              8.39d0  !  C, solar
     &, 700,              7.78d0  !  N, solar
     &, 800,              8.66d0  !  O, solar
     &, 900,              4.56d0  !  F, solar
     &,1000,              7.84d0  ! Ne, solar
     &,1100,              6.17d0  ! Na, solar
     &,1200,              7.53d0  ! Mg, solar
     &,1300,              6.37d0  ! Al, solar
     &,1400,              7.51d0  ! Si, solar
     &,1500,              5.36d0  !  P, solar
     &,1600,              7.14d0  !  S, solar
     &,1700,              5.50d0  ! Cl, solar
     &,1800,              6.18d0  ! Ar, solar
     &,1900,              5.08d0  !  K, solar
     &,2000,              6.31d0  ! Ca, solar
     &,2100,              3.05d0  ! Sc, solar
     &,2200,              4.90d0  ! Ti, solar
     &,2300,              4.00d0  !  V, solar
     &,2400,              5.64d0  ! Cr, solar
     &,2500,              5.39d0  ! Mn, solar
     &,2600,              7.45d0  ! Fe, solar
     &,2700,              4.92d0  ! Co, solar
     &,2800,              6.23d0  ! Ni, solar
     &,2900,              4.21d0  ! Cu, solar
     &,3000,              4.60d0  ! Zn, solar
     &,3100,              2.88d0  ! Ga, solar
     &,3200,              3.58d0  ! Ge, solar
     &,3300,              2.29d0  ! As, meteor.
     &,3400,              3.33d0  ! Se, meteor.
     &,3500,              2.56d0  ! Br, meteor.
     &,3600,              3.28d0  ! Kr, meteor.
     &,3700,              2.60d0  ! Rb, solar
     &,3800,              2.92d0  ! Sr, solar
     &,3900,              2.21d0  !  Y, solar
     &,4000,              2.59d0  ! Zr, solar
     &,4100,              1.42d0  ! Nb, solar
     &,4200,              1.92d0  ! Mo, solar
!    &,4300,            -99.00d0  ! Tc, unknown
     &,4400,              1.84d0  ! Ru, solar
     &,4500,              1.12d0  ! Rh, solar
     &,4600,              1.69d0  ! Pd, solar
     &,4700,              0.94d0  ! Ag, meteor.
     &,4800,              1.77d0  ! Cd, solar
     &,4900,              1.60d0  ! In, solar
     &,5000,              2.00d0  ! Sn, solar
     &,5100,              1.00d0  ! Sb, solar
     &,5200,              2.19d0  ! Te, meteor.
     &,5300,              1.51d0  !  I, meteor.
     &,5400,              2.27d0  ! Xe, meteor.
     &,5500,              1.07d0  ! Cs, meteor.
     &,5600,              2.17d0  ! Ba, solar
     &,5700,              1.13d0  ! La, solar
     &,5800,              1.58d0  ! Ce, solar
     &,5900,              0.71d0  ! Pr, solar
     &,6000,              1.45d0  ! Nd, solar
!    &,6100,            -99.00d0  ! Pm, unknown
     &,6200,              1.01d0  ! Sm, solar
     &,6300,              0.52d0  ! Eu, solar
     &,6400,              1.12d0  ! Gd, solar
     &,6500,              0.28d0  ! Tb, meteor.
     &,6600,              1.14d0  ! Dy, solar
     &,6700,              0.51d0  ! Ho, meteor.
     &,6800,              0.93d0  ! Er, solar
     &,6900,              0.00d0  ! Tm, meteor.
     &,7000,              1.08d0  ! Yb, solar
     &,7100,              0.06d0  ! Lu, meteor.
     &,7200,              0.88d0  ! Hf, solar
     &,7300,             -0.17d0  ! Ta, meteor.
     &,7400,              1.11d0  !  W, meteor.
     &,7500,              0.23d0  ! Re, meteor.
     &,7600,              1.45d0  ! Os, solar
     &,7700,              1.38d0  ! Ir, solar
     &,7800,              1.64d0  ! Pt, solar
     &,7900,              1.01d0  ! Au, meteor.
     &,8000,              1.13d0  ! Hg, meteor.
     &,8100,              0.90d0  ! Tl, meteor.
     &,8200,              2.00d0  ! Pb, solar
     &,8300,              0.65d0  ! Bi, meteor.
     &,9000,              0.06d0  ! Th, meteor.
     &,9200,             -0.52d0  !  U, meteor.
     &,     0,         -999.00d0/
c
      data (el_code(i),elmass(i),elsymbol(i),elname(i), i=1,89)/
     &,    100,   1.0079, 'H ', 'Hydrogen'
     &,    200,   4.0026, 'He', 'Helium'
     &,    300,   6.941,  'Li', 'Lithium'
     &,    400,   9.0122, 'Be', 'Beryllium'
     &,    500,  10.811,  'B ', 'Boron'
     &,    600,  12.0107, 'C ', 'Carbon'
     &,    700,  14.0067, 'N ', 'Nitrogen'
     &,    800,  15.9994, 'O ', 'Oxygen'
     &,    900,  18.9984, 'F ', 'Fluorine'
     &,   1000,  20.1797, 'Ne', 'Neon'
     &,   1100,  22.9897, 'Na', 'Sodium'
     &,   1200,  24.305,  'Mg', 'Magnesium'
     &,   1300,  26.9815, 'Al', 'Aluminum'
     &,   1400,  28.0855, 'Si', 'Silicon'
     &,   1500,  30.9738, 'P ', 'Phosphorus'
     &,   1600,  32.065,  'S ', 'Sulfur'
     &,   1700,  35.453,  'Cl', 'Chlorine'
     &,   1800,  39.948,  'Ar', 'Argon'
     &,   1900,  39.0983, 'K ', 'Potassium'
     &,   2000,  40.078,  'Ca', 'Calcium'
     &,   2100,  44.9559, 'Sc', 'Scandium'
     &,   2200,  47.867,  'Ti', 'Titanium'
     &,   2300,  50.9415, 'V,', 'anadium'
     &,   2400,  51.9961, 'Cr', 'Chromium'
     &,   2500,  54.938,  'Mn', 'Manganese'
     &,   2600,  55.845,  'Fe', 'Iron'
     &,   2700,  58.9332, 'Co', 'Cobalt'
     &,   2800,  58.6934, 'Ni', 'Nickel'
     &,   2900,  63.546,  'Cu', 'Copper'
     &,   3000,  65.39,   'Zn', 'Zinc'
     &,   3100,  69.723,  'Ga', 'Gallium'
     &,   3200,  72.64,   'Ge', 'Germanium'
     &,   3300,  74.9216, 'As', 'Arsenic'
     &,   3400,  78.96,   'Se', 'Selenium'
     &,   3500,  79.904,  'Br', 'Bromine'
     &,   3600,  83.8,    'Kr', 'Krypton'
     &,   3700,  85.4678, 'Rb', 'Rubidium'
     &,   3800,  87.62,   'Sr', 'Strontium'
     &,   3900,  88.9059, 'Y ', 'Yttrium'
     &,   4000,  91.224,  'Zr', 'Zirconium'
     &,   4100,  92.9064, 'Nb', 'Niobium'
     &,   4200,  95.94,   'Mo', 'Molybdenum'
     &,   4300,  98,      'Tc', 'Technetium'
     &,   4400, 101.07,   'Ru', 'Ruthenium'
     &,   4500, 102.9055, 'Rh', 'Rhodium'
     &,   4600, 106.42,   'Pd', 'Palladium'
     &,   4700, 107.8682, 'Ag', 'Silver'
     &,   4800, 112.411,  'Cd', 'Cadmium'
     &,   4900, 114.818,  'In', 'Indium'
     &,   5000, 118.71,   'Sn', 'Tin'
     &,   5100, 121.76,   'Sb', 'Antimony'
     &,   5200, 127.6,    'Te', 'Tellurium'
     &,   5300, 126.9045, 'I ', 'Iodine'
     &,   5400, 131.293,  'Xe', 'Xenon'
     &,   5500, 132.9055, 'Cs', 'Cesium'
     &,   5600, 137.327,  'Ba', 'Barium'
     &,   5700, 138.9055, 'La', 'Lanthanum'
     &,   5800, 140.116,  'Ce', 'Cerium'
     &,   5900, 140.9077, 'Pr', 'Praseodymium'
     &,   6000, 144.24,   'Nd', 'Neodymium'
     &,   6100, 145,      'Pm', 'Promethium'
     &,   6200, 150.36,   'Sm', 'Samarium'
     &,   6300, 151.964,  'Eu', 'Europium'
     &,   6400, 157.25,   'Gd', 'Gadolinium'
     &,   6500, 158.9253, 'Tb', 'Terbium'
     &,   6600, 162.5,    'Dy', 'Dysprosium'
     &,   6700, 164.9303, 'Ho', 'Holmium'
     &,   6800, 167.259,  'Er', 'Erbium'
     &,   6900, 168.9342, 'Tm', 'Thulium'
     &,   7000, 173.04,   'Yb', 'Ytterbium'
     &,   7100, 174.967 , 'Lu', 'Lutetium'
     &,   7200, 178.49,   'Hf', 'Hafnium'
     &,   7300, 180.9479, 'Ta', 'Tantalum'
     &,   7400, 183.84,   ' W', 'Tungsten'
     &,   7500, 186.207,  'Re', 'Rhenium'
     &,   7600, 190.23,   'Os', 'Osmium'
     &,   7700, 192.217,  'Ir', 'Iridium'
     &,   7800, 195.078,  'Pt', 'Platinum'
     &,   7900, 196.9665, 'Au', 'Gold'
     &,   8000, 200.59,   'Hg', 'Mercury'
     &,   8100, 204.3833, 'Tl', 'Thallium'
     &,   8200, 207.2,    'Pb', 'Lead'
     &,   8300, 208.9804, 'Bi', 'Bismuth'
     &,   8400, 209,      'Po', 'Polonium'
     &,   8500, 210,      'At', 'Astatine'
     &,   8600, 222,      'Rn', 'Radon'
     &,   8700, 223,      'Fr', 'Francium'
     &,   8800, 226,      'Ra', 'Radium'
     &,   8900, 227,      'Ac', 'Actinium'/
      data (el_code(i),elmass(i),elsymbol(i),elname(i), i=90,z_max)/
     &    9000, 232.0381, 'Th', 'Thorium'
     &,   9100, 231.0359, 'Pa', 'Protactinium'
     &,   9200, 238.0289, ' U', 'Uranium'
     &,   9300, 237,      'Np', 'Neptunium'
     &,   9400, 244,      'Pu', 'Plutonium'
     &,   9500, 243,      'Am', 'Americium'
     &,   9600, 247,      'Cm', 'Curium'
     &,   9700, 247,      'Bk', 'Berkelium'
     &,   9800, 251,      'Cf', 'Californium'
     &,   9900, 252,      'Es', 'Einsteinium'
     &,  10000, 257,      'Fm', 'Fermium'
     &,  10100, 258,      'Md', 'Mendelevium'
     &,  10200, 259,      'No', 'Nobelium'
     &,  10300, 262,      'Lr', 'Lawrencium'
     &,  10400, 261,      'Rf', 'Rutherfordium'
     &,  10500, 262,      'Db', 'Dubnium'
     &,  10600, 266,      'Sg', 'Seaborgium'
     &,  10700, 264,      'Bh', 'Bohrium'
     &,  10800, 277,      'Hs', 'Hassium'
     &,  10900, 268,      'Mt', 'Meitnerium'
     &,  11000, 275,      'Ds', 'Darmstadtium'
     &,  11100, 272,      'Rg', 'Roentgenium'/
c
      save
      end module AGAbund
