import numpy as np
# from PSA_essentials import PSA_experiment


# Bitte übergeben Sie den Pfad zum Datensatz in folgender, beispielhafter Form:
Datensatz = np.loadtxt("C:/Users/ingap/OneDrive/Desktop/Uni/WiSe_22-23/PSA/PSA_SpoC_Mining/SpoC_Projekt/data/SpoC_Datensatz.txt")

# visited = []
# STORAGE= [10,2,4,6]
# storage = []

# Gürtel = PSA_essentials(Datensatz)


# print("Relativer Materialbestand: ", Gürtel.relative_material_stock())
# print("Min. Material absolut und relativ: ", Gürtel.minimal_material())

# print(Datensatz[int(100.0),0])

import PSA_essentials_try as psa
# print(psa.DV_norm(3500))

print(Datensatz[0:5])