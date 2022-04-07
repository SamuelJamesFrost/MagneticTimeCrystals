import mtc
import matplotlib.pyplot as plt
import numpy as np
import random
import time

cycles = 100_000
duration = 15 # seconds
shape = (50, 50)
B = 0
sneed = int(time.time()) # sneeding for each simualtion
print(f'seeding with {sneed} for each sub-simulation.')

net_magnet = []
temperatures = [*np.linspace(0, 2, 20)] # * = explode
res = 5

for i, T in enumerate(temperatures):
    random.seed(sneed)
    mag = 0
    for k in range(res):
        model = mtc.nano.Model(shape, T, B)
        model.simulate(cycles)
        mag += model.magnetisation()

    net_magnet.append(mag/res)
    #net_magnet.append(model.magnetisation())
    mtc.log(f"\rdata points: {i+1}/{len(temperatures)}", end="")

mtc.log("\ndone!")
plt.ylabel("Normalised Magnetisation")
plt.xlabel("Temperature")
plt.plot(temperatures, net_magnet, 'x')
plt.plot(temperatures, net_magnet, '-')
plt.show()

