

# Units and factors from SI units
unit_equivalencies = {
    'km': ('distance', 1e3),
    'm': ('distance', 1.),
    'cm': ('distance', 1e-2),
    'nm': ('distance', 1e-9),
    'Angstrom': ('distance', 1e-10),
    'yr': ('time', 31557600.),
    's': ('time', 1.),
    'kg': ('mass', 1.),
    'g': ('mass', 1e-3),
    'C': ('charge', 1.),
    'J': ('energy', 1.),
    'erg': ('energy', 1e-7),
    'eV': ('energy', 1.602176634e-19),
    'W': ('power', 1.),
    'erg/s': ('power', 1e-7),
    'T': ('magnetic field', 1.),
    'G': ('magnetic field', 1e-5),
    'F': ('capacitance', 1.),
    'K': ('temperature', 1.),
}


class Unit:

    def __init__(self, unit: str = None, multiple: float = None):
        self._unit_dict = {}

        if multiple is None:
            multiple = 1.

        if unit is not None:
            if unit not in unit_equivalencies:
                print(f'Warning: {unit} not a valid unit.')
            unit_type = unit_equivalencies[unit][0]
            self._unit_dict[unit_type] = {unit: multiple}

    def get_conversion(self, *desired_units: tuple):
        factor = 1.
        new_units = self.copy()

        for desired_unit in desired_units:
            _factor, _new_units = self._get_single_conversion(desired_unit)

            factor *= _factor
            new_units *= _new_units

        return factor, new_units

    def copy(self):
        new_units = Unit()

        new_unit_dict = {}
        for unit_type, unit_group in self._unit_dict.items():
            new_unit_dict[unit_type] = unit_group.copy()

        new_units._unit_dict = new_unit_dict

        return new_units

    def __add__(self, x):
        assert self._unit_dict == x._unit_dict

        return self.copy()

    def __mul__(self, x):
        assert isinstance(x, Unit)

        if not x._unit_dict:
            return self.copy()

        new_units = self.copy()

        for unit_type, x_unit_group in x._unit_dict.items():
            if unit_type not in new_units._unit_dict:
                new_units._unit_dict[unit_type] = x_unit_group.copy()
                continue

            unit_group = new_units._unit_dict[unit_type]
            for unit, multiple in x_unit_group.items():
                if unit not in unit_group:
                    unit_group[unit] = multiple
                    continue

                unit_group[unit] += multiple

        new_units._clear_zero_factors()

        return new_units

    # def __rmul__(self, x):
    #     return self.__mul__(x)

    def __imul__(self, x):
        assert isinstance(x, Unit)

        if not x._unit_dict:
            return self

        for unit_type, x_unit_group in x._unit_dict.items():
            if unit_type not in self._unit_dict:
                self._unit_dict[unit_type] = x_unit_group.copy()
                continue

            unit_group = self._unit_dict[unit_type]
            for unit, multiple in x_unit_group.items():
                if unit not in unit_group:
                    unit_group[unit] = multiple
                    continue

                unit_group[unit] += multiple

        self._clear_zero_factors()

        return self

    def __truediv__(self, x):
        return self * x**(-1.)

    # def __rtruediv__(self, x):
    #     return self**(-1.) * x

    def __pow__(self, x):
        new_units = self.copy()

        for unit_group in new_units._unit_dict.values():
            for unit in unit_group:
                unit_group[unit] *= x

        return new_units

    def __eq__(self, x):
        return self._unit_dict == x._unit_dict

    def __str__(self):
        return str(self._unit_dict)

    def _clear_zero_factors(self):
        for unit_type in list(self._unit_dict):
            unit_group = self._unit_dict[unit_type]
            for unit in list(unit_group):
                if unit_group[unit] == 0.:
                    unit_group.pop(unit, None)
            if not unit_group:
                self._unit_dict.pop(unit_type, None)

    def _get_single_conversion(self, desired_unit: str):
        if desired_unit not in unit_equivalencies:
            print(f'Warning: {desired_unit} not a valid unit.')
            return 1.

        unit_type = unit_equivalencies[desired_unit][0]
        if unit_type not in self._unit_dict:
            print(f'Warning: Cannot convert to {desired_unit}')
            return 1.

        factor = 1.
        new_units = Unit()
        for unit, multiple in self._unit_dict[unit_type].items():
            if unit == desired_unit:
                continue

            new_scale = unit_equivalencies[desired_unit][1]
            old_scale = unit_equivalencies[unit][1]
            # This seems backwards because of the values I use
            # in `unit_equivalencies`
            factor *= (old_scale / new_scale)**multiple

            new_units *= Unit(desired_unit) / Unit(unit)

        return factor, new_units


class Quantity():

    def __init__(self, value: float, units: dict = None):
        self.value = value
        self.units = Unit()

        if units is not None:
            for unit, multiple in units.items():
                self.units *= Unit(unit, multiple)

    def __add__(self, x):
        if not isinstance(x, Quantity):
            new_quantity = Quantity(self.value + float(x))
            new_quantity.units = self.units.copy()

            return new_quantity

        new_quantity = Quantity(self.value + x.value)
        new_quantity.units = self.units + x.units

        return new_quantity

    def __radd__(self, x):
        return self.__add__(x)

    def __mul__(self, x):
        if not isinstance(x, Quantity):
            new_quantity = Quantity(self.value * float(x))
            new_quantity.units = self.units.copy()

            return new_quantity

        new_quantity = Quantity(self.value * x.value)
        new_quantity.units = self.units * x.units

        return new_quantity

    def __rmul__(self, x):
        return self.__mul__(x)

    def __truediv__(self, x):
        if not isinstance(x, Quantity):
            new_quantity = Quantity(self.value / float(x))
            new_quantity.units = self.units.copy()

            return new_quantity

        new_quantity = Quantity(self.value / x.value)
        new_quantity.units = self.units / x.units

        return new_quantity

    def __rtruediv__(self, x):
        if not isinstance(x, Quantity):
            new_quantity = Quantity(float(x) / self.value)
            new_quantity.units = self.units.copy()

            return new_quantity

        new_quantity = Quantity(x.value / self.value)
        new_quantity.units = x.units / self.units

        return new_quantity

    def __pow__(self, x):
        new_quantity = Quantity(self.value**x)
        new_quantity.units = self.units**x

        return new_quantity

    def __str__(self):
        return str(self.value) + '   ' + str(self.units)

    def to(self, *desired_units):
        if desired_units[0].lower() == 'si':
            return self._to_si()
        elif desired_units[0].lower() == 'cgs':
            return self._to_cgs()
        else:
            return self._to_specific(*desired_units)

    def _to_si(self):
        pass

    def _to_cgs(self):
        pass

    def _to_specific(self, *desired_units):
        factor, new_units = self.units.get_conversion(*desired_units)
        new_value = self.value * factor

        new_quantity = Quantity(new_value)
        new_quantity.units = new_units

        return new_quantity


if __name__ == '__main__':
    h_bar = Quantity(1.054571817e-34, {'J': 1., 's': 1.})
    c = Quantity(2.99792458e8, {'m': 1., 's': -1.})