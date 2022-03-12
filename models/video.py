import mtc

cycles = 500_000
duration = 15 # seconds
shape = (100, 100)
T = 0 # NOT Kelvin
B = 0
mu = 0.97

mtc.log("generating ising model video.")

model = mtc.ising.Model(shape, T, B, mu=0.5)
callback, stop_recording = mtc.plot.record_simulation('ising.mp4', cycles, duration, fps=10)

x = 50
for i in range(x):
    model.simulate(int((i+1)*cycles/x), callback)
    model.flip(mu)
stop_recording()
mtc.log("\ndone!")