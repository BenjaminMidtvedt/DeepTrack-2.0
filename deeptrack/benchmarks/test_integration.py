import numpy as np
import deeptrack as dt
from deeptrack.dynamics.universe import Universe
import pytest


u = dt.units


@pytest.mark.parametrize(
    "num_particles",
    [1, 10, 100],
)
def test_VelocityVerlet(num_particles, benchmark):
    benchmark.group = f"VelocityVerlet {num_particles} particles"

    universe = Universe(0)

    particles = [
        dt.PointParticle(
            position=np.array((i // 5, i % 5)),
            velocity=np.random.randn(2),
            acceleration=0,
            force=0,
            mass=2,
            sigma=0.5,
            epsilon=1,
        )
        for i in range(num_particles)
    ]

    def on_simulation_begin():
        np.random.seed(0)

        universe.atoms = []
        for i in range(num_particles):
            universe.add_atom(particles[i])

    universe.on_simulation_begin = on_simulation_begin

    benchmark(lambda: universe.run(0.5, 0.01))
