"""
Ising model
"""

from . import log
from .colours import pastel
from .constants import kb  # Boltzmann constant
import inspect
import numpy as np


import random

# Prepare random 2D array of spins
# flip the spin of a random atom/magnet
# if dE < 0 (favourable) then flip it,
# if dE > 0 then flip it with prob exp(-dE/T)

class Model:
    """Ising model simulation"""

    def __init__(self, shape=(100, 100), temperature=0.8, magnetic_field=0, mu=0.5):
        self.width, self.height = shape
        self.temperature = temperature
        self.magnetic_field = magnetic_field
        self.lattice = self.random_grid(mu)
        self.lattice_mu = mu
        self.last_cycle = 0

    def magnetisation(self):
        """
        calculates the net magnetisation of the system
        i.e. the total spin of the system
        does not have real units.
        """
        return sum(sum(self.lattice))/(self.height * self.width)

    def random_grid(self, mu):
        """
        takes in mu, the probability of flipping, i.e. 0.85 will flip 85% of the spins
        """
        flipping = np.array(
            [random.choices([1, -1], [1-mu, mu], k=self.width) for _ in range(self.height)],
            dtype=np.byte)
        return flipping

    def flip(self, mu):
        self.lattice *= self.random_grid(mu)

    def energy(self, i, j):
        """
        Checks the position against its neighbours and compares spin,
        if it's the same the energy is negative (stable),
        if they're different it's positive (unstable)
        Adds an external magnetic field, B, which adds an aligning
        force to the spins, positive B will try to turn spins positive,
        by default it is off
        """
        centre = self.lattice[i, j]
        J = 2 # Coloumb interaction force (flip factor)
        # i moves from array to array
        # j moves right and left
        dist = 1
        E_tot = 0
        for k in range(1, dist+1):
            E = 0 
            # right
            E += -J * centre * self.lattice[i, (j+k) % self.width]
            # left
            E += -J * centre * self.lattice[i, (j-k) % self.width]
            # above
            E += -J * centre * self.lattice[(i-k) % self.height , j]
            # below
            E += -J * centre * self.lattice[(i+k) % self.height, j]
            
            E += -self.magnetic_field * self.lattice[i, j]
            E /= k**12  # distance proportionality
            E_tot += E

        return E_tot

    def cycle(self, cycle_num, cycle_callback=None):
        """
        Do one cycle.
        """
        i = random.randint(0, self.height - 1)
        j = random.randint(0, self.width  - 1)
        E = self.energy(i, j)
        T = self.temperature

        if E >= 0: # if E is in an unfavourable position
            self.lattice[i, j] *= -1
        elif T != 0 and np.exp(E/(T)) >= random.random(): # if E can "borrow" energy
            self.lattice[i, j] *= -1

        if cycle_callback is not None:
            cycle_callback(self, cycle_num)

        self.last_cycle += 1
        return E

    def simulate(self, cycles, cycles_callback=None):
        if isinstance(cycles, int):
            cycles = range(self.last_cycle, cycles)

        for cycle in cycles:
            # perform a cycle.
            self.cycle(cycle, cycles_callback)                

