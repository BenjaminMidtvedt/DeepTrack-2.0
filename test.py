#%%

import deeptrack as dt
import deeptrack.dynamics as dyn
import numpy as np
import matplotlib.pyplot as plt

universe =dyn.universe.Universe(0)

def on_simulation_begin():
    # np.random.seed(0)
    for i in range(1):
        x = i // 5
        y = i % 5
        universe.add_atom(
            dt.PointParticle(
                position=np.array((x, y)),
                velocity=np.random.randn(2),
                acceleration=0,
                force=0,
                mass=2,
                sigma=0.5,
                epsilon=1,
            )
        )

universe.on_simulation_begin = on_simulation_begin

universe.run(0.5, 0.01)


#%%

%timeit universe.run(0.01, 0.01)

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