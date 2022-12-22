import numpy as np
import matplotlib.pyplot as plt
import pykep as pk
from pykep import phasing
from scipy.stats import kde
import random

################
### Constants
################
T_START = pk.epoch_from_iso_string("30190302T000000")   # Start and end epochs
T_END = pk.epoch_from_iso_string("30240302T000000")
T_DAUER = 1827
G = 6.67430e-11                                 # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30                                   # Sun_mass (kg)
MS = 8.98266512e-2 * SM                         # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS                            # Mu of the Trappist-1 star
DV_per_propellant = 10000                       # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30                         # Maximum time to fully mine an asteroid


##############
### LETS GO
##############
import PSA_functions as psa

""" Ablauf der Reise in einer Schleife:
        1.  Clustering, dh. Datenbegrenzung
        2.  Flugoptimierung --> gibt tof und t_spent !!!
        3.  Vorschlag für einen optimalen nächsten Asteroiden mittels Fuzzy-Logik
        4.  Auswahl des 2. Asteroiden --> gibt den Index 
    Schleifenabbruchkriterien:
        1.  Keine Zeit mehr
        2.  Tank nicht mehr ausreichend für alle möglichen Asteroiden
        3.  Kein Tank mehr abbaubar
        4.  Alle Asteroiden besucht
        5.  Ein Rohstoff ausgeschöpft --> maximale Güte erreicht
    WICHTIG:
            Immer abfragen, ob das vorgegebene Zeitfenster noch eingehalten wird (Ankunftszeit - Abflugzeit <=! Zeitfenster)

"""
#################
# ASTEROIDS:  Creating lists with indices of asteroids
#################

# Lists to be created
asteroids_kp = []
asteroids_idx = []
asteroids_fuel_kp = []
asteroids_fuel_idx = []


# Loading data as keplerian elements (planets) in an "array"
# data = np.loadtxt("C:/Users/ingap/OneDrive/Desktop/Uni/WiSe_22-23/PSA/PSA_SpoC_Mining/SpoC_Projekt/data/SpoC_Datensatz.txt")
# data = open('SpoC_Datensatz.txt', 'r')
data = np.loadtxt("SpoC_Datensatz.txt")

for line in data:
    p = pk.planet.keplerian(
        T_START,
        (
            line[1],
            line[2],
            line[3],
            line[4],
            line[5],
            line[6],
        ),
        MU_TRAPPIST,
        G * line[7],  # mass in planet is not used in UDP, instead separate array below
        1,  # these variable are not relevant for this problem
        1.1,  # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0])),
    )
    if line[-1] == 3:
        asteroids_fuel_idx.append(int(line[0]))
        asteroids_fuel_kp.append(p)
    asteroids_idx.append(int(line[0]))
    asteroids_kp.append(p)


# SONSTIGES, NOCH SORTIEREN
i_start = random.randrange(0, len(asteroids_idx),1)
i_start = 9953

asteroid_1 = asteroids_idx[i_start]        # Der erste Asteroid der Liste wird ausgewählt
asteroid_1_idx = i_start
if data[i_start,1].astype(int) == 3: 
    asteroids_idx.remove(i_start)
    asteroids_fuel_idx.remove(i_start)
else:
    asteroids_idx.remove(i_start)




###########
### TIME
###########

# Startwerte
t_start = [0]
t_aktuell = [t_start] # Seien wir 0 Tage auf dem ersten Asteroiden stehen geblieben bis 1. Abflug
t_opt = 30
# t_aktuell_e = pk.epoch(t_aktuell[-1])

# Laufvariablen
ERG_t_arr = [0.0]   # double, Ankunftszeit
ERG_t_m = []        # double, Verweildauer
ERG_a = [i_start]   # int, besuchte Asteroiden


###########
### GÜTE
###########

propellant = 1.0 # entspricht DV_max = 10.000

bestand = [0.0, 0.0, 0.0, propellant]
bestand_rel = [0.0, 0.0, 0.0, 0.0]

verf = np.array([0.03, 0.4, 0.42, 0.15])  # ToDo: Verfügbarkeit berechnen

from _Extra._Mathias.fuzzy_system import FuzzySystem
my_system = FuzzySystem(verf.min(), verf.max(), resolution=0.05)


# while var <= i_start+grenze:
print("Start-Asteroid: ", i_start)

while len(ERG_a) <= 30:     # <= 10000
    asteroid_1_idx = ERG_a[-1]                  # aktueller Asteroid
    asteroid_1_kp = asteroids_kp[asteroid_1_idx]   # aktueller Asteroid inkl Kepler-Inofs

    #################################
    ### SCHRITT 1:      Clustering      JEDER 2. TANKFÜLLUNG
    #################################
    # Annahme:  Wir befinden uns auf einem Asteroiden
    i = 0
    # dv_min_2 = []
    score_2 = []
    flight_opt = []

    # Optimale Zeit für die Zeitoptimierung anpassen
    if ERG_a[-1] == i_start: t_opt = 0
    else: t_opt = psa.asteroid_masse(asteroid_1_idx)*30

    # Clustering abhängig vom vorhandenen Tank
    if bestand[-1] < 0.6:

        # Lister mit Asteroiden in Keppler-Form!! 
        asteroids_fuel_kp_copy = [asteroids_kp[id] for id in asteroids_fuel_idx]
        asteroids_fuel_kp_copy.append(asteroids_kp[asteroid_1_idx])

        knn_fuel = phasing.knn(asteroids_fuel_kp_copy, ERG_t_arr[-1]+t_opt, 'orbital', T=30) #    ACHTUNG: Referenzradius & -geschw. sind Gürtelabhängig!
        radius = 4000
        neighb_fuel_idx = psa.clustering_fuel(knn_fuel, asteroids_kp, asteroid_1_idx, radius) # neighb_fuel, neighb_fuel_idx
        print("Nachbarn: ", neighb_fuel_idx)

        while i < len(neighb_fuel_idx):
            asteroid_2_idx = neighb_fuel_idx[i]
            asteroid_2_kp = asteroids_kp[neighb_fuel_idx[i]]
            t_abflug_opt_, t_flug_min_dv_, dv_min_ = psa.time_optimize_time_v2(asteroid_1_kp, asteroid_2_kp, ERG_t_arr[-1] + t_opt, t_opt)
            score = my_system.calculate_score(
                t_n= bestand[-1]-dv_min_,
                delta_v=dv_min_,
                bes=bestand[psa.asteroid_material(asteroid_2_idx)],
                verf=verf[psa.asteroid_material(asteroid_2_idx)],
                mas=psa.asteroid_masse(asteroid_2_idx))
            # dv_min_2.append(dv_min_)
            score_2.append(score)
            flight_opt.append([t_abflug_opt_, t_flug_min_dv_, dv_min_])
            i += 1

        # dv_min_2_intermediate_INDEX = dv_min_2.index(min(dv_min_2))
        # asteroid_2_idx = neighb_fuel_idx[dv_min_2_intermediate_INDEX]
        score_2_idx = score_2.index(max(score_2))
        t_abflug_opt_, t_flug_min_dv_, dv_min_ = flight_opt[score_2_idx]
        asteroid_2_idx = neighb_fuel_idx[score_2_idx]
        asteroid_2_kp = asteroids_kp[asteroid_2_idx]
        print("Verbrauchtes DV: ", dv_min_)

    else:
        asteroids_kp_copy = [asteroids_kp[id] for id in asteroids_fuel_idx]
        asteroids_kp_copy.append(asteroids_kp[asteroid_1_idx])

        knn = phasing.knn(asteroids_kp_copy, ERG_t_arr[-1]+t_opt, 'orbital', T = 30) #                                            ACHTUNG: Referenzradius & -geschw. sind Gürtelabhängig!
        radius = 4000
        neighb_idx = psa.clustering(knn, asteroids_kp, asteroid_1_idx, radius) # neighb, neighb_idx

        while i < len(neighb_idx):
            asteroid_2_idx = neighb_idx[i]
            asteroid_2_kp = asteroids_kp[neighb_idx[i]]
            t_abflug_opt_, t_flug_min_dv_, dv_min_ = psa.time_optimize_time_v2(asteroid_1_kp, asteroid_2_kp, ERG_t_arr[-1] + t_opt, t_opt)
            score = my_system.calculate_score(
                t_n=bestand[-1] - dv_min_,
                delta_v=dv_min_,
                bes=bestand[psa.asteroid_material(asteroid_2_idx)],
                verf=verf[psa.asteroid_material(asteroid_2_idx)],
                mas=psa.asteroid_masse(asteroid_2_idx))
            # dv_min_2.append(dv_min_)
            score_2.append(score)
            flight_opt.append([t_abflug_opt_, t_flug_min_dv_, dv_min_])
            i += 1

        # dv_min_2_intermediate_INDEX = dv_min_2.index(min(dv_min_2))
        # asteroid_2_idx = neighb_fuel_idx[dv_min_2_intermediate_INDEX]
        score_2_idx = score_2.index(max(score_2))
        t_abflug_opt_, t_flug_min_dv_, dv_min_ = flight_opt[score_2_idx]
        asteroid_2_idx = neighb_idx[score_2_idx]
        asteroid_2_kp = asteroids_kp[asteroid_2_idx]
        print("Verbrauchtes DV: ", dv_min_)

        # PRÜFUNG von DV
        # print("get_DV: ", psa.get_dv(asteroid_1_kp, asteroid_2_kp, t_abflug_opt_, t_flug_min_dv_))
        # print("Alle möglichen DV: ", dv_min_2)
        # print("Notw DV: ", min(dv_min_2))



# ACHTUNG: WENN CLUSTER DURCH BEDINGUNG LEER, DANN IST "dv_min_2" LEER !!! 
# DAS IST ZU VERMEIDEN!!!!!! => Was dann ?!?!?!




    ###################################
    # SCHRITT 2:        Fuzzy-Logic
    ###################################
    # Annahme:  Cluster wurde gebildet und man hat aus 10.000 nur noch 300 (=beta) mögliche/sinnvolle Asteroiden zur Auswahl
    # Cluster nicht abhängig von DV, deswegen wird Fuzzy zustätzlich dafür benutzt
    # ERGEBNIS: beta-Beste Asteroiden werden durch Fuzzy vorgeschlagen




    # calculate score

    ###################################
    # SCHRITT 3:        Tree-Search
    ###################################
    # Annahmen: Fuzzy hat beta-Beste Asteroiden vorgeschlagen
    # ERGEBNIS: TS liefert den BESTEN Asteroiden!!

    # Dieser Teil existiert noch nicht  -->     dh. man wählt einen besten Asteroiden aus fürs Erste

    # next_best_ast = var+1 # Aktuell laufe ich einfach nur durch mein eigenes Cluster durch
    # visited_ind.append(next_best_ast)
    



    #######################################
    # SCHRITT 4:        Zeitoptimierung
    #######################################
    # Annahme:  Aus dem Cluster wurden beta-Beste und daraus dann der beste Asteroid ausgewählt
    # ERGEBNIS: 
    #   -   Zeitoptimierung:
    #           -   Optimaler Abflugzeitpunkt bzgl. Abbau, 
    #           - optimale Flugzeit
    #           - optimiertes DV werden vorgeschlagen
    #   -   Lösungsvektoren aktualisieren
    #           1.  ERG_t_arr:      Ankunftszeitpunkte auf neuem Planeten
    #           2.  t_aufenthalt:   Dauer auf dem aktuellen Planeten (Abflug minus letzte Ankunft)
    #           3.  a_besucht:      Die Indizes der besuchten Planeten, damit keine doppelten Besuche


    
    # Lösungsvektoren:
    ERG_t_m.append(t_abflug_opt_ - ERG_t_arr[-1])
    ERG_t_arr.append(t_abflug_opt_ + t_flug_min_dv_)
    ERG_a.append(asteroid_2_idx)

    # if ERG_a[-1] == i_start: 
    #     ERG_t_m.append(t_abflug_opt_)
    #     ERG_t_arr.append(t_abflug_opt_ + t_flug_min_dv_)
    # else: 
    #     ERG_t_m.append(t_abflug_opt_ - ERG_t_arr[-1])
    #     ERG_t_arr.append(ERG_t_arr[-1] + ERG_t_m[-1] + t_flug_min_dv_)
    # ERG_a.append(asteroid2_id)

    # print("t_m: ", ERG_t_m)
    # print("t_arr: ", ERG_t_arr)
    # print("a: ", ERG_a)

    #######################################
    # SCHRITT 5:        Abbau und Flug
    #######################################
    # Annahme:  Abbau ist fertig oder wird abgebrochen. Dh man befindet sich an Abflugzeit "t_abflug_opt"
    # ERGEBNIS:
    #   -   Bestands-Vektoren aktualisieren
    #   -   Gütemaß berechnen
    #   -   Tank aktualisieren
    #
    # Weitere Bedingungen:
    #   - Wenn t_opt > 60 :  t_opt = 60
    #   - Rohstoff max. 30 Tage lang abbauen
    #   - Es sind noch Rohstoff-Ast. vorhanden. Nur wenn noch vorhanden, dann nächste Suche
    #   - Nicht alle Rohstoffe wurden schon vollständig abgebaut. Wenn nicht, dann nächste Suche


    print("Produkt: ", data[asteroid_1_idx,-1].astype(int))

    print("Aufenthaltsdauer: ", ERG_t_m[-1])

    # Neuer Bestand
    psa.abbau(bestand, asteroid_1_idx, ERG_t_m[-1])
    print("Bestand nach Abbau, vor Abflug: ", bestand)

    # Gütemaß
    J = - np.min(bestand[0:2])
    print("Gütemaß ohne Tank: ", J)


    # Abbau abgeschlossen, jetzt Flug zum nächsten Asteroiden
    DV = dv_min_/10000
    # Tank NACH dem Landen auf Ast 2
    bestand[-1] = bestand[-1] - DV



    # Asteroiden aus Liste streichen
    if psa.asteroid_material(asteroid_2_idx) == 3:
        asteroids_fuel_idx.remove(asteroid_2_idx)
        asteroids_idx.remove(asteroid_2_idx)
    else: asteroids_idx.remove(asteroid_2_idx)
    print("Besuchte Asteroiden: ", ERG_a)




    
    
    print("--------------------------------------------")
    
    # var += 1
    

print("=====================================================================")

print("Anzahl der besuchten Asteroiden: ", len(ERG_a))

#################################################
# SCHRITT 6:        Lösungs-Zeitplan erstellen
#################################################
from from_website import SpoC_Kontrolle as spoc

x = ERG_t_arr[0:-2] + ERG_t_m + ERG_a[0:-2]
print(spoc.udp.pretty(x))

### Beschränkung von t_m : Wenn t_arr + t_m > max_Zeit, usw...

###########################################
# SCHRITT 6:        json-File-Erstellung
###########################################
# Annahme:  Flug beendet und Ergebnisvektoren aufgestellt
# ERGEBNIS: json-File aus den Vektoren wird gebildet

from from_website.submisson_helper import create_submission
create_submission("spoc-mining","mine-the-belt",x,"TUDa_GoldRush_submission_file.json","TUDa_GoldRush","submission_description")