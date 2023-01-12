import numpy as np
import copy
import PSA_functions_v5

data = np.loadtxt("SpoC_Datensatz.txt")

# den zweiten Asteroiden finden, aus minimaler Verfügbarkeit und maximaler Masse


min_mat_mass = []
for i in range(0,len(data)):
    if data[i,-1] == 1:
        min_mat_mass.append(data[i,-2])

second_asteroid = np.argpartition(min_mat_mass, -1)[-1:]

print(second_asteroid, min_mat_mass[second_asteroid[0]])