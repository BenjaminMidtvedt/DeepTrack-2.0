import numpy as np
from pint.quantity import Quantity


def LennardJones(dx, sigma, eps):
    d = sigma / dx
    if isinstance(d, Quantity):
        d = d.to_base_units().magnitude

    d2 = d * d
    d4 = d2 * d2
    d6 = d4 * d2
    d12 = d6 * d6
    return 48 * eps * (d12 - 0.5 * d6) / dx


_two_to_power_one_over_six = 2 ** (1 / 6)


def RepulsiveLennardJones(dx, sigma, eps):

    d = dx / sigma
    if isinstance(d, Quantity):
        d = d.to_base_units().magnitude

    dx2 = np.clip(np.abs(d), 0, _two_to_power_one_over_six)
    dx2 = dx2 * np.sign(d) * sigma
    return LennardJones(dx2, sigma, eps)
