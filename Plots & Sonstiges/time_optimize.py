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
def time_optimize_time_v2(asteroid1, asteroid2, t_start, t_opt):
    """ Zeitoptimierung von Delta V mit 2 Levels. Erst Flugzeit, dann Startzeit
        Rechenaufwand: Anzahl Flugzeit-Elemente + Anzahl Startzeitpunkte (10+7=17)

        Unterschied zu v1:
        Betrachteter Startpunkt bewegt sich bis zu 60 Tage
        Auswahl des Minimums über Gewichtung der Größen Flugzeit, Abbauzeit, Spritverbrauch

        Übergabe: Asteroid 1 und 2, optimaler Startpunkt, optimale Abbauzeit auf aktuellem Asteroiden
        Rückgabe: optimaler Startpunkt, optimale Flugzeit, optimiertes DV
    """
    dv_t_flug = []
    dv_t_start = []
    # Mit der Suche wird am Tag begonnen, an dem der Start-Asteroid vollständig abgebaut ist.
    # zunächst wird nur die Flugzeit optimiert in einem Bereich von 20-30 Tagen
    # oben ist t_flug mit 30 angegeben, könnte man auch ändern
    t_flug_1 = range(5, 46, 4)

    # Variation der Flugzeit, Startpunkt fest
    for t in t_flug_1:
        dv_t_flug.append(get_dv(asteroid1, asteroid2, t_start, t))

    # Minimum für Flugzeit heraussuchen (Gewichtung Flugzeit vs. DV)
    # ******** hinzugefügt
    results_t_flug = []
    for i in range(0, len(t_flug_1)):
        # "Normierung" für ähnliche Skalierung
        # Zahlenfindung: Siehe MathTests.py
        results_t_flug.append([t_flug_1[i] / 30, dv_t_flug[i] / 2000])
    weights = np.array([0.3, 0.7])
    rank_t_flug = []
    for sol in results_t_flug:
        rank_t_flug.append(sum(weights * sol))                          # Bewertung aus gewichteter Summe

    index_min = rank_t_flug.index(min(rank_t_flug))
    # index_min = dv_t_flug.index(min(dv_t_flug))
    t_flug_min_dv = t_flug_1[index_min]

    # Variation des Startpunktes bei gegebener Flugzeit
    # vor optimalem Starttag
    t_start_relativ_var = [-0.3, -0.2, -0.1, -0.05]
    t_start_var = []
    for rel in t_start_relativ_var:
        t_start_var.append(rel * t_opt)
    # Nach optimalem Startpunkt
    t_var_after = np.arange(0, 60 - t_opt, 4)
    for t_var in t_var_after:
        t_start_var.append(t_var)
    # Berechnung für alle Variationen t_var
    for t_var in t_start_var:
        t = t_start + t_var
        dv_t_start.append(get_dv(asteroid1, asteroid2, t, t_flug_min_dv))

    # Minimum heraussuchen
    # Rang Folge bilden (da nicht unnötig lange Flugzeit gewählt werden sollte)
    results_t_start = []
    for i in range(0, len(t_start_var)):
        # "Normierung" für ähnliche Skalierung - abs(t_var) da Betrag der Abweichung von t_opt relevant
        # nur t_start, DV (t_flug bereits zuvor gewählt)
        results_t_start.append([abs(t_start_var[i]/10), dv_t_start[i]/1000])

    weights_neg_var = np.array([1.5, 0.7])
    weights_pos_var = np.array([0.3, 0.7])
    weights = weights_pos_var
    rank_t_start = []
    for i in range(0, len(results_t_start)):
        if t_start_var[i] < 0:
            weights = weights_neg_var
        else:
            weights = weights_pos_var
        rank_t_start.append(sum(weights * results_t_start[i]))  # Bewertung aus gewichteter Summe

    index_min = rank_t_start.index(min(rank_t_start))

    # Wertepaar für Index des Minimums
    t_start_min_dv = t_start + t_start_var[index_min]
    t_flug_min_dv = t_flug_1[index_min]
    dv_min = dv_t_start[index_min]

    return t_start_min_dv, t_flug_min_dv, dv_min
