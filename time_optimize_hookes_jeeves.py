
# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde

# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST

# DV berechnen
from time_optimize import getDV

# pymoo Funktionen und Klassen
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.pattern import PatternSearch
from pymoo.optimize import minimize
from pymoo.termination.default import DefaultSingleObjectiveTermination

# "Globale" Objekte asteroid1 und asteroid2 (hoffe das Funktioniert)
asteroid1 = None
asteroid2 = None


class TimeOptimizeWithHookeAndJeeves(ElementwiseProblem):

    def __init__(self, xl, xu):
        """ 
        Optimierungsproblem:
        n_obj: Spritverbrauch soll minimiert werden
        n_var: Variablen dabei sind: Flugzeit T, Starttag t_start
        
        Weitere mögliche Ziele:
        Minimierung der Flugzeit,
        Minimierung der Abweichung: absolut(t_start - t_start_opt)


        Parameters:
        xl : [t_start_min, T_min], np.array, float, int
            Lower bounds for Startingtime and Flighttime. if integer all lower bounds are equal.

        xu : [t_start_max, T_max], np.array, float, int
            Upper bounds for Startingtime and Flighttime. if integer all upper bounds are equal.
         """
        super().__init__(n_var = 2, n_obj = 1, n_ieq_constr = 0, xl = xl, xu = xu)


    def _evaluate(x, out, self):
        """
        x: [t_start, T], NumPy Arry, int, float
            t_start: Starttag des Wechsels (mjd_2000)
            T: Flugzeit
        out: Dictionary, output is written to
        """

        DV = getDV(asteroid1, asteroid2, x[0], x[1])
        
        out["F"] = [DV]



def optimizerHookeJeeves(asteroid_start, asteroid_landing, t_start, t_opt):
    """ Zeitoptimierung von Delta V mit Hooke und Jeeves in vereinfachter Form
  
        Übergabe: 
        asteroid_start: Asteroid-Objekt
            Startasteroid
        asteroid_landing: Asteroid-Objekt
            Zielasteroid
        t_start: int, float (mjd_2000)
            optimaler Startpunkt (Masse komplett abgebaut)
        t_opt: int, float
            optimale Abbauzeit auf aktuellem Asteroiden
        
        Rückgabe:
        t_minDV: int,float
            optimaler Startpunkt
        T_minDV: int, float
            optimale Flugzeit
        DV_min: int,float
            optimiertes DV
    """

    # Asteroiden festlegen
    asteroid1 = asteroid_start
    asteroid2 = asteroid_landing


    # Gültigkeitsbereich festlegen
    t_var_min = -0.3*t_opt  # Es müssen mindestens 60% abgebaut werden
    t_var_max = 60 - t_opt  # Man darf maximal 60 Tage warten
    t_start_min = t_start-t_var_min
    t_start_max = t_start-t_var_max
    T_min = 1               # Flugzeit soll nicht kürzer als T_min sein
    T_max = 100             # Flugzeit soll nicht länger als T_max Tage betragen

    # Ausgangspunkt (initial value)
    # t_start = t_start
    T = 30                  # Sollte nochmal überlegt werden
    
    # Problem erstellen
    problem = TimeOptimizeWithHookeAndJeeves([t_start_min, T_min], [t_start_max, T_max])

    # Lösungsalgorithmus
    algorithm = PatternSearch(
        [t_start, T],       # Initial Values
        delta= 0.1,         # anfägnliche & größte Schrittweite relativ zum Suchintervall (Bsp: 20< t_start < 60 => delta = 4; 1 < T < 100 => delta = 10)
        rho = 0.5,          # Verkleinerung: neue Schrittweite: delta2 = rho*delta
        # step_size = 1.0   # Nicht wirklich verstanden
    )

    # Termination Criterion
    termination = DefaultSingleObjectiveTermination(
        xtol=0.25,          # Minimale Schrittweite von 0.25 Tagen
        cvtol=1e-6,         # Convergence in Constraings - wir haben keine Constraints
        ftol=0.05,          # Minimale Änderung von 5%
        period=3,           # Betrachten der letzten 3 Iterationen
        n_max_gen=20,       # Maximale Anzahl "Generationen" - bei uns (wahrscheinlich neuer Ausgangspunkte)
        n_max_evals = 100   # Maximale Anzahl Funktionsaufrufe
    )

    # Optimize
    res = minimize(
        problem = problem,
        algorithm = algorithm,
        termination = termination,
        save_history = True,            # Kann später auskommentiert werden, nur für Testzwecke
        verbose = True,                 # print des Endergebnisses (auch auskommentieren)
        return_least_infeasible = True  # Bestmögliche Lösung zurückgeben, falls sonst nichts gefunden wird
    )

    # Lösung auslesen
    t_minDV, T_minDV = res.X
    DV_min = res.F

    # Visiualize Design Space
    print(res.history)
    # xl, xu = problem.bounds()
    # plt.figure(figsize=(7, 5))
    # plt.scatter(X[:, 0], X[:, 1], s=30, facecolors='none', edgecolors='r')
    # plt.xlim(xl[0], xu[0])
    # plt.ylim(xl[1], xu[1])
    # plt.title("Design Space")
    # plt.xlabel("Starttag")
    # plt.ylabel("Flugzeit")
    # plt.show()
    # # Visiualize Objective Space - Hier nur 1D, deshalb über Iterationen aufgetragen
    # plt.figure(figsize=(7, 5))
    # plt.scatter(F[:, 0], F[:, 1], s=30, facecolors='none', edgecolors='blue')
    # plt.title("Objective Space")
    # plt.show()

    return t_minDV, T_minDV, DV_min
