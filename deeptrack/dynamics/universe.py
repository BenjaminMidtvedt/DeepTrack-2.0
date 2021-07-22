from .integration import VelocityVerlet
import numpy as np
from .. import units as u


class Universe:
    def __init__(self, bounds, border_condition="periodic"):

        self.bounds = bounds
        self.border_condition = "periodic"

        self.on_frame_start = lambda: ...
        self.on_frame_end = lambda: ...

        self.on_simulation_begin = lambda: ...
        self.on_simulation_end = lambda: ...

        self.integrator = VelocityVerlet()

        self.atoms = []

    def add_atom(self, atom):
        assert hasattr(atom, "position"), "Atom needs to have a position"
        assert hasattr(atom, "velocity"), "Atom needs to have a defined velocity"
        assert hasattr(
            atom, "acceleration"
        ), "Atom needs to have a defined acceleration"
        assert hasattr(atom, "force"), "Atom needs to define a force"
        assert hasattr(atom, "mass"), "Atom needs to define a mass"
        assert hasattr(
            atom, "sigma"
        ), "Atom needs to define sigma (the effective size of the atom)"
        self.atoms.append(atom)

    def run(self, time, dt):
        t = 0

        self.on_simulation_begin()

        while t < time:
            self.on_frame_start()

            self.integrator.step(self.atoms, dt)

            self.on_frame_end()
            t += dt

        self.on_simulation_end()