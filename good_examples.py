import numpy as np
import pykep as pk
from pykep import phasing
# from pykep import _dbscan
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from SpoC_Constants import data, dict_asteroids

# T_START = pk.epoch_from_iso_string("30190302T000000")  # Start and end epochs

# start_asts = [3622, 5384, 2257, 925]
# for id in start_asts:
#     # print(np.array(dict_asteroids[id][0].eph(T_START.mjd2000)[1])) # r  vom kepler-Element als np-array
#     print(dict_asteroids[id][0])

ecc = data[:,1]

print("Min Ecc: ", np.argmin(ecc), "   Max Ecc: ", np.argmax(ecc))

mitte_ecc = np.mean(ecc)
print(mitte_ecc)
grenze = 0.1*mitte_ecc
ecc_95 = []
for line in ecc:
    if (mitte_ecc - grenze) <= line <= (mitte_ecc + grenze): ecc_95.append(line)
print("Länge ecc: ", len(ecc), "    Länge ecc_95: ", len(ecc_95), "    Min ecc_95: ", np.min(ecc_95))

                