import sys
import warnings
warnings.filterwarnings('ignore')

# General functions used in imports
def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

from . import ising
from . import plot

def main():
    pass

if __name__ == '__main__':
    main()
