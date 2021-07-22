from itertools import combinations
from .forces import RepulsiveLennardJones
from .. import units as u

import numpy as np


class VelocityVerlet:
    def step(self, atoms, dt):
        self.update_position(atoms, dt)
        self.update_force(atoms, dt)
        self.update_velocity(atoms, dt)
        self.update_acceleration(atoms, dt)

    def update_position(self, atoms, dt):
        dt2 = dt * dt
        for atom in atoms:
            new_pos = atom.position() + atom.velocity() * dt + atom.acceleration() * dt2
            atom.position.set_value(new_pos)

    def update_force(self, atoms, dt):

        _ = [atom.force.invalidate() for atom in atoms]

        for (atom_1, atom_2) in combinations(atoms, 2):

            dx = atom_1.position() - atom_2.position()

            r = np.sqrt(np.sum(np.square(dx)))

            sigma = atom_1.sigma() + atom_2.sigma()
            epsilon = 1

            force = RepulsiveLennardJones(r, sigma, epsilon) / r * dx
            atom_1.force.set_value(atom_1.force() + force)
            atom_2.force.set_value(atom_2.force() - force)

            print(atom_1.force(), atom_2.force())

    def update_velocity(self, atoms, dt):
        dt05 = dt * 0.5
        for atom in atoms:
            new_vel = (
                atom.velocity()
                + (atom.force() / atom.mass() + atom.acceleration()) * dt05
            )
            atom.velocity.set_value(new_vel)

    def update_acceleration(self, atoms, dt):
        for atom in atoms:
            atom.acceleration.set_value(atom.force() / atom.mass())
