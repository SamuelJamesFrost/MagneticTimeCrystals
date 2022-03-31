from . import ising

class Model():
    def energy(self, i, j):
        """ 
        modified energy function which changes the energy calculation so that elements to the 
        left and to the right of each element decrease the total energy if they are in opposite directions
        """
        centre = self.lattice[i, j]
        E = 0 
        J = 2 # Coloumb interaction force (flip factor)
        # i moves from array to array
        # j moves right and left
        if j + 1 < self.width:
            E += J * centre * self.lattice[i, j+1]
        if j + 1 == self.width:
            E += J * centre * self.lattice[i, 0]

        if j - 1 >= 0:
            E += J * centre * self.lattice[i, j-1]
        if j - 1 == -1:
            E += J * centre * self.lattice[i, self.width-1]

        if i - 1 >= 0:
            E += -J * centre * self.lattice[i-1, j]
        if i - 1 == -1:
            E += -J * centre * self.lattice[self.height-1, j]

        if i + 1 < self.height:
            E += -J * centre * self.lattice[i+1, j]
        if i + 1 == self.height:
            E += -J * centre * self.lattice[0, j]

        # magnetic field  essentially lowers the energy needed to switch state
        E += - self.magnetic_field * self.lattice[i, j]

        return E
