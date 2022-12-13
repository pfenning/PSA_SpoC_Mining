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
import PSA_essentials_try as psa
import time_optimize_final as zeitopti

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
asteroids_original = []
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
    asteroids_original.append(p)
# asteroid_masses = data[:, -2]
# asteroid_materials = data[:, -1].astype(int)


# ANGABE START-ASTEROID
i_start = random.randrange(0, len(data),1)


# Startwerte
t_start = [0]
t_aktuell = [t_start] # Seien wir 0 Tage auf dem ersten Asteroiden stehen geblieben bis 1. Abflug
t_opt = 30
# t_aktuell_e = pk.epoch(t_aktuell[-1])

propellant = 1.0 # entspricht DV_max = 10.000

asteroids = asteroids_original
asteroid1 = asteroids[i_start]        # Der erste Asteroid der Liste wird ausgewählt
asteroid1_id = i_start
asteroids = np.delete(asteroids, i_start)

# Laufvariablen
ERG_t_arr = [0.0]   # double, Ankunftszeit
ERG_t_m = [0.0]        # double, Verweildauer
ERG_a = [i_start]   # int, besuchte Asteroiden

bestand = [0.0, 0.0, 0.0, propellant]
bestand_rel = [0.0, 0.0, 0.0, 0.0]


# Erst mal nur durch die ersten 3 (grenze-1) durchlaufen und gucken, ob alles funktioniert
var = i_start
grenze = 4

# while t_aktuell < T_DAUER:

visited = [i_start]
while len(visited) <= 30: # <= 10000


# while var <= i_start+grenze:
    #print("Ast " + str(var) + " --> Ast " + str(var+1))
    propellant = 1.0

    var = visited[-1]
    asteroid1 = asteroids[var]
    
    #################################
    ### SCHRITT 1:      Clustering
    #################################
    # Annahme:  Wir befinden uns auf einem Asteroiden

    from pykep import phasing

    knn = phasing.knn(asteroids, ERG_t_arr[-1], 'orbital', T = 30) #                                            ACHTUNG: Referenzradius & -geschw. sind Gürtelabhängig!
    neighb, neighb_ids, neighb_dis = knn.find_neighbours(var, query_type='ball', r=800)
    neighb = list(neighb)
    neighb_ids = list(neighb_ids)

    asteroid2_id = neighb_ids[random.randrange(0, len(neighb),1)]
    asteroid2 = asteroids[asteroid2_id]

    # print("Nachbarn: ", len(neighb))
    # print("Näheste Nachbarn: ", neighb_ids)
    print("Ausgewählter Asteroid2: ", asteroid2_id)


    visited.append(asteroid2_id)
    # print("Besuchte Ast: ", visited)


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
    # visited.append(next_best_ast)
    

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

    # Nächster Asteroid
    # asteroid2 = asteroids[next_best_ast]
    material_to_be_mined = data[asteroid2_id,-1].astype(int)
    print("Produkt: ", material_to_be_mined)

    # Zeitoptimierung       ?       optimale Abbauzeit wird gefordert..woher kommt diese?
    t_abflug_opt, t_flug_min_dv, dv_min = psa.zeitoptimierung(asteroid1, asteroid2, ERG_t_arr[-1] + t_opt, t_opt) # Erst mal die optimale Abbauzeit = 20 Tage
    
    print("Zeitoptimierung: ", t_abflug_opt, t_flug_min_dv, dv_min)
    
    # Lösungsvektoren:
    if ERG_t_arr[-1] == t_start: 
        ERG_t_m.append(t_abflug_opt)
        ERG_t_arr.append(t_abflug_opt + t_flug_min_dv)
    else: 
        ERG_t_m.append(t_abflug_opt - ERG_t_arr[-1])
        ERG_t_arr.append(ERG_t_arr[-1] + ERG_t_m[-1] + t_flug_min_dv)
    ERG_a.append(asteroid2_id)

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

    # Gütewert J:
    J = - np.min(bestand[0:2])
    print("Gütemaß ohne Tank: ", J)
    print("Bestand nach Abbau, Abflugzeitpunkt: ", psa.abbau(bestand, material_to_be_mined, ERG_t_m[-1]))

    # Verbrauch des Flugs vom Tank abziehen!
    bestand[-1] = propellant - dv_min/10000
    print("Tankfüllung nach Flug: ", bestand[-1])
    print("Verbrauchter Tank: ", dv_min)
    
    # Asteroiden aus Liste streichen
    asteroids = np.delete(asteroids, asteroid2_id)
    print("--------------------------------------------")
    
    # var += 1

print("=====================================================================")

print("Anzahl der besuchten Asteroiden: ", len(visited))

#################################################
# SCHRITT 6:        Lösungs-Zeitplan erstellen
#################################################

import SpoC_Kontrolle as spoc

x = ERG_t_arr + ERG_t_m + ERG_a
print(spoc.udp.pretty(x))



###########################################
# SCHRITT 6:        json-File-Erstellung
###########################################
# Annahme:  Flug beendet und Ergebnisvektoren aufgestellt
# ERGEBNIS: json-File aus den Vektoren wird gebildet

from submisson_helper import create_submission
create_submission("spoc-mining","mine-the-belt",x,"TUDa_GoldRush_submission_file.json","TUDa_GoldRush","submission_description")