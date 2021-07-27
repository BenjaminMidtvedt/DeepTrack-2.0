from functools import reduce
from deeptrack.dynamics import integration
import deeptrack as dt
import deeptrack.dynamics as dyn
import numpy as np
import matplotlib.pyplot as plt

universe = dyn.universe.Universe(0)


def attraction(position, group):

    pos = [atom.position() for atom in universe.atoms if atom.group() == group]
    centroid = np.mean(pos, axis=0)

    direct = centroid - position
    direct = direct / np.sqrt(np.sum(np.square(direct)))

    return direct * 3 + np.random.randn() * 3


def on_simulation_begin():

    universe.atoms = []
    universe.history = []

    universe.optics = dt.Fluorescence()

    for i in range(20):
        x = (i // 5) + 40
        y = (i % 5) + 40
        universe.add_atom(
            dt.PointParticle(
                position=np.array((x * 2, y * 2, np.random.randn())),
                velocity=np.random.randn(3) / 2,
                acceleration=0,
                force=attraction,
                mass=2,
                group=1,
                sigma=0.5,
                epsilon=1,
            )
        )

    for i in range(20):
        x = (i // 5) + 20
        y = (i % 5) + 20
        universe.add_atom(
            dt.PointParticle(
                position=np.array((x * 2, y * 2, np.random.randn())),
                velocity=np.random.randn(3) / 2,
                acceleration=0,
                force=attraction,
                mass=2,
                group=2,
                sigma=0.5,
                epsilon=1,
            )
        )


def on_frame_end():
    pos = np.array([atom.position() for atom in universe.atoms])
    universe.history.append(pos)

    sample = reduce(lambda a, b: a & b, universe.atoms)

    feature = universe.optics(
        sample,
    )
    feature.plot()

    if np.random.rand() < 0.005:

        groups = [atom.group() for atom in universe.atoms]

        new_group_index = np.max(groups) + 1

        old_group_index = np.random.randint(new_group_index)

        for atom in universe.atoms:
            if atom.group() == old_group_index and np.random.rand() > 0.5:
                atom.group.set_value(new_group_index)


np.random.seed(2)
universe.on_simulation_begin = on_simulation_begin
universe.on_frame_end = on_frame_end
universe.run(100, 0.03)
pos = np.array(universe.history)


for i in range(len(universe.atoms)):
    plt.plot(pos[:, i, 0], pos[:, i, 1])

plt.show()