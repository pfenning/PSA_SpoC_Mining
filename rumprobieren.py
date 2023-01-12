import numpy as np
import copy
import PSA_functions_v5 as psa

data = np.loadtxt("SpoC_Datensatz.txt")

# den ZWEITEN Asteroiden finden, aus minimaler Verfügbarkeit und maximaler Masse
min_mat_mass = []
min_mat = psa.find_min_material(data)
for i in range(0,len(data)):
    if data[i,-1] == min_mat:
        min_mat_mass.append(data[i,-2])
second_asteroid = np.argpartition(min_mat_mass, -1)[-1:]
print(min_mat_mass[second_asteroid[0]])

# Cluster um zweiten Asteroiden bilden
