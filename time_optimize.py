# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde



# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST



def getDV(asteroid1, asteroid2, t_start, T_flug, printResult = False):
    """ Berechnung des approximierten Delta V mithilfe des Lambert-Problems
    
        Übergabe:
        asteroid1: Asteroid Objekt
            Start-Asteroid
        asteroid2: Asteroid Objekt
            Lande-Asteroid
        t_start: int, float (mjd_2000)
            Startzeitpunkt
        T: int, float
            Flugzeit
        printResult: boolean
            Ausgabe des Egebnisse mit print()

        Rückgabe:
        DV: float
            Delta V für berechnete Flugbahn
    """

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

    if printResult:
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





