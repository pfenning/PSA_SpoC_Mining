# Packages laden
import numpy as np
import pykep as pk
# from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde

# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST

# DV berechnen
from time_optimize import get_dv

# pymoo Funktionen und Klassen
from pymoo.core.problem import ElementwiseProblem
# Algo
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
# Optimize
from pymoo.optimize import minimize
# Termination
from pymoo.termination.default import DefaultSingleObjectiveTermination

# "Globale" Objekte 
# asteroid1 und asteroid2
asteroid_trip = [asteroids[0], asteroids[0]]
# Optimaler Starttag
t_start_opt = 0


class TimeOptimizeWithNSGA2(ElementwiseProblem):
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
            Lower bounds for Starting-Time and Flight-Time. if integer all lower bounds are equal.

        xu : [t_start_max, T_max], np.array, float, int
            Upper bounds for Starting-Time and Flight-Time. if integer all upper bounds are equal.
        """
        super().__init__(n_var=2, n_obj=3, n_ieq_constr=0, xl=xl, xu=xu)

    def _evaluate(self, x, out, *args, **kwargs):
        """
        x: [t_start, T], NumPy Array, int, float
            t_start: Starttag des Wechsels (mjd_2000)
            T: Flugzeit
        out: Dictionary, output is written to
        """

        dv = get_dv(asteroid_trip[0], asteroid_trip[1], x[0], x[1]) / 1000
        t_var = abs(x[0] - t_start_opt) / 30
        t_opt = x[1] / 30

        out["F"] = [t_var, t_opt, dv]


def time_optimize_nsga2(asteroid_start, asteroid_landing, t_start, t_opt):
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
        t_start_min_dv: int,float
            optimaler Startpunkt
        t_flug_min_dv: int, float
            optimale Flugzeit
        dv_min: int,float
            optimiertes DV
    """

    # Asteroiden festlegen
    asteroid_trip[0] = asteroid_start
    asteroid_trip[1] = asteroid_landing
    # Optimale Startzeit speicher
    t_start_opt = t_start

    # Gültigkeitsbereich festlegen
    t_var_min = -0.3 * t_opt  # Es müssen mindestens 60% abgebaut werden
    t_var_max = 60 - t_opt  # Man darf maximal 60 Tage warten
    t_start_min = t_start - t_var_min
    t_start_max = t_start + t_var_max
    t_flug_min = 1  # Flugzeit soll nicht kürzer als t_flug_min sein
    t_flug_max = 60  # Flugzeit soll nicht länger als t_flug_max Tage betragen

    # Ausgangspunkt (initial value)
    # t_start = t_start
    T = 30  # Sollte nochmal überlegt werden

    # Problem erstellen
    problem = TimeOptimizeWithNSGA2(np.array([t_start_min, t_flug_min]), np.array([t_start_max, t_flug_max]))

    # Lösungsalgorithmus
    algorithm = NSGA2(pop_size=10)  # Anzahl der Population und der Lösungen am Ende

    # Termination Criterion
    termination = DefaultSingleObjectiveTermination(
        xtol=0.025,
        # Minimale Schrittweite von --* Intervall Tage
        # (z.B. xtol=0.025: Starttag [20-60] => Grenze: 1 Tag; Flugzeit: 1-100 Tage => 2.5 Tage)
        cvtol=1e-6,  # Convergence in Constraings - wir haben keine Constraints
        ftol=0.02,  # Minimale Änderung von --%
        period=4,  # Betrachten der letzten -- Iterationen
        n_max_gen=10,  # Maximale Anzahl "Generationen" - bei uns (wahrscheinlich neuer Ausgangspunkte)
        n_max_evals=150  # Maximale Anzahl Funktionsaufrufe
    )

    # Optimize
    res = minimize(
        problem,
        algorithm,
        termination,
        save_history=False,  # Kann später auskommentiert werden, nur für Testzwecke
        verbose=True,  # print des Endergebnisses (auch auskommentieren)
        return_least_infeasible=True  # Bestmögliche Lösung zurückgeben, falls sonst nichts gefunden wird
    )

    # Lösungsset auslesen
    # t_start_min_dv, t_flug_min = res.X
    # t_flug_min_dv = res.F[2]*30
    # dv_min = res.F[0]*1000

    print(res.X)
    print(res.F)

    # Multi-Criteria Decision-Making - make it easy
    weights = np.array([0.2, 0.3, 0.5])  # t_start, T, DV
    rank = []
    for sol in res.F:
        rank.append(sum(weights * sol))

    opt_ind = rank.index(min(rank))
    t_start_min_dv, t_flug_min_dv = res.X[opt_ind]
    dv_min = res.F[opt_ind][2] * 1000
    # print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
    return t_start_min_dv, t_flug_min_dv, dv_min
