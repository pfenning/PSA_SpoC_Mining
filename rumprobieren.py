import pykep as pk
from pykep import phasing
import numpy as np
import copy
import PSA_functions_v5 as psa
import branch_class_v2 as bc

T_START = pk.epoch_from_iso_string("30190302T000000")  # Start and end epochs
T_END = pk.epoch_from_iso_string("30240302T000000")
T_DAUER = 1827
G = 6.67430e-11  # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30  # Sun_mass (kg)
MS = 8.98266512e-2 * SM  # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS  # Mu of the Trappist-1 star
DV_per_propellant = 10000  # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30  # Maximum time to fully mine an asteroid

data = np.loadtxt("SpoC_Datensatz.txt")
asteroids_kp = []
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

print(asteroids_kp)

entire_ids = asteroids_kp[:,0]

'''
Vorgabe des ersten und zweiten Asteroiden!!
Insbesondere der zweite Asteroid ist von Bedeutung
==> Rückwirkenden Branch erstellen!! 
'''

# 1) den ZWEITEN Asteroiden finden, aus minimaler Verfügbarkeit und maximaler Masse
ast_2_idx_v = []
min_mat_mass = []
min_mat = psa.find_min_material(data)
for i in range(0,len(data)):
    if data[i,-1] == min_mat:
        min_mat_mass.append(data[i,-2])
        ast_2_idx_v.append(data[i,0])
second_asteroid = np.argpartition(min_mat_mass, -1)[-1:] # Vektor mit Index
asteroid_2_idx = int(ast_2_idx_v[second_asteroid[0]])
asteroid_2_masse = min_mat_mass[second_asteroid[0]]
# print(asteroid_2_idx, asteroid_2_masse)
entire_ids.pop(asteroid_2_idx)

# 2) Cluster um zweiten Asteroiden bilden, ERSTEN Asteroiden auswählen mit minimalem Abstand!! 
#       ==> Zeitoptimierung für Auswahl egal, aber: beeinflusst man dadurch die Zeitoptimierung?
#       find_nearest_neighbors von ast_2 ausgehend & dann den Ast. mit der kleinesten Distanz auswählen


# candidates bekomme ich aus branch_class: find_start_idx --> macht doch keinen Sinn, weil diese evtl. viel zu weit weg vom zweiten Ast sind
# candidates = [for id in data[:,0]] 
# knn = phasing.knn(candidates, t_opt, 'orbital', T=30) # wie wähle ich t_arr und t_opt?  # visited[-1]['t_arr'] + t_opt 

# neighb_ind, neighb_dis = psa.clustering(knn, asteroids_kp, asteroid_2_idx)


# 3) Objekt Branch erstellen, nur mit zwei vorgegebenen Asteroiden: Erster und zweiter!!


## Kann man bestimmen, dass dieser Asteroid vollständig abgebaut wird und danach erst die Zeitoptimierung durchgeführt wird?

