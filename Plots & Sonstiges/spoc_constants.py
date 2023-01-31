# Packages laden
import numpy as np
import pykep as pk
import matplotlib.pyplot as plt

################
### Constants
################

# Start and end epochs
T_START = pk.epoch_from_iso_string("30190302T000000")
T_END = pk.epoch_from_iso_string("30240302T000000")

# Cavendish constant (m^3/s^2/kg)
G = 6.67430e-11

# Sun_mass (kg)
SM = 1.989e30

# Mass and Mu of the Trappist-1 star
MS = 8.98266512e-2 * SM
MU_TRAPPIST = G * MS

# DV per propellant [m/s]
DV_per_propellant = 10000

# Maximum time to fully mine an asteroid
TIME_TO_MINE_FULLY = 30

# Loading the asteroid data
data = np.loadtxt("Asteroidengürtel.txt")
asteroids = []
for line in data:
    p = pk.planet.keplerian(
        T_START,
        (
            line[1],
            line[2],
            line[3],
            line[4],
            line[5],
            line[6],
        ),
        MU_TRAPPIST,
        G * line[7],  # mass_v in planet is not used in UDP, instead separate array below
        1,  # these variable are not relevant for this problem
        1.1,  # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0])),
    )
    asteroids.append(p)

# And asteroids' masses and material type
asteroid_masses = data[:, -2]
asteroid_materials = data[:, -1].astype(int)
