from . import log
from .colours import pastel
from .constants import kb  # Boltzmann constant

import numpy as np
import matplotlib as mpl
import matplotlib.animation as manim
import matplotlib.pyplot as plt

import random

# Prepare random 2D array of spins
# flip the spin of a random atom/magnet
# if dE < 0 (favourable) then flip it,
# if dE > 0 then flip it with prob exp(-dE/T)

class Model:
    """Ising model simulation"""

    def __init__(self, shape=(250, 250), temperature=0.8):
        self.width, self.height = shape
        self.temperature = temperature
        self.lattice = np.array([
            [random.choice([-1, 1]) for _ in range(self.width)]
                                    for _ in range(self.height)
        ])

    def energy(self, i, j):
        """
        Checks the position against its neighbours and compares spin,
        if it's the same the energy is negative (stable),
        if they're different it's positive (unstable)
        """
        centre = self.lattice[i, j]
        E = 0

        # i moves from array to array
        # j moves right and left
        if j + 1 < self.width:
            E += -2 * centre * self.lattice[i, j+1]
        if j - 1 >= 0:
            E += -2 * centre * self.lattice[i, j-1]
        if i - 1 >= 0:
            E += -2 * centre * self.lattice[i-1, j]
        if i + 1 < self.height:
            E += -2 * centre * self.lattice[i+1, j]

        return E

    def cycle(self):
        """
        Do one cycle.
        """
        i = random.randint(0, self.height - 1)
        j = random.randint(0, self.width  - 1)
        E = self.energy(i, j)
        T = self.temperature

        if E > 0:
            self.lattice[i, j] *= -1
        elif np.exp(E/(T)) >= random.random():
            self.lattice[i, j] *= -1

        return E

    def simulate(self, video_file, cycles, duration, fps=8, dpi=192, cmap=pastel):
        """
        Generate a video file of all the plot over all the cycles.
        At the end, the lattice (model state) is set to the state of
        the last cycle in the simulation.

        Neither the duration nor the fps affect how many cycles are performed,
        it does affect the rendering time a lot though, so choose wisely
        """
        fig = plt.figure()
        frames = fps * duration
        cycles_per_frame = int(cycles / frames)

        # grab ffmpeg writer
        Writer = manim.writers['ffmpeg']
        writer = Writer(fps=fps)

        # save plot as an mp4 file via ffmpeg
        with writer.saving(fig, video_file, dpi=dpi):
            log("baking cake...")

            for cycle in range(cycles):
                log(f"\rfinished: {round(cycle/cycles * 100)}%", end="")
                # perform a cycle.
                self.cycle()

                # save a video frame every cycles_per_frame frame
                if cycle % cycles_per_frame == 0:
                    img = plt.imshow(self.lattice, cmap=cmap)
                    writer.grab_frame()
                    img.remove()

            log("\rding!", " " * 16)

