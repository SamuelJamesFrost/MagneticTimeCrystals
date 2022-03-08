import mtc

cycles = 5_000_000
duration = 15 # seconds
shape = (100, 100)
T = 0.8 # Kelvin
B = 0
mu = 0.85

mtc.log("generating ising model video.")

model = mtc.ising.Model(shape, T, B)

callback, stop_recording = mtc.plot.record_simulation('ising.mp4', cycles, duration)

x = 10
for i in range(x):
    model.simulate(int((i+1)*cycles/x), callback)
    model.flip(mu)
stop_recording()
mtc.log("\ndone!")