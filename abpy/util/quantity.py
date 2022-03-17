

# Units and factors from SI units
unit_conversions = {
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

unit_equivalencies = {
    'J': {'charge': ('C', 2.), 'capacitance': ('F', -1.)},
    'J': {'mass': ('kg', 1.), 'distance': ('m', 2.), 'time': ('s', -2.)}
}


class Unit:

    def __init__(self, unit: str = None, multiple: float = None):
        self._unit_dict = {}

        if multiple is None:
            multiple = 1.

        if unit is not None:
            if unit not in unit_conversions:
                print(f'Warning: {unit} not a valid unit.')
            unit_type = unit_conversions[unit][0]
            self._unit_dict[unit_type] = {unit: multiple}

    def get_conversion(self, *desired_units: tuple, simplify=True):
        factor = 1.
        new_units = self.copy()

        for desired_unit in desired_units:
            _factor, _new_units = self._get_single_conversion(desired_unit)

            factor *= _factor
            new_units *= _new_units

        if simplify:
            new_units.simplify()

        return factor, new_units

    def simplify(self):
        for new_unit, new_unit_equivs in unit_equivalencies.items():
            # Check if unit types exist in Unit
            unit_types = new_unit_equivs.keys()
            if not all(unit_type in self._unit_dict for unit_type in unit_types):
                continue

            # Check if the specific units from equivalencies are in Unit
            if not all(unit_group[0] in self._unit_dict[unit_type]
                       for unit_type, unit_group in new_unit_equivs.items()):
                continue

            # Check if there are enough multiples of each unit within Unit
            if not all(unit_group[1] < self._unit_dict[unit_type][unit_group[0]]
                       for unit_type, unit_group in new_unit_equivs.items()):
                continue

            # Check for the maximum number of unit exchanges to perform
            # (This is limited to integer multiples)
            new_unit_multiple = None
            for unit_type, unit_group in new_unit_equivs.items():
                unit, multiple = unit_group
                total_multiple = self._unit_dict[unit_type][unit]
                if multiple is not None:
                    new_unit_multiple = min(new_unit_multiple,
                                            total_multiple // multiple)

            # Rescale the units
            conversion = Unit(new_unit, new_unit_multiple)
            for unit, multiple in new_unit_equivs.values():
                conversion /= Unit(unit, multiple)
            self *= conversion

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
        new_units = self.copy()
        new_units *= x**(-1.)

        return new_units

    def __itruediv__(self, x):
        self *= x**(-1.)

        return self

    def __pow__(self, x):
        new_units = self.copy()

        for unit_group in new_units._unit_dict.values():
            for unit in unit_group:
                unit_group[unit] *= x

        return new_units

    def __eq__(self, x):
        return self._unit_dict == x._unit_dict

    def __str__(self):
        unit_str_list = [
            f'{unit}^{multiple}' if multiple > 0. else f'{unit}^{{{multiple}}}'
            for unit_type, unit_group in self._unit_dict.items()
            for unit, multiple in unit_group.items()
        ]
        s = ' '.join(unit_str_list)

        return s

    def _clear_zero_factors(self):
        for unit_type in list(self._unit_dict):
            unit_group = self._unit_dict[unit_type]
            for unit in list(unit_group):
                if unit_group[unit] == 0.:
                    unit_group.pop(unit, None)
            if not unit_group:
                self._unit_dict.pop(unit_type, None)

    def _get_single_conversion(self, desired_unit: str):
        factor = 1.
        new_units = Unit()

        if desired_unit not in unit_conversions:
            print(f'Warning: {desired_unit} not a valid unit.')
            return factor, new_units

        unit_type = unit_conversions[desired_unit][0]
        if unit_type not in self._unit_dict:
            print(f'Warning: Cannot convert to {desired_unit}')
            return factor, new_units

        for unit, multiple in self._unit_dict[unit_type].items():
            if unit == desired_unit:
                continue

            new_scale = unit_conversions[desired_unit][1]
            old_scale = unit_conversions[unit][1]
            # This seems backwards because of the values I use
            # in `unit_conversions`
            factor *= (old_scale / new_scale)**multiple
            new_units *= (Unit(desired_unit) / Unit(unit))**multiple

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

    def __sub__(self, x):
        return self.__add__(-x)

    def __rsub__(self, x):
        return (-self).__add__(x)

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
            new_quantity.units = self.units**(-1.)

            return new_quantity

        new_quantity = Quantity(x.value / self.value)
        new_quantity.units = x.units / self.units

        return new_quantity

    def __pow__(self, x):
        new_quantity = Quantity(self.value**x)
        new_quantity.units = self.units**x

        return new_quantity

    def __neg__(self):
        new_quantity = Quantity(-self.value)
        new_quantity.units = self.units.copy()

        return new_quantity

    def __str__(self):
        return f'{self.value}   {self.units}'

    def __format__(self, format_spec):
        return '{:{}}   {}'.format(self.value, format_spec, self.units)

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

        new_quantity = Quantity(self.value * factor)
        new_quantity.units = new_units

        return new_quantity


if __name__ == '__main__':
    h_bar = Quantity(1.054571817e-34, {'J': 1., 's': 1.})
    c = Quantity(2.99792458e8, {'m': 1., 's': -1.})
