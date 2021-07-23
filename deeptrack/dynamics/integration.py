from itertools import combinations
import itertools
from .forces import RepulsiveLennardJones, _two_to_power_one_over_six
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

        max_sigma = max(f.sigma() for f in atoms)

        max_x = max(f.position()[0] for f in atoms)
        max_y = max(f.sigma() for f in atoms)
        min_x = max(f.sigma() for f in atoms)
        min_y = max(f.sigma() for f in atoms)

        for (atom_1, atom_2) in combinations(atoms, 2):

            dx = atom_1.position() - atom_2.position()

            r = np.sqrt(np.sum(np.square(dx)))

            sigma = atom_1.sigma() + atom_2.sigma()

            if r < _two_to_power_one_over_six * sigma:
                epsilon = 1
                force = RepulsiveLennardJones(r, sigma, epsilon) / r * dx
                atom_1.force.set_value(atom_1.force() + force)
                atom_2.force.set_value(atom_2.force() - force)

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


class FastVelocityVerlet(VelocityVerlet):
    def update_force(self, atoms, dt):

        _ = [atom.force.invalidate() for atom in atoms]

        max_sigma = max(f.sigma() for f in atoms)

        positions = np.array([f.position() for f in atoms])

        ind_positions = (positions // (max_sigma * 2)).astype(np.int)

        cells = dict()

        for i, p in enumerate(ind_positions):
            p = tuple(p)
            if p not in cells:
                cells[p] = []

            cells[p].append(i)

        for key, atom_indices in cells.items():

            for index in atom_indices:
                for offset in itertools.product([-1, 0, 1], [-1, 0, 1]):

                    other_key = tuple(a + b for a, b in zip(key, offset))

                    if other_key in cells:
                        for other in cells[other_key]:

                            if other == index:
                                continue
                            atom_1 = atoms[index]
                            atom_2 = atoms[other]

                            dx = atom_1.position() - atom_2.position()

                            r = np.sqrt(np.sum(np.square(dx)))

                            sigma = atom_1.sigma() + atom_2.sigma()

                            if r < sigma * 1.3:
                                epsilon = 1
                                force = (
                                    RepulsiveLennardJones(r, sigma, epsilon) / r * dx
                                )
                                atom_1.force.set_value(atom_1.force() + force)
                                atom_2.force.set_value(atom_2.force() - force)

            atom_indices.remove(index)
        # for (atom_1, atom_2) in combinations(atoms, 2):
