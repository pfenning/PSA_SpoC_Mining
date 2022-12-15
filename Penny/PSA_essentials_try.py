import numpy as np
import matplotlib.pyplot as plt
import pykep as pk
from load_data import data

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
    """ Material vom potenziellen Asteroiden abrufen (ist identisch zum Index, den wir benutzen wollen)
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


def get_DV(asteroid1, asteroid2, t_start, t_flug, print_result=False):  #variante="lambert", 
    """ Berechnung von DV mit verschiedenen Varianten
        Args:
            Orbital
            Direct
            Indirect
            Lambert (default)
        i:  int
            aktueller Asteroid
        j:  int
            nächster Asteroid
    """

    # Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution

    # DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
    #       ==> TOF & t_spent geben wir vor durch Zeitoptimierung!! 

    # r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
    #t_start_rv1 = T_START.mjd2000 + t_start
    r1, v1 = asteroid1.eph(T_START.mjd2000 + t_start)
    
    # r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])
    r2, v2 = asteroid2.eph(T_START.mjd2000 + t_start + t_flug)
            
    l = pk.lambert_problem(r1=r1,r2=r2,tof=t_flug*pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0)

    DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
    DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
    DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)    
    return DV   

    if variante == "orbital":
        def DV_orbital():
            pass
    if variante == "direct":
        def DV_direct():
            pass
    if variante == "indirect":
        def DV_indirect():
            pass
    if variante == "lambert":
        def DV_lambert():
            
            # Wenn tof < 0.1, dann ist Flug zu kurz --> singular lambert solution

            # DIE ZEITVEKTOREN BRAUCHEN SCHON 2 EINTRÄGE !!! ANKUNFT & VORBEREITUNG muss bekannt sein
            #       ==> TOF & t_spent geben wir vor durch Zeitoptimierung!! 

            # r1, v1 = asteroids[asteroid1].eph(T_START.mjd2000 + t_arrival[-2] + t_spent[-2])
            r1, v1 = asteroid1.eph(T_START.mjd2000 + t_start)
            # r2, v2 = asteroids[asteroid2].eph(T_START.mjd2000 + t_arrival[-1])
            r2, v2 = asteroid2.eph(T_START.mjd2000 + t_start + t_flug)
            
            l = pk.lambert_problem(r1=r1,r2=r2,tof=tof*pk.DAY2SEC, mu=MU_TRAPPIST, cw=False, max_revs=0)

            DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
            DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
            DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)    
            return DV                                        # ACHTUNG: Hier kommen Werte wie "622902.82..." raus !!

    # else: DV_lambert()

    # def propellant_used():
    #     propellant = propellant - get_DV / DV_per_propellant  # Und hier dann prop. -8..von 1 aus gerechnet
        
# print(T_START.mjd2000)


def DV_norm(DV,norm_goal=4000):
    """ Skalierung des DV auf den Wertebereich von 0 bis 4.000
    Übergabe:
        -   DV_norm: 
                der Wert, der skaliert werden soll!
        -   norm_goal:
                Max Skalierungsgrenze (default = 4000)  
    """
    return DV/norm_goal



# ACHTUNG: CLUSTERING, FUZZY UND ZEITOPTIMIERUNG HÄNGEN ALLE VONEINANDER AB!!!

# def fuzzy(cluster, beta=20):
#     """
#     Erwartung:  Most valuable Asteroid (tank, rohstoff, masse)
#     ==> Vorher Abfrage: Wenn Tank kleiner als Grenze (<3000), nur Ast mit Treibstoff betrachten
#             wie viele Ast. mit Kraftstoff sind noch im Cluster? Wenn weniger als beta, dann direkt in Tree-search 
#             (beta hoch, tank nach wechsel wird berücksichtigt)

#     Übergabe:
#         -   cluster:
#                 Das bereits minimierte Cluster
#         -   beta:       default = 20
#                 Das sind die beta-Besten Asteroiden ausgewählt aus dem übergebenem Cluster
#     """

#     j = 0
#     if j not in visited:        # j ist der vorgeschlagene Ziel-Asteroid
#         visited.append(j)
#     else: 
#         sugg.pop(j)          # diesen Index aus den Vorschlägen löschen und fuzzy neu auswerten ohne j
#         fuzzy()


def zeitoptimierung(asteroid1, asteroid2, t_start, t_opt, print_result=False):
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
        dv_t_flug.append(get_DV(asteroid1, asteroid2, t_start, t))

    # Minimum heraussuchen
    index_min = dv_t_flug.index(min(dv_t_flug))
    t_flug_min_dv = t_flug_1[index_min]

    # Variation des Startpunktes bei gegebener Flugzeit
    # vor optimalem Starttag
    t_start_relativ_var = [-0.3, -0.2, -0.1, -0.05, 0, 0.05, 0.1, 0.2, 0.3] # An Start:  -0.3, -0.2, -0.1, -0.05, 
    t_start_var = []
    for rel in t_start_relativ_var:
        t_start_var.append(rel * t_opt)
    # Berechnung für alle Variationen t_var
    for t_var in t_start_var:
        t = t_start + t_var
        dv_t_start.append(get_DV(asteroid1, asteroid2, t, t_flug_min_dv))

    # Minimum heraussuchen
    index_min = dv_t_start.index(min(dv_t_start))
    t_start_min_dv = t_start + t_start_var[index_min]
    dv_min = dv_t_start[index_min]

    if print_result == True:
        print({"Opt Start: " + str(t_start_min_dv) + ", Opt. Flugdauer: " + str(t_flug_min_dv) + ", Minimales DV: " + str(dv_min)})

    return t_start_min_dv, t_flug_min_dv, dv_min


def abbau(bestand, material, t_aufenthalt):
    """ Berechnung des abgebauten Materials
    Übergabe:
        -   Material-Index
        -   Aufenthaltsdauer auf Planet
    """
    if material == 3:
        propellant_found = np.minimum(asteroid_masse(material), (t_aufenthalt/TIME_TO_MINE_FULLY))
        bestand[material] = np.minimum(1.0, bestand[material] + propellant_found)
    else:
        bestand[material] += np.minimum(asteroid_masse(material), (t_aufenthalt/TIME_TO_MINE_FULLY))
    return bestand



def gütemaß():
    """ Wichtig als Vergleichsfaktor für die Auswertung!!
    """
    pass





###############################
### AUF GEHTS INS UNIVERSUM
###############################

# class PSA_experiment():
#     """ Ablauf der Reise in einer Schleife:
#             1.  Clustering, dh. Datenbegrenzung
#             2.  Flugoptimierung --> gibt tof und t_spent !!!
#             3.  Vorschlag für einen optimalen nächsten Asteroiden mittels Fuzzy-Logik
#             4.  Auswahl des 2. Asteroiden --> gibt den Index 
#         Schleifenabbruchkriterien:
#             1.  Keine Zeit mehr
#             2.  Tank nicht mehr ausreichend für alle möglichen Asteroiden
#             3.  Kein Tank mehr abbaubar
#             4.  Alle Asteroiden besucht
#             5.  Ein Rohstoff ausgeschöpft --> maximale Güte erreicht
#         WICHTIG:
#                 Immer abfragen, ob das vorgegebene Zeitfenster noch eingehalten wird (Ankunftszeit - Abflugzeit <=! Zeitfenster)

#     """

#     def __init__(self, data) :
#         self.data       =   data
#         self.t_current  =   t_current
#         self.t_current_e =  t_current_e
#         self.t_left     =   t_left
#         self.t_spent    =   t_spent 
#         self.t_arrival  =   t_arrival
#         self.propellant =   propellant
#         self.asteroids  =   asteroids
#         self.visited    =   visited
#         self.sugg       =   sugg
#         self.asteroid1  =   asteroid1
#         self.asteroid2  =   asteroid2
#         self.storage_abs =  storage_abs
#         self.storage_rel =  storage_rel

#     def journey(self):
#         # asteroid1/2 mit "id" versehen. Dafür richtige Asteroiden-Objekte erstellen

#         DV = []
#         i = 0 # Start
#         while i <= 5: #int(data[-1,0]+1): 
#             self.asteroid1 = int(data[i,0])
#             visited.append(self.asteroid1)

#             # clustering_fuzzy.clustering(i, t_arrival[i], 800, 5,'orbital', 20)      # T wirklich auch 20? warum?
#             i += 1
        
#         return DV('lambert',1,2)
#         print(visited)
#         return visited


            # evtl. Flugoptimierung



    # def zeitplan(self):
    #     """ Erstellung vom Zeitplan
    #         Verwendete Größen:
    #             Arrival times:              double, days
    #                 Ankunftszeiten auf dem nächsten Planeten
    #             Mining/preparation time:    double, days
    #                 Dauer des Abbaus während Aufenthalt auf einem Planeten  --> ACHTUNG, nicht größer als 60
    #             Asteroids visited:          int
    #                 Indizes der besuchten Asteroiden
    #     """
    #     # import SpoC_Kontrolle as sp

    #     # x = sp.convert_to_chromosome([], True) #chromosome
    #     # return sp.pretty(x)

    #     def creating_x(self):
    #         x=[]
    #         return x
    #     # x.convert_to_chromosome()
    #     # x.pretty()
    #     # return x
    #     pass



# experiment = PSA_experiment(data)
