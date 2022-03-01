import mtc

cycles = 100_000
duration = 15 # seconds
shape = (100, 100)
T = 4 # Kelvin
B = 8

mtc.log("generating ising model video.")

model = mtc.ising.Model(shape, T, B)

callback, stop_recording = mtc.plot.record_simulation('ising.mp4', cycles, duration)
model.simulate(int(cycles/3), callback)
model.magnetic_field = -8
model.simulate(int(2*cycles/3), callback)

model.magnetic_field = 0
model.simulate(cycles, callback)
stop_recording()
mtc.log("\ndone!")