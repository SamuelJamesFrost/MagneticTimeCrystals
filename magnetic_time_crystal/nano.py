from . import ising
import numpy as np
from cffi import FFI
from os.path import exists, dirname

so = dirname(__file__) + "/" + "nano_magnetisation.so"
C = None
if exists(so):
    ffi = FFI()
    ffi.cdef("double nano_magnetisation(signed char *arr, size_t width, size_t height);")
    C = ffi.dlopen(so)
else:
    print("You should compile the shared object file to improve performance")

class Model(ising.Model):
    """
    Modified energy function which changes the energy calculation so that elements to the 
    left and to the right of each element decrease the total energy if they are in opposite directions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lattice = np.tile([1,-1], (self.height, int(self.width/2+1)))[:self.width,:self.height] 
        self.lattice *= self.random_grid(self.lattice_mu)
        self.lattice = self.lattice.astype(np.byte)

    def energy(self, i, j):
        centre = self.lattice[i, j]
        J = 2 # Coloumb interaction force (flip factor)
        # i moves from array to array
        # j moves right and left
        dist = 1
        E_tot = 0
        for k in range(1, dist+1):
            E = 0 
            # right
            E += +J * centre * self.lattice[i, (j+k) % self.width]
            # left
            E += +J * centre * self.lattice[i, (j-k) % self.width]
            # above
            E += -J * centre * self.lattice[(i-k) % self.height , j]
            # below
            E += -J * centre * self.lattice[(i+k) % self.height, j]
            
            E += -self.magnetic_field * self.lattice[i, j]
            E /= k**3  # distance proportionality
            E_tot += E

        return E_tot

    def magnetisation(self):
        """
        Modified magnetisation function which checks the stripiness of the lattice, probably 
        quite slow and can be improved upon
        """
        stripe = 0
        # there is definitely a better way to do this...
        for j in range(self.width):
            for i in range(self.height):
                stripe -= self.lattice[i,j] * self.lattice[(i+1) % self.width, j]
                stripe += self.lattice[i,j] * self.lattice[i, (j+1) % self.height]

        return stripe/(2*self.width*self.height)

if C is not None:
    doc = Model.magnetisation.__doc__
    def magnetisation(self):
        doc
        lattice = ffi.cast("signed char *", self.lattice.ctypes.data)
        return C.nano_magnetisation(lattice, self.width, self.height)
    Model.magnetisation = magnetisation
