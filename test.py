#%%

import deeptrack as dt
import deeptrack.dynamics as dyn
import numpy as np
import matplotlib.pyplot as plt

universe = dyn.universe.Universe(0)


def on_simulation_start():

    plt.figure()

    universe.atoms = []

    universe.add_atom(
        dt.PointParticle(
            position=np.array((32, 32)),
            velocity=np.array((-2, 0.02)),
            acceleration=0,
            force=lambda: 0,
            mass=2,
            sigma=1,
            epsilon=1,
        )
    )

    universe.add_atom(
        dt.PointParticle(
            position=np.array((28, 32)),
            velocity=np.array((2, 0.02)),
            acceleration=0,
            force=lambda: 0,
            mass=1,
            sigma=1,
            epsilon=1,
        )
    )


def on_frame_begin():
    for atom in universe.atoms:
        plt.scatter(*atom.position())


def on_simulation_end():
    plt.show()


universe.on_simulation_begin = on_simulation_start
universe.on_frame_start = on_frame_begin
universe.on_simulation_end = on_simulation_end


#%%

universe.run(2, 0.02)

#%%

p = dt.PointParticle(
    position=np.array((32, 32)),
    velocity=np.random.randn(),
    acceleration=0,
    force=lambda: np.random.randn(2),
    mass=1,
    sigma=1,
    epsilon=1,
)

#%%
print(p.force())
p.force.invalidate()
p.force.is_valid()
print(p.force())