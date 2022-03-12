import mtc
import matplotlib.pyplot as plt
import numpy as np

tau = 30 # how many times the entire system is allowed to evolve before flipping
        # i.e tau = 2 means 20,000 (2 * (100x100)) cycles between each flip
        # tau CANNOT BE 0 (ZERO), the larger the value of tau the more cycles required and thus
        # the longer the computational time
single_evolution = 10_000
shape = (100, 100)
B = 0
T = 0
res = 40 # how many different mu values we want
tau = res # we want it square so for now tau = res
flips = 10 # how many times you want it to flip, incerases the resolution of the data
final = [ [None]*res for i in range(tau)]

mus = np.linspace(0.8, 1, res)  # * = explode 
taus = np.linspace(0.1, 4, tau)

for k, tau in enumerate(taus):
    cycles = tau * single_evolution * flips * res
    for i, mu in enumerate(mus):
        net_magnet = []
        total_cycles = []
        def record_magnetisation(model, cycle):
            if cycle % 100 == 0:
                total_cycles.append(cycle)
                net_magnet.append(model.magnetisation())

        model = mtc.ising.Model(shape, T, B, 0.8)

        for j in np.arange(i*cycles/res, (i+1)*cycles/res, cycles/(res*flips)):
            sub_cycles = int(j-((i)*cycles/res) + cycles/(res*flips))
            model.simulate(sub_cycles, record_magnetisation)
            model.flip(mu)

        #plt.plot(total_cycles, net_magnet, label=str(mu))

        # some fine tuning required
        net_magnet = sum(abs(np.array(net_magnet[int(0*len(net_magnet)):])))/len(net_magnet)
        final[k][i] = net_magnet

        mtc.log(f"\rtau: {k+1}/{len(taus)} mu: {i+1}/{len(mus)} ", end="  ")

mtc.log("\ndone!")

plt.imshow(final, origin='lower')
plt.colorbar()
plt.show()
