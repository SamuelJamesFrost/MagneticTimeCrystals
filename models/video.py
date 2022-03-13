import mtc

cycles = 500_000
duration = 15 # seconds
shape = (100, 100)
T = 0 # NOT Kelvin
B = 0
mu = 0.97

mtc.log("generating ising model video.")

model = mtc.ising.Model(shape, T, B, mu=0.5)
model.lattice = mtc.raster.shape_init(mtc.raster.square, 10, 80, 80, shape)
callback, stop_recording = mtc.plot.record_simulation('ising.mp4', cycles, duration, fps=5)

model.simulate(cycles, callback)

x = 20
for i in range(x):
    model.simulate(int((i+1)*cycles/x), callback)
    model.flip(mu)
stop_recording()
mtc.log("\ndone!")