import numpy as np
import matplotlib.pyplot as plt
import pykep as pk
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

# Loading data as keplerian elements (planets) in an "array"
data = np.loadtxt("C:/Users/ingap/OneDrive/Desktop/Uni/WiSe_22-23/PSA/PSA_SpoC_Mining/SpoC_Projekt/data/SpoC_Datensatz.txt")
asteroids = []
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
    asteroids.append(p)
# asteroid_masses = data[:, -2]
# asteroid_materials = data[:, -1].astype(int)
data_fuel = []
asteroids_fuel = []
i = 0
while i < len(data):
    if data[i,-1].astype(int) == 3:
        data_fuel.append(data[i])
        i += 1
    else: i += 1
for line in data_fuel:
    p = pk.planet.keplerian(T_START,(line[1],line[2],line[3],line[4],line[5],line[6],),
        MU_TRAPPIST,
        G * line[7],  # mass in planet is not used in UDP, instead separate array below
        1,  # these variable are not relevant for this problem
        1.1,  # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0])),
    )
    asteroids_fuel.append(p)                                                       # ACHTUNG, wirklich p schon anhängen?!?!?!
asteroid_masses = data[:, -2]
asteroid_materials = data[:, -1].astype(int)


# ANGABE START-ASTEROID
i_start = random.randrange(0, len(data),1)


# Startwerte
t_start = [0]
t_aktuell = [t_start] # Seien wir 0 Tage auf dem ersten Asteroiden stehen geblieben bis 1. Abflug
t_opt = 30
# t_aktuell_e = pk.epoch(t_aktuell[-1])

propellant = 1.0 # entspricht DV_max = 10.000

asteroid1 = asteroids[i_start]        # Der erste Asteroid der Liste wird ausgewählt
asteroid1_id = i_start
asteroids = np.delete(asteroids, i_start)

# Tank-Asteroiden
asteroids_fuel_ind = []
i = 0
while i <= len(asteroids):
    if data[i,-1].astype(int) == 3:
        asteroids_fuel_ind.append(i)
    i += 1

# Laufvariablen
ERG_t_arr = [0.0]   # double, Ankunftszeit
ERG_t_m = []        # double, Verweildauer
ERG_a = [i_start]   # int, besuchte Asteroiden

bestand = [0.0, 0.0, 0.0, propellant]
bestand_rel = [0.0, 0.0, 0.0, 0.0]


# # Erst mal nur durch die ersten 3 (grenze-1) durchlaufen und gucken, ob alles funktioniert
# var = i_start
# grenze = 4

# while t_aktuell < T_DAUER:



# while var <= i_start+grenze:
print("Start-Asteroid: ", i_start)
propellant=1.0
visited_ind = [i_start]
while len(visited_ind) <= 5: # <= 10000
    #print("Ast " + str(var) + " --> Ast " + str(var+1))
    # propellant = 1.0

    var = visited_ind[-1] # aktueller Asteroid!!
    asteroid1 = asteroids[var]
    # print("Asteroid1: ", asteroid1)
    

    #################################
    ### SCHRITT 1:      Clustering      UNEINGESCHRÄNKT
    #################################
    # # Annahme:  Wir befinden uns auf einem Asteroiden
    # from pykep import phasing
    # knn = phasing.knn(asteroids, ERG_t_arr[-1], 'orbital', T = 30) #                                            ACHTUNG: Referenzradius & -geschw. sind Gürtelabhängig!
    # radius = 1500
    # neighb, neighb_ids = psa.clustering(knn, var, radius)
    # # print(len(neighb_ids))
    # # print("Nachbarn: ", neighb_ids)
    # i = 0
    # dv_min_2 = []
    # while i < len(neighb_ids):
    #     if neighb_ids[i] not in visited_ind:
    #         asteroid2_id = neighb_ids[i]
    #         asteroid2 = asteroids[asteroid2_id]
    #         t_abflug_opt_, t_flug_min_dv_, dv_min_ = psa.time_optimize_time_v2(asteroid1, asteroid2, ERG_t_arr[-1] + t_opt, t_opt)        
    #         dv_min_2.append(dv_min_)
    #         i += 1
    #     else:
    #         i += 1

    # dv_min_2_intermediate_INDEX = dv_min_2.index(min(dv_min_2))
    # asteroid2_id = neighb_ids[dv_min_2_intermediate_INDEX]
    # asteroid2 = asteroids[asteroid2_id]

    # # Asteroiden aus Liste streichen
    # asteroids = np.delete(asteroids, asteroid2_id)
    # visited_ind.append(asteroid2_id)  
    # print("Besuchte Asteroiden: ", visited_ind)

    # # ACHTUNG: WENN CLUSTER DURCH BEDINGUNG LEER, DANN IST "dv_min_2" LEER UND ER BESUCHT DEN GLEICHEN ASTEROIDEN NOCHMAL!!! 
    # # DAS IST ZU VERMEIDEN!!!!!!


    #################################
    ### SCHRITT 1:      Clustering      JEDER 2. TANKFÜLLUNG
    #################################
    # Annahme:  Wir befinden uns auf einem Asteroiden
    from pykep import phasing

    # print(len(neighb_ids))
    # print("Nachbarn: ", neighb_ids)
    i = 0
    dv_min_2 = []

    if ERG_a[-1] == i_start: t_opt = 0
    else: t_opt = psa.asteroid_masse(asteroid1_id)*30

    if bestand[-1] < 0.6:
        knn_fuel = phasing.knn(asteroids_fuel, ERG_t_arr[-1]+t_opt, 'orbital', T = 30) #                                            ACHTUNG: Referenzradius & -geschw. sind Gürtelabhängig!
        radius = 4000
        neighb_fuel, neighb_fuel_ids = psa.clustering_fuel(knn_fuel, var, radius)
        print("Nachbarn: ", neighb_fuel_ids)
        while i < len(neighb_fuel_ids):
            asteroid2_fuel_id = neighb_fuel_ids[i]
            asteroid2 = asteroids[asteroid2_fuel_id]
            t_abflug_opt_, t_flug_min_dv_, dv_min_ = psa.time_optimize_time_v2(asteroid1, asteroid2, ERG_t_arr[-1] + t_opt, t_opt)        
            dv_min_2.append(dv_min_)
            i += 1
        dv_min_2_intermediate_INDEX = dv_min_2.index(min(dv_min_2))
        asteroid2_id = neighb_fuel_ids[dv_min_2_intermediate_INDEX]
        asteroid2 = asteroids[asteroid2_id]

    else:
        knn = phasing.knn(asteroids, ERG_t_arr[-1]+t_opt, 'orbital', T = 30) #                                            ACHTUNG: Referenzradius & -geschw. sind Gürtelabhängig!
        radius = 4000
        neighb, neighb_ids = psa.clustering(knn, var, radius)
        while i < len(neighb_ids):
                asteroid2_id = neighb_ids[i]
                asteroid2 = asteroids[asteroid2_id]
                t_abflug_opt_, t_flug_min_dv_, dv_min_ = psa.time_optimize_time_v2(asteroid1, asteroid2, ERG_t_arr[-1] + t_opt, t_opt)        
                dv_min_2.append(dv_min_)
                i += 1
        dv_min_2_intermediate_INDEX = dv_min_2.index(min(dv_min_2))
        asteroid2_id = neighb_ids[dv_min_2_intermediate_INDEX]
        asteroid2 = asteroids[asteroid2_id]



# ACHTUNG: WENN CLUSTER DURCH BEDINGUNG LEER, DANN IST "dv_min_2" LEER !!! 
# DAS IST ZU VERMEIDEN!!!!!! => Was dann ?!?!?!




    ###################################
    # SCHRITT 2:        Fuzzy-Logic
    ###################################
    # Annahme:  Cluster wurde gebildet und man hat aus 10.000 nur noch 300 (=beta) mögliche/sinnvolle Asteroiden zur Auswahl
    # Cluster nicht abhängig von DV, deswegen wird Fuzzy zustätzlich dafür benutzt
    # ERGEBNIS: beta-Beste Asteroiden werden durch Fuzzy vorgeschlagen

    # Hier muss Mathias' Code eingebaut werden, so gut es geht

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
    ERG_a.append(asteroid2_id)

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


    print("Produkt: ", data[asteroid1_id,-1].astype(int))

    # Neuer Bestand
    psa.abbau(bestand, asteroid1_id, ERG_t_m[-1])
    print("Bestand nach Abbau, vor Abflug: ", bestand)

    # Gütemaß
    J = - np.min(bestand[0:2])
    print("Gütemaß ohne Tank: ", J)


    # Abbau abgeschlossen, jetzt Flug zum nächsten Asteroiden
    consumption = dv_min_2[dv_min_2_intermediate_INDEX]
    DV = consumption/10000
    # Tank NACH dem Landen auf Ast 2
    bestand[-1] = bestand[-1] - DV



    # Asteroiden aus Liste streichen
    if asteroid_materials(asteroid2_id) == 3:
        np.delete(asteroids_fuel, asteroid2_id)
        np.delete(asteroids, asteroid2_id)
    else: np.delete(asteroids, asteroid2_id)
    visited_ind.append(asteroid2_id)  
    print("Besuchte Asteroiden: ", visited_ind)




    
    
    print("--------------------------------------------")
    
    # var += 1
    

print("=====================================================================")

print("Anzahl der besuchten Asteroiden: ", len(visited_ind))

#################################################
# SCHRITT 6:        Lösungs-Zeitplan erstellen
#################################################

import from_website.SpoC_Kontrolle as spoc

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