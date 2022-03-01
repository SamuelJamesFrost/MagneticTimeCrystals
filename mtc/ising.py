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

    def __init__(self, shape=(100, 100), temperature=0.8):
        self.width, self.height = shape
        self.temperature = temperature
        self.lattice = np.array([
            [random.choice([-1, -1]) for _ in range(self.width)]
                                    for _ in range(self.height)
        ])

    def energy(self, i, j, B=0):
        """
        Checks the position against its neighbours and compares spin,
        if it's the same the energy is negative (stable),
        if they're different it's positive (unstable)
        Adds an external magnetic field, B, which adds an aligning
        force to the spins, positive B will try to turn spins positive,
        by default it is off
        """
        centre = self.lattice[i, j]
        E = 0

        # i moves from array to array
        # j moves right and left
        if j + 1 < self.width:
            E += -2 * centre * self.lattice[i, j+1]
        if j + 1 == self.width:
            E += -2 * centre * self.lattice[i, 0]

        if j - 1 >= 0:
            E += -2 * centre * self.lattice[i, j-1]
        if j - 1 == -1:
            E += -2 * centre * self.lattice[i, self.width-1]

        if i - 1 >= 0:
            E += -2 * centre * self.lattice[i-1, j]
        if i - 1 == -1:
            E += -2 * centre * self.lattice[self.height-1, j]

        if i + 1 < self.height:
            E += -2 * centre * self.lattice[i+1, j]
        if i + 1 == self.height:
            E += -2 * centre * self.lattice[0, j]

        # magnetic field  essentially lowers the energy needed to switch state
        E += - B * self.lattice[i, j]

        return E

    def cycle(self):
        """
        Do one cycle.
        """
        i = random.randint(0, self.height - 1)
        j = random.randint(0, self.width  - 1)
        E = self.energy(i, j, 2)
        T = self.temperature

        if E >= 0: # if E is in an unfavourable position
            self.lattice[i, j] *= -1
        elif np.exp(E/(T)) >= random.random() and T != 0:
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

        magnet = []
        x_axis = [] 

        # converts inputted cmap string into a cmap object 
        if isinstance(cmap, str):
            cmap = mpl.cm.get_cmap(cmap)

        # save plot as an mp4 file via ffmpeg
        with writer.saving(fig, video_file, dpi=dpi):
            log("baking cake...")

            for cycle in range(cycles):
                log(f"\rfinished: {round(cycle/cycles * 100)}%", end="")
                # perform a cycle.
                self.cycle()

                # save a video frame every cycles_per_frame frame
                if cycle % cycles_per_frame == 0:
                    # exponential factor for more frames near the start 
                    #print(cycle % int(cycles_per_frame / (500/np.exp(cycle/10000)+1)))
                    plt.clf() # clears the figure every cycle so graphs don't accumulate
                    magnet.append(sum(sum(self.lattice))/(self.height * self.width))
                    x_axis.append(cycle)

                    plt.subplot(211)
                    img = plt.imshow(self.lattice, cmap=cmap, clim=(-1, 1))
                    plt.subplot(212)
                    plt.plot(x_axis, magnet)

                    plt.ylabel("Pseudo-Magnetisation")
                    plt.xlabel("Cycles")
                    writer.grab_frame()
                    img.remove()

            log("\rding!", " " * 16)
            print(len(magnet))