from . import ising

class Model(ising.Model):
    """
    modified energy function which changes the energy calculation so that elements to the 
    left and to the right of each element decrease the total energy if they are in opposite directions
    """
    def energy(self, i, j):
        centre = self.lattice[i, j]
        J = 2 # Coloumb interaction force (flip factor)
        # i moves from array to array
        # j moves right and left
        dist = 10
        E_tot = 0
        for k in range(1, dist+1):
            E = 0 
            if j + k < self.width:
                E += +J * centre * self.lattice[i, j+k]
            if j + k == self.width:
                E += +J * centre * self.lattice[i, 0] 
            ### NOTE: DOES NOT BOUNDARY CHECK WITH K, STOPS AT EDGES, NEED TO FIX IF J + k == SELF.WIDTH INTO > SELF.WIDTH + K OR SOMETHING
            if j - k >= 0:
                E += +J * centre * self.lattice[i, j-k]
            if j - k == -1:
                E += +J * centre * self.lattice[i, self.width-k]

            if i - k >= 0:
                E += -J * centre * self.lattice[i-k, j]
            if i - k == -1:
                E += -J * centre * self.lattice[self.height-k, j]

            if i + k < self.height:
                E += -J * centre * self.lattice[i+k, j]
            if i + k == self.height:
                E += -J * centre * self.lattice[0, j]

            E += -self.magnetic_field * self.lattice[i, j]
            E /= k**3  # distance proportionality
            E_tot += E

        return E_tot
