""" Clusterung aller Asteroiden in Zeitschritten durchführen und anschließend Wichtige Parameter plotten """

# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde

# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST


""" Konstanten Definieren """
# Startzeit
t0 = 0
# Zeitschritte für Clusterung
t_Step = 3
timeline = np.arange(t0,21, t_Step) # 1827
# Zulässiger Radius der Clusterung
eps = 800
# Minimale Anzahl eines Clusters
min_samples = 5
# Zulässige Flugzeit
T = 30
# Zu plottende Größen: 
max_members = []
max_core_members = []


# Cluster Objekt erstellen
mycluster = pk.phasing.dbscan(asteroids)
# Durch Zeit durchiterieren und zu plottende Werte bestimmen (Cluster gehen verloren)
for t in timeline:
    mycluster.cluster(
            t= int(t),
            eps= eps,
            min_samples= min_samples,
            metric= 'orbital', 
            T= T
            )

    length_of_cluster = []
    i=0
    labels= []
    for label in list(mycluster.members.keys()):
        length_of_cluster.append(len(mycluster.members[label]))
        labels.append(label)
        i+=1

    max_label = labels[length_of_cluster.index(max(length_of_cluster))]

    max_members.append(mycluster.members[max_label])
    max_core_members.append(mycluster.core_members[max_label])


# print(len(timeline))
# print(len(max_members))
fig = plt.figure
plt.plot(timeline, max_members)
plt.plot(timeline, max_core_members)

plt.show()