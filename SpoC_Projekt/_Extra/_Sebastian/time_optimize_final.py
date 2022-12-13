# Packages laden
import numpy as np
import pykep as pk
# from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde

# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST


def get_dv(asteroid1, asteroid2, t_start, t_flug, print_result=False):
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
            Ausgabe des Ergebnisses mit print()

        Rückgabe:
        DV: float
            Delta V für berechnete Flugbahn
    """

    r1, v1 = asteroid1.eph(t_start)
    r2, v2 = asteroid2.eph(t_start + t_flug)
    # Solve the lambert problem for this flight
    l = pk.lambert_problem(
        r1=r1, r2=r2, tof=t_flug * pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0
    )
    # Compute the delta-v necessary to go there and match its velocity
    dv1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
    dv2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
    DV = np.linalg.norm(dv1) + np.linalg.norm(dv2)

    if print_result:
        print("Starttag:", f"{t_start:.0f}", "Flugzeit:", f"{t_flug:.0f}", " => Delta V =", f"{DV:.0f}")

    return DV


# ToDo: Zeitraum der Flugzeit neu definieren (z.B. auf 5-46 in 4er Schritten)
#       - Reicht Auflösung? Sonst: nach gefundenem Minimum nochmal einen halben Schritt in jede Richtung machen
def time_optimize_time_v1(asteroid1, asteroid2, t_start, t_opt):
    """ Zeitoptimierung von Delta V mit 2 Levels. Erst Flugzeit, dann Startzeit
        Rechenaufwand: Anzahl Flugzeit-Elemente + Anzahl Startzeitpunkte (10+7=17)

        Übergabe: Asteroid 1 und 2, optimaler Startpunkt, optimale Abbauzeit auf aktuellem Asteroiden
        Rückgabe: optimaler Startpunkt, optimale Flugzeit, optimiertes DV
        t_start_min_DV_ float
            Startpunkt der optimalen Konstellation
        t_flug_min_DV float
            Flugzeit der optimalen Konstellation
        dv_min float
            Minimales DV
    """
    # DVs für variable Flugzeiten t_flug_1, bzw. Variable Startpunkte t_start
    dv_t_flug = []
    dv_t_start = []
    # Mit der Suche wird am Tag begonnen, an dem der Start-Asteroid vollständig abgebaut ist.
    # zunächst wird nur die Flugzeit optimiert in einem Bereich von 20-30 Tagen
    # oben ist t_flug mit 30 angegeben, könnte man auch ändern
    t_flug_1 = range(5, 46, 4)

    # Variation der Flugzeit, Startpunkt fest
    for t in t_flug_1:
        dv_t_flug.append(get_dv(asteroid1, asteroid2, t_start, t))

    # Minimum heraussuchen
    index_min = dv_t_flug.index(min(dv_t_flug))
    t_flug_min_dv = t_flug_1[index_min]

    # Variation des Startpunktes bei gegebener Flugzeit
    # vor optimalem Starttag
    t_start_relativ_var = [-0.3, -0.2, -0.1, -0.05, 0, 0.05, 0.1, 0.2, 0.3]
    t_start_var = []
    for rel in t_start_relativ_var:
        t_start_var.append(rel * t_opt)
    # Berechnung für alle Variationen t_var
    for t_var in t_start_var:
        t = t_start + t_var
        dv_t_start.append(get_dv(asteroid1, asteroid2, t, t_flug_min_dv))

    # Minimum heraussuchen
    index_min = dv_t_start.index(min(dv_t_start))
    t_start_min_dv = t_start + t_start_var[index_min]
    dv_min = dv_t_start[index_min]

    return t_start_min_dv, t_flug_min_dv, dv_min
