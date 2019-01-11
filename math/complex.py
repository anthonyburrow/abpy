class Complex:

    def __init__(self, re, im):
        self.re = re
        self.im = im

    def __add__(self, other):
        if not isinstance(other, Complex):
            return Complex(self.re + other, self.im)

        return Complex(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, Complex):
            return Complex(self.re - other, self.im)

        return Complex(self.re - other.re, self.im - other.im)

    def __rsub__(self, other):
        if not isinstance(other, Complex):
            return Complex(other - self.re, -self.im)

        return Complex(other.re - self.re, other.im - self.im)

    def __mul__(self, other):
        if not isinstance(other, Complex):
            return Complex(self.re * other, self.im * other)

        return Complex(self.re * other.re - self.im * other.im,
                       self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def __pow__(self, other):
        if other == 0:
            return Complex(1, 0)
        s = self
        for i in range(other - 1):
            s *= self
        return s


def Conjugate(z):
    return Complex(z.re, -z.im)


def ModSquared(z):
    return z.re**2 + z.im**2
