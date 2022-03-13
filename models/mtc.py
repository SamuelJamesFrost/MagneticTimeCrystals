import sys
sys.path.append("..")
import magnetic_time_crystal as mtc

for symbol in dir(mtc):
    if symbol[0] != '_':
        globals()[symbol] = getattr(mtc, symbol)
