# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde


# Code spezifische Packages:
import random

# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST
# Andere Midule:
import time_optimize as to
import time_optimize_hookes_jeeves as hooke_Jeeves



########################
# Test der Zeitoptimierung mit zufälligem Startasteroid und zufälligem Asteroid in Umgebung
########################
id_1 = random.randrange(0, len(asteroids), 1)
asteroid1 = asteroids[id_1]
t_opt = asteroid_masses[id_1]*30

# Nachbarn innerhalb von 1000m finden für optimalen Startzeitpunkt (Asteroid komplett abgebaut)
t_start =  0 + t_opt
T = 30
knn = pk.phasing.knn(asteroids, t=t_start, metric='orbital', T=T)
neighb, neighb_ids, _ = knn.find_neighbours(asteroid1, query_type='ball', r=1500)


# for i in range(len(neighb)):
#     print(f'{neighb_ids[i]:10}')

# Asteroid 1 aus Array entfernen (Zunächst muss Tuple in List umgewandelt werden...)
neighb = list(neighb)
neighb.remove(asteroid1)
neighb_ids = list(neighb_ids)
neighb_ids.remove(id_1)
    
""" Hier fehlt noch eine Lösung, falss es keine Elemente in der Nähe gibt 
    z.B. Längere Flugdauer, größerer Radius
"""

# Zufälliger Asteroid aus Cluster
asteroid2 = neighb[random.randrange(0, len(neighb),1)]


print("Start:", asteroid1.name, ", Startzeitpunkt:", f'{t_opt:.1f}', "vollständige Abbauzeit: ", f'{t_opt:.1f}')
print("Anzahl Ansteroiden in der Nähe für T =", T,"   =>", len(neighb))
print("Ziel:", asteroid2.name, "\n")

# Zeiten mit Variante 1 bestimmen (erst T, dann t)
# t_minDV, T_minDV, DV_min = to.optimizeTimeV1(asteroid1, asteroid2, t_start=t_opt, t_opt=t_opt)

# Zeiten mit Hooke and Jeeves
t_minDV, T_minDV, DV_min = hooke_Jeeves.optimizerHookeJeeves(asteroid1, asteroid2, t_start=t_opt, t_opt=t_opt)

print("Die optimalen Parameter mit Variante 1 haben sich ergeben zu:")
print("t_start:", f"{t_minDV:2f}")
print("T:", f"{T_minDV:.0f}")
print("DV::", f"{DV_min:.1f}")


