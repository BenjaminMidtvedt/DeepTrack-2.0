import numpy as np
import deeptrack as dt
from deeptrack.dynamics.forces import LennardJones, RepulsiveLennardJones
import pytest


u = dt.units


@pytest.mark.parametrize(
    "units",
    [True, False],
)
def test_LennardJones(units, benchmark):
    benchmark.group = f"LennardJones"
    benchmark.name = f"{'with' if units else 'without'} units"

    kwargs = {}

    def setup():

        kwargs["dx"] = (u.m if units else 1) * np.random.randn(3)
        kwargs["sigma"] = (u.m if units else 1) * np.random.rand()
        kwargs["eps"] = (u.m * u.N if units else 1) * np.random.rand()
        return ((), kwargs)

    benchmark.pedantic(LennardJones, setup=setup, rounds=100)


@pytest.mark.parametrize(
    "units",
    [True, False],
)
def test_RepulsiveLennardJones(units, benchmark):
    benchmark.group = f"RepulsiveLennardJones"
    benchmark.name = f"{'with' if units else 'without'} units"

    kwargs = {}

    def setup():

        kwargs["dx"] = (u.m if units else 1) * np.random.randn(3)
        kwargs["sigma"] = (u.m if units else 1) * np.random.rand()
        kwargs["eps"] = (u.m * u.N if units else 1) * np.random.rand()
        return ((), kwargs)

    benchmark.pedantic(RepulsiveLennardJones, setup=setup, rounds=100)
