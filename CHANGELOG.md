# Changelog
This changelog will double up as the lab diary.

### 01/03
Separated the plotting from the `ising.py` file, this allows for easier plotting of different plots, some of which have been added to the `/models` directory. 

### 04/03
Added a flipping function which creates a random lattice of spins, which when multiplied by the current lattice will result its random flipping proportional to some variable mu. Added a new file which demonstrates this. This new function brings out time crystal behaviour in the system, but only if mu > 0.85

### 08/03
Refactored the flipping function, created a random_grid function which is used in both the flipping function and the initialisation function.

### 12/03
Added a new plotting file, `tau_v_mu.py`, which plots the time between flips, against the number if spins flipped a in a 3D colour plot, this needs proper axes to be added to it 