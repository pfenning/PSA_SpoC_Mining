import numpy as np
import matplotlib.pyplot as plt
import pykep as pk
# from pykep import dbscan

################
### Constants
################
T_START = pk.epoch_from_iso_string("30190302T000000")   # Start and end epochs
T_END = pk.epoch_from_iso_string("30240302T000000")
G = 6.67430e-11                                 # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30                                   # Sun_mass (kg)
MS = 8.98266512e-2 * SM                         # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS                            # Mu of the Trappist-1 star
DV_per_propellant = 10000                       # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30                         # Maximum time to fully mine an asteroid


####################
### Laufvariablen       ==> sellten in self gespeichert werden
####################
t_current = 0
t_current_e = pk.epoch(0)
t_left = 1827 - t_current

t_arrival = [0,62.34]
t_spent = [50.1,12.2] # prepping material

propellant = 1.0
asteroids = []
visited = []
sugg = []                   # hier nicht addieren, immer neu löschen...dann nicht als self, sonder in Schleifen verarbeiten?
asteroid1 = 345
asteroid2 = 654
storage_abs = []
storage_rel = []

###################
### Before start
###################
#   Loading data
data = np.loadtxt("C:/Users/ingap/OneDrive/Desktop/Uni/WiSe_22-23/PSA/PSA_SpoC_Mining/SpoC_Projekt/data/SpoC_Datensatz.txt")
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
        G * line[7],  # mass in planet is not used in UDP, instead separate array below
        1,  # these variable are not relevant for this problem
        1.1,  # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0])),
    )
    asteroids.append(p)                                                       # ACHTUNG, wirklich p schon anhängen?!?!?!
asteroid_masses = data[:, -2]
asteroid_materials = data[:, -1].astype(int)

data_fuel = []
asteroids_fuel = []
i = 0
while i < len(data):
    if data[i,-1].astype(int) == 3:
        data_fuel.append(data[i])
        i += 1
    else: i += 1
for line in data_fuel:
    p = pk.planet.keplerian(T_START,(line[1],line[2],line[3],line[4],line[5],line[6],),
        MU_TRAPPIST,
        G * line[7],  # mass in planet is not used in UDP, instead separate array below
        1,  # these variable are not relevant for this problem
        1.1,  # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0])),
    )
    asteroids_fuel.append(p)                                                       # ACHTUNG, wirklich p schon anhängen?!?!?!
asteroid_masses = data[:, -2]
asteroid_materials = data[:, -1].astype(int)





# class rumspielen:
#       STORAGE= [10,2,4,6]
#     # def __init__(self):
#     #     #self.vektor = vektor
#     #     pass     
#     def calc_minimum(vektor):
#         return(
#         STORAGE.index(np.min(vektor))
#         )
# print(rumspielen.calc_minimum(STORAGE))

# storage = []
# storage_ges = np.sum(STORAGE)
# for i in range(0,STORAGE.index(STORAGE[-1])+1):
#     storage.append(np.round(STORAGE[i]/storage_ges,3))
# print(STORAGE[1]/storage_ges)
# print(storage)


# Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution
# DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
# tof = t_arrival[-1] - t_arrival[-2] - t_spent[-2]
# r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
# r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])         
# l = pk.lambert_problem(r1=r1,r2=r2,tof=tof*pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0)
# DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
# DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
# DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)
# print(propellant - (DV / DV_per_propellant))



# def asteroid_material(i):
#     """ Material vom potentiellen Asteroiden abrufen (ist identisch zum Index, den wir benutzen wollen)
#         Parameter:
#             i:
#                 kann evtl. "self.asteroids[asteroid2]" sein!!       ACHTUNG: ASTEROID2 WIRD DURCH LAUFVARIABLE "DURCHGEREICHT"
#         Rückgabe vom Material auf Asteroid i
#     """
#     i = asteroid2
#     return data[i, -1].astype(int)
# def asteroid_masse(i):
#     """ Masse vom potentiellen Asteroiden abrufen
#         Parameter:
#             i:
#                 kann evtl. "self.asteroids[asteroid2]" sein!!        ACHTUNG: ASTEROID2 WIRD DURCH LAUFVARIABLE "DURCHGEREICHT"
#         Rückgabe:   
#             Masse von Asteroid i zwischen 0 und 1
#     """
#     return data[i, -2]
# mat_ind = asteroid_material(asteroid2)
# print(asteroid_masse(mat_ind), np.minimum(asteroid_masse(mat_ind), (t_spent[-1]/TIME_TO_MINE_FULLY)))


