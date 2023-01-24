import numpy as np
import pykep as pk
from pykep import phasing
# from pykep import _dbscan
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from SpoC_Constants import data, dict_asteroids


T_START = pk.epoch_from_iso_string("30190302T000000")  # Start and end epochs

start_asts = [3622, 5384, 2257, 925]
for id in start_asts:
    print(np.array(dict_asteroids[id][0].eph(T_START.mjd2000)[0])) # r  vom kepler-Element als np-array