import mtc
import matplotlib.pyplot as plt
import numpy as np
import random
import time

cycles = 500_000
duration = 15 # seconds
shape = (100, 100)
B = 0
sneed = int(time.time()) # sneeding for each simualtion
print(f'seeding with {sneed} for each sub-simulation.')

net_magnet = []
temperatures = [*np.linspace(0, 8, 20)] # * = explode 

for i, T in enumerate(temperatures):
    random.seed(sneed) 
    model = mtc.ising.Model(shape, T, B)
    model.simulate(cycles)
    net_magnet.append(model.magnetisation())
    mtc.log(f"\rdata points: {i+1}/{len(temperatures)}", end="")

mtc.log("\ndone!")
plt.plot(temperatures, net_magnet)
plt.show()
    