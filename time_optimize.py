# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde



# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST

# Code spezifische Packages:
import random


def getDV(asteroid1, asteroid2, t_start, T_flug):
    """Übergeben werden der Startasteroid, der Zielasteroid, die Startzeit und die Flugzeit.
    Zurückgegeben wird das für den Flug benötigte Delta V"""

    r1,v1 = asteroid1.eph(t_start)
    r2,v2 = asteroid2.eph(t_start+T_flug)
    # Solve the lambert problem for this flight
    l = pk.lambert_problem(
        r1=r1, r2=r2, tof=T_flug * pk.DAY2SEC, mu= MU_TRAPPIST, cw=False, max_revs=0
        )
    # Compute the delta-v necessary to go there and match its velocity
    DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
    DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
    DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)

    print("Starttag:", f"{t_start:.0f}", "Flugzeit:", f"{T_flug:.0f}", " => Delta V =", f"{DV:.0f}")

    return DV



def optimizeTimeV1(asteroid1, asteroid2, t_start, t_opt):
    """ Zeitoptimierung von Delta V mit 2 Levels. Erst Flugzeit, dann Startzeit
        Rechenaufwand: Anzahl Flugzeit-Elemente + Anzahl Startzeitpunkte (10+7=17)

        Übergabe: Asteroid 1 und 2, optimaler Startpunkt, optimale Abbauzeit auf aktuellem Asteroiden
        Rückgabe: optimaler Startpunkt, optimale Flugzeit, optimiertes DV
    """
    DV_T = []
    DV_tstart = []
    # Mit der Suche wird da begonnen, wo der Start-Asteroid vollständig abgebaut ist
    # Zunächst wird nur die Flugzeit optimiert in einem Bereich von 20-30 Tagen - Oben ist T mit 30 angegeben; könnte man auch ändern
    T_flug_1 = range(20,60,4)

    # Variation der Flugzeit, Startpunkt fest
    for t in T_flug_1:
        DV_T.append(getDV(asteroid1, asteroid2, t_start, t))

    # Minimum raussuchen
    index_min = DV_T.index(min(DV_T))
    T_minDV = T_flug_1[index_min]
    DV_min = DV_T[index_min]
    # print("Bestes Wertepaar: Flugzeit=", T_minDV, "DV=", DV_min)


    # Variation des Startpunktes bei gegebener Flugzeit
    t_start_relativ_var = [-0.3, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.3]
    t_start_var = []
    for rel in t_start_relativ_var: t_start_var.append(rel*t_start)
    for t_var in t_start_var:
        t = t_start + t_var
        DV_tstart.append(getDV(asteroid1, asteroid2, t, T_minDV))

    # Minimum raussuchen
    index_min = DV_tstart.index(min(DV_tstart))
    t_minDV = t_start - t_start_var[index_min]
    DV_min = DV_tstart[index_min]

    return t_minDV, T_minDV, DV_min



def optimizerHookeJeeves(asteroid1, asteroid2, t_start, t_opt):
    """ Zeitoptimierung von Delta V mit Hooke und Jeeves in vereinfachter Form

        Übergabe: Asteroid 1 und 2, optimaler Startpunkt, optimale Abbauzeit auf aktuellem Asteroiden
        Rückgabe: optimaler Startpunkt, optimale Flugzeit, optimiertes DV
    """
    # Gültigkeitsbereich festlegen
    t_var_min = -0.3*t_opt  # Es müssen mindestens 60% abgebaut werden
    t_var_max = 60 - t_opt  # Man darf maximal 60 Tage warten
    T_min = 1               # Flugzeit soll nicht kürzer als T_min sein
    T_max = 100             # Flugzeit soll nicht länger als T_max Tage betragen



    return t_minDV, T_minDV, DV_min



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
t_minDV, T_minDV, DV_min = optimizeTimeV1(asteroid1, asteroid2, t_start=t_opt, t_opt=t_opt)

print("Die optimalen Parameter mit Variante 1 haben sich ergeben zu:")
print("t_start:", f"{t_minDV:2f}")
print("T:", f"{T_minDV:.0f}")
print("DV::", f"{DV_min:.1f}")


