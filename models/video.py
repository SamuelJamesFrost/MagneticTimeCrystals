import mtc
import numpy as np

cycles = 100_000
duration = 15 # seconds
shape = (100, 100)
T = 0 # NOT Kelvin
B = 0
mu = 0.95

mtc.log("generating ising model video.")

model = mtc.nano.Model(shape, T, B, mu=0.8)
#model.lattice = mtc.raster.shape_init(mtc.raster.star_of_david, 5, 90, 90, shape)
# model.lattice = np.tile([1,-1], (model.height, int(model.width/2+1)))[:shape[0],:shape[1]] * model.random_grid(0.8)
callback, stop_recording = mtc.plot.record_simulation('ising.mp4', cycles, duration, dpi=400, fps=15)

#model.simulate(cycles, callback)

x = 10
for i in range(x):
    model.simulate(int((i+1)*cycles/x), callback)
    model.flip(mu)
stop_recording()
mtc.log("\ndone!")
