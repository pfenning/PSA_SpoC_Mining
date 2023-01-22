import numpy as np
import pykep as pk
from pykep import phasing
# from pykep import _dbscan

T_START = pk.epoch_from_iso_string("30190302T000000")  # Start and end EPOCHS
T_END = pk.epoch_from_iso_string("30240302T000000")
T_DAUER = 1827
G = 6.67430e-11  # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30  # Sun_mass (kg)
MS = 8.98266512e-2 * SM  # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS  # Mu of the Trappist-1 star
DV_per_propellant = 10000  # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30  # Maximum time to fully mine an asteroid


data = np.loadtxt("SpoC_Datensatz.txt")
dict_asteroids ={int(line[0]):  # ID
    [pk.planet.keplerian(       # Keplerian-Object
        T_START,
        (
            line[1],
            line[2],
            line[3],
            line[4],
            line[5],
            line[6]
        ),
        MU_TRAPPIST,
        G * line[7],    # mass in planet is not used in UDP, instead separate array below
        1,              # these variable are not relevant for this problem
        1.1,            # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0]))),
        line[-2],               # Mass
        int(line[-1])]          # Material
    for line in data}

asteroids = [dict_asteroids[line][0] for line in dict_asteroids]


# detecting clusters (very dense spaces)
cl = phasing.dbscan(asteroids)                                 # dbscan funktioniert nicht
cl.cluster(T_START.mjd2000, T=30)
cl.pretty()
