


import sys
sys.path.append("../DeepTrack")

from DeepTrack.Generators import Generator
from DeepTrack.Particles import SphericalParticle
from DeepTrack.Backend.Distributions import uniform_random
from DeepTrack.Noise import Gaussian, Offset
from DeepTrack.Optics import BaseOpticalDevice2D
import numpy as np
import matplotlib.pyplot as plt

from timeit import default_timer as timer

'''
    Simple example showcasing current possiblites.
    
    A generator is created with certai optical properties. To the generator two particles are added.
 '''


Optics = BaseOpticalDevice2D(
    shape=(64,64),      # Desired output shape of the generator.
    NA=0.7,             # The NA of the optical system.
    pixel_size=0.1e-6,     # The pixel_size of the optical system (m).
    wavelength=0.68e-6     # The wavelength of the illuminating source (m).
)

G = Generator(
    Optics
)

P = SphericalParticle(
    radius=np.linspace(0.1e-6,1e-6),                                             # Radius of the generated particles
    intensity=np.linspace(40, 60),                           # Peak intensity of the generated particle
    position_distribution=uniform_random((64,64,10))           # The distrbution from which to draw the position of the particle
)

N1 = Gaussian(
    mu=0, 
    sigma=np.linspace(0.02,0.05)
)

N2 = Offset(
    offset=np.linspace(-0.2,0.2)
)

G.get(P + N1 + N2)


# Time the average generation time for 100 particles
start = timer()

for i in range(100):
    image = G.get(P*0.9 + P*0.2 + N1 + N2)

end = timer()

print("Generates (128,128) particles at {0}s per image".format((end - start)/100))


# Show one typical particle
plt.gray()
for i in range(1):
    Image = G.get(P + P + N1 + N2)
    plt.imshow(Image, vmin=-0.2, vmax=1)
    plt.show()

