# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde

# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST


##########
# Tests
#########


""" Orbit plotten """
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1, projection = '3d')
# for i in range(20): ax1 = pk.orbit_plots.plot_planet(asteroids[i], t0=0, tf=None, N=60, units=1.0,  color='b', axes= ax)
# # ax1 = pk.orbit_plots.plot_planet(asteroids[2], t0=0, tf=None, N=60, units=1.0,  color='r', axes= ax)
# plt.show()


""" Verteilung der Periodendauer  """
# myasteroid = asteroids[3]
# T = myasteroid.compute_period(epoch(5))
# print('Periodendauer von %(name)s sind %(number)f Sekunden' %{"name": myasteroid.name, "number": T})

# period = []
# for asteroid in asteroids:
#     period.append(
#         asteroid.compute_period(epoch(0))/(24*60*60)    #Sekunden in Tage umrechnen
#         )

# # Dichteplot
# prob_density = kde.gaussian_kde(period)
# prob_density.covariance_factor = lambda : .05
# prob_density._compute_covariance()

# x = np.linspace(min(period),max(period),300)
# y = prob_density(x)
# plt.plot(x,y)
# plt.title("Density of Orbit-Period [days]")

# plt.show()


""" Verteilung der Masse: Fragestellung, ob man Verbleib davon abhängig machen sollte """
# prob_density = kde.gaussian_kde(asteroid_masses)
# prob_density.covariance_factor = lambda : .05
# prob_density._compute_covariance()

# x = np.linspace(min(asteroid_masses),max(asteroid_masses),300)
# y = prob_density(x)
# plt.plot(x,y)
# plt.title("Density of Asteroid-Masses")

# plt.show()

""" Verteilung der Materialien über die Asteroiden """
# plt.hist(asteroid_materials, bins=[-0.25,0.25,0.75,1.25,1.75,2.25,2.5,2.75,3.25])
# plt.title("Distribution of Materials")
# plt.show()


###############################################
# Clusterung mit DBSCAN
##############################################
mycluster = pk.phasing.dbscan(asteroids)

# """ Mit Anzahl Clustern vertraut machen """
# eps_range = np.linspace(200, 800, 20)
# n_cluster = []

# for eps in eps_range:
#     mycluster.cluster(t=0, eps= eps,min_samples=5,metric='orbital', T=20)   # T ist die Reisezeit, wenn diese zu lang wird, kann man (fast) jeden Asteroiden erreichen
#     n_cluster.append(mycluster.n_clusters)

# for i in range(len(n_cluster)):
#     print(f'{eps_range[i]:10} ==> {n_cluster[i]:10f}')
# plt.plot(eps_range,n_cluster)
# plt.show()

# Probleme mit Achse...
# mycluster.plot()

# mycluster.pretty()

""" Für eine Distanz von 800m Cluster bestimmen und DV für nächstgelegenden berechnen """
""" Ergebnis: Bei Entfernung von ?? (<800m) wird bei 20 Tagen Flugzeit ein DV von 1252m/s^2 benötigt. 
Reihenfolge der Members sagt nichts über Eignung aus, sondern ist nach ID sortiert"""
# t0 = 0
# T = 20

# mycluster.cluster(
#     t= t0, 
#     eps= 800 ,
#     min_samples= 5,
#     metric= 'orbital', 
#     T= T
#     )
# asteroid1 = asteroids[mycluster.core_members[0][0]]  # Von Cluster 0 Asteroid 0 wählen
# # asteroid2 = asteroids[mycluster.core_members[0][1]]
# asteroid2 = asteroids[mycluster.members[0][-1]]

# # DV für ersten Nachbarn und für verschiedene Zeitpunkte
# # Startpunkt
# r1,v1 = asteroid1.eph(t0)
# # Trajektorie und Landepunkt
# for t in np.linspace(t0+1,T,10):
#     #Position und Geschwindigkeit von 2 zum Zeitpunkt t abrufen
#     r2,v2 = asteroid2.eph(t)
#     # Solve the lambert problem for this flight
#     l = pk.lambert_problem(
#         r1=r1, r2=r2, tof=t * pk.DAY2SEC, mu= MU_TRAPPIST, cw=False, max_revs=0
#         )
#     # Compute the delta-v necessary to go there and match its velocity
#     DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
#     DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
#     DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)

#     print(DV)

# mycluster.pretty()


""" Spritverbrauch bestimmen für einen Flug von ?? Metern """
""" Bei Abstand dist = 1918 (kNN) ergit sich ein DV von 3950 bei T=20 für den hier betrachteten Fall """
current = 0 # Aktuell betrachteter Asteroid
T = 20      # Maximale Reisezeit
knn = pk.phasing.knn(asteroids, t=epoch(0), metric='orbital', T=T)
neighbs, ids, dists = knn.find_neighbours(asteroids[current], query_type='knn', k = 20)

for i in range(len(neighbs)):
    print(f'{ids[i]:10} ==> {dists[i]:10f}')

print(f'{ids[1]:10} ==> {dists[1]:10f}')
r1,v1 = asteroids[current].eph(0)


# DV für ersten Nachbarn und für verschiedene Zeitpunkte
for t in np.linspace(1,T,10):
    r2,v2 = asteroids[ids[1]].eph(t)
    # Solve the lambert problem for this flight
    l = pk.lambert_problem(
        r1=r1, r2=r2, tof=t * pk.DAY2SEC, mu= MU_TRAPPIST, cw=False, max_revs=0
        )
    # Compute the delta-v necessary to go there and match its velocity
    DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
    DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
    DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)

    print(DV)
