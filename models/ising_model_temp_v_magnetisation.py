import mtc
import matplotlib.pyplot as plt
import numpy as np

cycles = 100_000
duration = 15 # seconds
shape = (100, 100)
B = 0

net_magnet = []
temperatures = [*np.linspace(0, 8, 20)] # * = explode 

for i, T in enumerate(temperatures):
    model = mtc.ising.Model(shape, T, B)
    model.simulate(cycles)
    net_magnet.append(model.magnetisation())
    mtc.log(f"\rdata points: {i+1}/{len(temperatures)}", end="")

mtc.log("\ndone!")
plt.plot(temperatures, net_magnet)
plt.show()
    