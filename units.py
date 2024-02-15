from numpy import sqrt
from pint import UnitRegistry

units = UnitRegistry()

l = 5 * units.meter

print(sqrt(l))

print(l.to(units.miles))