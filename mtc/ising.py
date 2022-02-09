import numpy as np
import matplotlib as mpl
import matplotlib.animation as manim
import matplotlib.pyplot as plt
import random

# Prepare random 2D array of spins
# flip the spin of a random atom/magnet
# if dE < 0 (favourable) then flip it,
# if dE > 0 then flip it with prob exp(-dE/T)

PASTEL = mpl.colors.LinearSegmentedColormap.from_list('john',
        [(1,0.75,0.85), (0.75,0.80,1)])
N = 50
T = 300
#Boltzmann
kb = 1.38e-23

array = np.array([[random.choice([-1, 1]) for i in range(N)] for j in range(N)])
print(array)


def energy(i, j):
    """
    Checks the position against its neighbours and compares spin,
    if it's the same the energy is negative (stable),
    if they're different it's positive (unstable)
    """
    centre = array[i][j]
    E = 0
    # i moves from array to array
    # j moves right and left
    if j + 1 < N:
        E += -2 * centre * array[i][j+1]
    if j - 1 >= 0:
        E += -2 * centre * array[i][j-1]
    if i - 1 >= 0:
        E += -2 * centre * array[i-1][j]
    if i + 1 <  N:
        E += -2 * centre * array[i+1][j]
    return E



fig = plt.figure()

cycles = 5000
# take a frame 1% of the cycles
cycles_per_frame = cycles * 0.005


# grab ffmpeg writer
Writer = manim.writers['ffmpeg']
writer = Writer(fps=180)

# save plot as an mp4 file via ffmpeg
with writer.saving(fig, "ising.mp4", dpi=200):
    print("baking cake...")

    for cycle in range(cycles):
        print(f"\rfinished: {round(cycle/cycles * 100)}%", end="")
        i = random.randint(0, N-1)
        j = random.randint(0, N-1)
        E = energy(i, j)
        if E > 0:
            array[i, j] *= -1
        #elif np.exp(-E/(kb * T)) > random.random():
        #    array[i, j] *= -1

        # saves a video frame every cycles_per_frame frame
        if cycles % cycles_per_frame == 0:
            img = plt.imshow(array, cmap='binary')
            writer.grab_frame()
            img.remove()
    print("\rding!                 ")

