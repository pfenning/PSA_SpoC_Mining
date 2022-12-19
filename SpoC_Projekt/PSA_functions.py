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
# t_spent = [0] # prepping material
# t_start = [0]
# t_arrival = [0]
# t_current = [0]
# t_current_e = pk.epoch(0)
# t_left = 1827 - t_current[-1]

# propellant = 1.0
# asteroids = []
# visited = []
# sugg = []                   # hier nicht addieren, immer neu löschen...dann nicht als self, sonder in Schleifen verarbeiten?
# asteroid1 = 0
# asteroid2 = 1
# storage_abs = []
# storage_rel = []


###################
### Before start
###################
# #   Loading data
data = np.loadtxt("C:/Users/ingap/OneDrive/Desktop/Uni/WiSe_22-23/PSA/PSA_SpoC_Mining/SpoC_Projekt/data/SpoC_Datensatz.txt")
# for line in data:
#     p = pk.planet.keplerian(
#         T_START,
#         (
#             line[1],
#             line[2],
#             line[3],
#             line[4],
#             line[5],
#             line[6],
#         ),
#         MU_TRAPPIST,
#         G * line[7],  # mass in planet is not used in UDP, instead separate array below
#         1,  # these variable are not relevant for this problem
#         1.1,  # these variable are not relevant for this problem
#         "Asteroid " + str(int(line[0])),
#     )
#     asteroids.append(p)                                                       # ACHTUNG, wirklich p schon anhängen?!?!?!
# asteroid_masses = data[:, -2]
# asteroid_materials = data[:, -1].astype(int)


##########################
### Essential functions
##########################
def asteroid_masse(i):
    """ Masse vom potentiellen Asteroiden abrufen
        Parameter:
            i:
                kann evtl. "asteroids[asteroid2]" sein!!        ACHTUNG: ASTEROID2 WIRD DURCH LAUFVARIABLE "DURCHGEREICHT"
        Rückgabe:   
            Masse von Asteroid i zwischen 0 und 1
    """
    return data[i, -2]

def asteroid_material(i):
    """ Material vom potentiellen Asteroiden abrufen (ist identisch zum Index, den wir benutzen wollen)
        Parameter:
            i:
                kann evtl. "asteroids[asteroid2]" sein!!       ACHTUNG: ASTEROID2 WIRD DURCH LAUFVARIABLE "DURCHGEREICHT"
        Rückgabe vom Material auf Asteroid i
    """
    return data[i, -1].astype(int)

# def relative_material_stock():
#     """ Bestand der bisher gesammelten Materialien (absolut und relativ) 
#         Aufbau:
#             Material 0-2:   storage_abs[0:2]
#             Material 3:     storage_abs[3]      # = PROPELLANT
#         Rückgabe:
#             storage_rel:
#                 Vektor mit dem aktuellen, relativen(!) Bestand aller Materialien
#     """
#     storage_ges = np.sum(storage_abs)
#     for i in range(0,storage_abs.index(storage_abs[-1])+1):
#         storage_rel.append(np.round(storage_abs[i]/storage_ges,3))
#     return storage_rel

# def minimal_material():
#     """ Gibt einem das Material wieder, welches bisher am wenigsten abgebaut wurde
#         Rückgabe:
#             STORAGE_min:
#                 Menge von Material mit absolutem Minimum
#             storage_min:
#                 Menge von Material mit relativem Minimum
#     """
#     min_storage_abs = np.min(storage_abs)
#     min_storage_rel = np.min(storage_rel)
#     return min_storage_abs, min_storage_rel

# def index_minimal_material():
#     """ Gibt einem den Index des Materials, welches bisher am wenigsten abgebaut wurde
#         Rückgabe:
#             STORAGE_min:
#                 Index von Material mit absolutem Minimum
#             storage_min:
#                 Index von Material mit relativem Minimum
#     """
#     min_storage_abs_ind = storage_abs.index(np.min(storage_abs))
#     min_storage_rel_ind = storage_rel.index(np.min(storage_rel))
#     return min_storage_abs_ind, min_storage_rel_ind








def tof(t_arrival, t_spent):
    """ Berechnet die Flugzeit von Asteroid 1 zu Asteroid 2

        ACHTUNG: Sicherheit einbauen, dass t_arrival[-1] > t_spent[-2]!! Sonst ist tof negativ!
    """
    return (t_arrival[-1] - (t_arrival[-2] + t_spent[-2]))








# def get_DV(asteroid1, asteroid2, t_start, t_flug, print_result=False):  #variante="lambert", 
#     """ Berechnung von DV mit verschiedenen Varianten
#         Args:
#             Orbital
#             Direct
#             Indirect
#             Lambert (default)
#         i:  int
#             aktueller Asteroid
#         j:  int
#             nächster Asteroid
#     """
#     # Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution
#     # DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
#     #       ==> TOF & t_spent geben wir vor durch Zeitoptimierung!! 
#     # r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
#     #t_start_rv1 = T_START.mjd2000 + t_start
#     r1, v1 = asteroid1.eph(T_START.mjd2000 + t_start)    
#     # r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])
#     r2, v2 = asteroid2.eph(T_START.mjd2000 + t_start + t_flug)            
#     l = pk.lambert_problem(r1=r1,r2=r2,tof=t_flug*pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0
#     DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
#     DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
#     DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)    
#     return DV   

#     if variante == "orbital":
#         def DV_orbital():
#             pass
#     if variante == "direct":
#         def DV_direct():
#             pass
#     if variante == "indirect":
#         def DV_indirect():
#             pass
#     if variante == "lambert":
#         def DV_lambert():            
#             # Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution
#             # DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
#             #       ==> TOF & t_spent geben wir vor durch Zeitoptimierung!! 
#             # r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
#             r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_start)
#             # r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])
#             r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_start + t_flug)            
#             l = pk.lambert_problem(r1=r1,r2=r2,tof=tof*pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0)
#             DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
#             DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
#             DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)    
#             return DV                                        # ACHTUNG: Hier kommen Werte wie "622902.82..." raus !!
#     # else: DV_lambert()
#     # def propellant_used():
#     #     propellant = propellant - get_DV / DV_per_propellant  # Und hier dann prop. -8..von 1 aus gerechnet
# # print(T_START.mjd2000)





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




def DV_norm(DV,norm_goal=4000):
    """ Skalierung des DV auf den Wertebereich von      0 bis 4.000   
    Übergabe:
        -   DV_norm: 
                der Wert, der skaliert werden soll!
        -   norm_goal:
                Max Skalierungsgrenze (default = 4000)  
    """
    return DV/norm_goal








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



def clustering(knn, var, radius):
    neighb, neighb_ids, neighb_dis = knn.find_neighbours(var, query_type='ball', r=radius)
    neighb = list(neighb)
    neighb_ids = list(neighb_ids)
    return neighb, neighb_ids

def clustering_fuel(knn_fuel, var, radius):
    neighb_fuel, neighb_fuel_ids, neighb_fuel_dis = knn_fuel.find_neighbours(var, query_type='ball', r=radius)
    neighb_fuel = list(neighb_fuel)
    neighb_fuel_ids = list(neighb_fuel_ids)
    return neighb_fuel, neighb_fuel_ids






def abbau(bestand,ast_id, material, t_aufenthalt):
    """ Berechnung des abgebauten Materials
    Übergabe:
        -   Material-Index
        -   Aufenthaltsdauer auf Planet
    """
    if material == 3:
        propellant_found = np.minimum(asteroid_masse(ast_id), (t_aufenthalt/TIME_TO_MINE_FULLY))
        bestand[material] = np.minimum(1.0, bestand[material] + propellant_found)
    else:
        bestand[material] += np.minimum(asteroid_masse(ast_id), (t_aufenthalt/TIME_TO_MINE_FULLY))
    return bestand




