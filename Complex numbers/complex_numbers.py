import math

class ComplexNumber(object):
    def __init__(s, real, imaginary):
        s.real = s.r = real
        s.imaginary = s.i = imaginary

    def __eq__(s, other):
        return s.r == other.r and s.i == other.i    
        
    def __add__(s, other):
        return ComplexNumber(s.r + other.r, s.i + other.i)
    
    def __mul__(s, other):
        return ComplexNumber(s.r * other.r - s.i * other.i, s.i * other.r + s.r * other.i)

    def __sub__(s, other):
        return ComplexNumber(s.r - other.r, s.i - other.i)

    def __truediv__(s, other):
        nom = (s.r * other.r + s.i * other.i)/(other.r**2 + other.i**2)
        den = (s.i * other.r - s.r * other.i)/(other.r**2 + other.i**2)
        return ComplexNumber(nom, den)

    def __abs__(s):
        return (s.r**2 + s.i**2)**0.5

    def conjugate(s):
        return ComplexNumber(s.r, -s.i)

    def exp(s):
        return ComplexNumber(math.exp(s.r) * math.cos(s.i), math.exp(s.r) * math.sin(s.i))