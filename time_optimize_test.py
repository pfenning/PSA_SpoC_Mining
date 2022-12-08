# Packages laden
import numpy as np
import pykep as pk
# from pykep import epoch
# import matplotlib.pyplot as plt
# from scipy.stats import kde


# Code spezifische Packages:
import random
import time

# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST
# Andere Module:
import time_optimize as to
import time_optimize_hookes_jeeves as hooke_jeeves
import time_optimize_NSGA2 as toNSGA2
import time_optimize_final as to_final

########################
# Zufälliger Startasteroid und zufälligem Asteroid in Umgebung
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
    
""" Hier fehlt noch eine Lösung, falls es keine Elemente in der Nähe gibt 
    z.B. Längere Flugdauer, größerer Radius
"""

# Zufälliger Asteroid aus Cluster
asteroid2 = neighb[random.randrange(0, len(neighb),1)]


print("Start:", asteroid1.name, ", Startzeitpunkt:", f'{t_opt:.1f}', "vollständige Abbauzeit: ", f'{t_opt:.1f}')
print("Anzahl Asteroiden in der Nähe für T =", T,"   =>", len(neighb))
print("Ziel:", asteroid2.name, "\n")

# Timer "starten"
time0 = time.perf_counter()
# Zeiten mit Variante 1 bestimmen (erst T, dann t)
t_minDV, T_minDV, DV_min = to.time_optimize_time_v2(asteroid1, asteroid2, t_start=t_opt, t_opt=t_opt)
time1 = time.perf_counter()
time_Variante1 = time1-time0
print("Erst T dann t_start bis 60 Tage: ", "t_start:", f"{t_minDV:2f}", "T:", f"{T_minDV:.0f}", "DV::",
      f"{DV_min:.1f}", "Berechnungsdauer:", f"{time_Variante1:.5}")

# # Zeiten mit Hooke and Jeeves
# t_minDV, T_minDV, DV_min = hooke_jeeves.optimizer_hooke_jeeves(asteroid1, asteroid2, t_start=t_opt, t_opt=t_opt)
# time2 = time.perf_counter()
# time_Hooke_Jeeves = time2 - time1
# print("Hooke and Jeeves: ", "t_start:", f"{t_minDV:2f}", "T:", f"{T_minDV:.0f}", "DV::",
#       f"{DV_min:.1f}", "Berechnungsdauer:", f"{time_Hooke_Jeeves:.5}")
#
# # Zeiten mit NSGA2 bestimmen
# t_minDV, T_minDV, DV_min = toNSGA2.time_optimize_nsga2(asteroid1, asteroid2, t_start=t_opt, t_opt=t_opt)
# time3 = time.perf_counter()
# time_NSGA2 = time3-time2
# print("NSGA2: ", "t_start:", f"{t_minDV:2f}", "T:", f"{T_minDV:.0f}", "DV::",
#       f"{DV_min:.1f}", "Berechnungsdauer:", f"{time_NSGA2:.5}")

# Zeiten mit einfacher Zeitoptimierung bestimmen
t_minDV, T_minDV, DV_min = to_final.time_optimize_time_v1(asteroid1, asteroid2, t_start=t_opt, t_opt=t_opt)
time4 = time.perf_counter()
time_final = time4-time1
print("Zeitoptimierung (nicht bis t_start=60): ", "t_start:", f"{t_minDV:2f}", "T:", f"{T_minDV:.0f}", "DV::",
      f"{DV_min:.1f}", "Berechnungsdauer:", f"{time_final:.5}")