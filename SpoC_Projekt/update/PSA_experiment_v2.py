import numpy as np
import pykep as pk
from pykep import phasing
import random

import PSA_functions_v2 as psa
from _Extra._Mathias.fuzzy_system import FuzzySystem

###########
# Constants
###########
T_START = pk.epoch_from_iso_string("30190302T000000")   # Start and end epochs
T_END = pk.epoch_from_iso_string("30240302T000000")
T_DAUER = 1827
G = 6.67430e-11                                 # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30                                   # Sun_mass (kg)
MS = 8.98266512e-2 * SM                         # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS                            # Mu of the Trappist-1 star
DV_per_propellant = 10000                       # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30                         # Maximum time to fully mine an asteroid


#################
# ASTEROIDS:  Creating lists with indices of asteroids
#################

# Lists to be created
asteroids_kp = []
dict_asteroids = dict()

# Loading data as keplerian elements (planets) in an "array"
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
    asteroids_kp.append(p)
    dict_asteroids[int(line[0])] = [p, line[-2], int(line[-1])]  # Key = ID, Liste mit [Kaplerian, Masse, Material]
# Putzen - wahrscheinlich nicht notwendig
del p
del data

#########
# TIME
#########

# Startwerte
t_start = 0
t_aktuell = [t_start]   # Seien wir 0 Tage auf dem ersten Asteroiden stehen geblieben bis 1. Abflug
# t_aktuell_e = pk.epoch(t_aktuell[-1])

#########
# GÜTE
#########

propellant = 1.0        # entspricht DV_max = 10.000
bestand = [0.0, 0.0, 0.0, propellant]
verf = np.array([0.03, 0.4, 0.42, 0.15])  # ToDo: Verfügbarkeit berechnen

my_system = FuzzySystem(verf.min(), verf.max(), resolution=0.02)


###########
# LETS GO
###########

# Startpunkt festlegen ToDo: Später müssen es mehrere sein, Funktion die gute Kandidaten findet fehlt noch!
# i_start = 3869, 8836 # Für diesen Asteroiden super weg bisher gefunden! - Ursprünglich: 9953
i_start = random.randrange(0, len(asteroids_kp), 1)
# Speicher für die beta Pfade:
# ToDo: Für Beam-Search gibt es wiederum ein Dictionary mit brachnN als Inhalte
#  durch dieses wird dann später iteriert
# beams = {0 : {0: {'id': i_start, 't_m': 0.0, 't_arr': 0.0}}}
branch = {0: {'id': i_start, 't_m': 0.0, 't_arr': 0.0}}

print("Start-Asteroid: ", branch[0]['id'])


for i in range(50):
    if T_DAUER < (branch[i]['t_arr']-59):
        branch[i]['t_m'] = 60.0
        # Abbau des Rohstoffs von Asteroid 1:
        psa.abbau(bestand, dict_asteroids[branch[i]['id']][1], dict_asteroids[branch[i]['id']][2], branch[i]['t_m'])
        # Bewertung:
        print(f"Gütemaß ohne Tank: {- np.min(bestand[0:3]):.3}")
        print("Bestand: ", bestand[0:3])
        break

    print(f"================ Durchlauf {i} ================")
    # for branch in beams:    # ToDo: Ermöglicht später ads iterieren durch die verschiedenen Branches - wenns so klappt
    # Aktuellen Startpunkt auslesen
    asteroid_1_id = branch[i]['id']
    asteroid_1_kp, asteroid_1_mas, asteroid_1_mat = dict_asteroids[asteroid_1_id]

    # Abbauzeit für gesamte Masse bestimmen
    if asteroid_1_id == i_start:    # bzw. i == 0
        t_opt = 0
    else:
        t_opt = 30*asteroid_1_mas

    # Asteroidenpool abhängig von vorhandenem Tank
    # ToDo: Leider nicht als Dictionary lösbar, oder? - clustering funktioniert sonst nicht
    # ToDo: evtl. auch später erst TankAsteroid auswählen, sonst zu wenige andere Asteroiden
    # ToDo: Beschränkung auf Basis des Tanks nach Abbau nicht vor - sonst bei Landung auf Tankasteroid zu streng
    if (bestand[-1] < 0.3) and (branch[i]['t_arr'] < 1750):
        candidates_id = [asteroid_id for asteroid_id, values in dict_asteroids.items() if values[-1] == 3]
        print("Als nächstes Tank-Asteroiden aussuchen")
    elif 3*np.min(bestand[:3]) < np.max(bestand[:3]):
        candidates_id = [asteroid_id for asteroid_id, values in dict_asteroids.items()
                         if values[-1] is not np.argmax(bestand[:3])]
        print(f"Ausschluss von Material {np.argmax(bestand[:3])}")
    else:
        candidates_id = [asteroid_id for asteroid_id, values in dict_asteroids.items()]
    candidates = [dict_asteroids[asteroid_id][0] for asteroid_id in candidates_id]

    # ===================
    # Clustering itself
    # ToDo: T & radius können auch anders gewählt werden
    radius = 4000
    knn = phasing.knn(candidates, branch[i]['t_arr']+t_opt, 'orbital', T=30)
    neighb_inds = psa.clustering(knn, asteroids_kp, asteroid_1_id, radius)   # ToDo: Eventuell knn anstatt ball?
    print(f"{len(neighb_inds)} gefundene Nachbarn: ", neighb_inds)
    # Iteration durch Cluster
    score_2 = []
    flight_opt = []
    for index in neighb_inds:
        if candidates_id[index] == asteroid_1_id:
            continue
        # Index ist nicht Startasteroid
        asteroid_2_id = candidates_id[index]
        asteroid_2_kp, asteroid_2_mas, asteroid_2_mat = dict_asteroids[asteroid_2_id]
        # Zeitoptimierung für Überflug
        t_abflug_opt_, t_flug_min_dv_, dv_min_ = psa.time_optimize_time_v2(
            asteroid_1_kp,
            asteroid_2_kp,
            t_start=branch[i]['t_arr']+t_opt,
            t_opt=t_opt,
            limit=bestand[-1]
            # print_result=True
        )
        # ToDo: Derzeit Bestand vor Abbau - Bei Tankasteroiden sollte das evtl. berücksichtigt werden
        # if asteroid_2_mat == 3:
        #     limit =
        # Bewertung nur durchführen, wenn Asteroid auch erreichbar!
        if (dv_min_/DV_per_propellant) < bestand[-1]:
            # Bewertung des Asteroids und des Wechsels
            score = my_system.calculate_score(  # ToDo: Über Normierung des delta_v sprechen
                t_n=(bestand[-1] - (dv_min_/DV_per_propellant)),    # Tank nach Flug → dv muss normiert werden
                delta_v=(dv_min_/radius),                           # Diese Normierung in Ordnung? - Dachte ganz sinnvoll
                bes=psa.norm_bestand(bestand, asteroid_2_mat),
                verf=verf[asteroid_2_mat],
                mas=asteroid_2_mas)
            # Score und Daten für Flug merken
            score_2.append(score)
            flight_opt.append([asteroid_2_id, t_abflug_opt_, t_flug_min_dv_, dv_min_])
            # print(f"Kandidat:{asteroid_2_id} Material:{dict_asteroids[asteroid_2_id][2]} "
            #       f"Masse:{dict_asteroids[asteroid_2_id][1]:.3} Güte: {score:.3}")
            # print(f"Starttag:{t_abflug_opt_:.0f}  Flugzeit:{t_flug_min_dv_:.0f}   => Delta V ={dv_min_:.0f}")

    print("========== Clustering abgeschlossen, Optimum wählen ==========")
    # Optimum wählen:
    asteroid_2_id, t_abflug_opt_, t_flug_min_dv_, dv_min_ = flight_opt[score_2.index(max(score_2))]
    print(f"Starttag:{t_abflug_opt_:.0f}  Flugzeit:{t_flug_min_dv_:.0f}   => Delta V ={dv_min_:.0f}")
    print(f"Ziel-Asteroid: {asteroid_2_id}  "
          f"Material:{dict_asteroids[asteroid_2_id][2]}  "
          f"Masse:{dict_asteroids[asteroid_2_id][1]:.3}")

    # Übername in Branch:
    # ToDo: Scheife Stoppen, sobald t_arr nach T_Dauer ist (was passiert mit dem  letzten Eintrag?)
    branch[i+1] = {'id': asteroid_2_id, 't_m': 0.0, 't_arr': t_abflug_opt_+t_flug_min_dv_}
    # t_m von aktuellem ASteroiden bestimmen
    branch[i]['t_m'] = t_abflug_opt_ - branch[i]['t_arr']

    # Abbau des Rohstoffs von Asteroid 1:
    psa.abbau(bestand, asteroid_1_mas, asteroid_1_mat, branch[i]['t_m'])
    # Bewertung:
    print(f"Gütemaß ohne Tank: {- np.min(bestand[0:3]):.3}")
    print("Bestand: ", bestand[0:3])
    # Flug zum anderen Asteroiden
    bestand[-1] -= dv_min_/DV_per_propellant
    print(f"Tank nach Abbau und Flug zum nächsten: {bestand[-1]:.3}")

    # Besuchten Asteroiden aus Dictionary streichen
    # del dict_asteroids[asteroid_1_id]
    dict_asteroids.pop(asteroid_1_id)
    # Kandidaten leeren
    # candidates_id.clear()
    # candidates.clear()
    # neighb_inds.clear()


######################################
# Ergebnisse auswerten und abspeichern
######################################
print("=====================================================================")

# # Laufvariablen       ToDo: Werden erst am Ende gefüllt, wenn finaler Pfad festliegt
ERG_a = []
ERG_t_m = []
ERG_t_arr = []
ERG_list = [[out for out in step.values()] for step in branch.values()]
for a, t_m, t_arr in ERG_list:
    ERG_a.append(a)
    ERG_t_m.append(t_m)
    ERG_t_arr.append(t_arr)

print("Anzahl der besuchten Asteroiden: ", len(ERG_a))
print(branch)
for a, t_m, t_arr in zip(ERG_a, ERG_t_m, ERG_t_arr):
    print(f"Asteroid ID:{a}     Ankunftszeit:{t_arr:.4}     Verweildauer:{t_m:.3}")
# for i in range(len(ERG_a)):
#     print("Asteroid ID: ", ERG_a[i], f"Ankunftszeit: {ERG_t_arr[i]:.3}", f"Verweildauer: {ERG_t_m[i]:.2}")
