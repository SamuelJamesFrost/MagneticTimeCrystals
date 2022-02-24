import mtc

if __name__ == '__main__':
    # Simulate Ising model.
    cycles = 500_000
    duration = 15 # seconds
    shape = (100, 100)
    T = 1.5 # Kelvin

    print("generating ising model video.")

    model = mtc.ising.Model(shape, T)
    model.simulate('ising.mp4', cycles, duration, fps=5)


