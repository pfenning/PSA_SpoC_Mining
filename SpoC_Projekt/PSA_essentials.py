import numpy as np
import matplotlib.pyplot as plt
import pykep as pk

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
### Laufvariablen       ==> sollten in self gespeichert werden
####################
t_spent = [0] # prepping material
t_start = [0]
t_arrival = [0]
t_current = [0]
t_current_e = pk.epoch(0)
t_left = 1827 - t_current

propellant = 1.0
asteroids = []
visited = []
sugg = []                   # hier nicht addieren, immer neu löschen...dann nicht als self, sonder in Schleifen verarbeiten?
asteroid1 = 0
asteroid2 = 1
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
# asteroid_masses = data[:, -2]
# asteroid_materials = data[:, -1].astype(int)




##############
### LETS GO
##############
import PSA_essentials_try

""" Ablauf der Reise in einer Schleife:
        1.  Clustering, dh. Datenbegrenzung
        2.  Flugoptimierung --> gibt tof und t_spent !!!
        3.  Vorschlag für einen optimalen nächsten Asteroiden mittels Fuzzy-Logik
        4.  Auswahl des 2. Asteroiden --> gibt den Index 
    Schleifenabbruchkriterien:
        1.  Keine Zeit mehr
        2.  Tank nicht mehr ausreichend für alle möglichen Asteroiden
        3.  Kein Tank mehr abbaubar
        4.  Alle Asteroiden besucht
        5.  Ein Rohstoff ausgeschöpft --> maximale Güte erreicht
    WICHTIG:
            Immer abfragen, ob das vorgegebene Zeitfenster noch eingehalten wird (Ankunftszeit - Abflugzeit <=! Zeitfenster)

"""

