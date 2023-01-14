# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde

# Konstanten und Database Laden
from spoc_constants import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST

mycluster = pk.phasing.dbscan(asteroids)

t0 = 0
T = 20

mycluster.cluster(
    t= t0, 
    eps= 800 ,
    min_samples= 5,
    metric= 'orbital', 
    T= T
    )
asteroid1 = asteroids[mycluster.core_members[0][0]]  # Von Cluster 0 Asteroid 0 wählen
# asteroid2 = asteroids[mycluster.core_members[0][1]]
asteroid2 = asteroids[mycluster.members[0][-1]]

# DV für ersten Nachbarn und für verschiedene Zeitpunkte
# Startpunkt
r1,v1 = asteroid1.eph(t0)
# Trajektorie und Landepunkt
for t in np.linspace(t0+1,T,10):
    #Position und Geschwindigkeit von 2 zum Zeitpunkt t abrufen
    r2,v2 = asteroid2.eph(t)
    # Solve the lambert problem for this flight
    l = pk.lambert_problem(
        r1=r1, r2=r2, tof=t * pk.DAY2SEC, mu= MU_TRAPPIST, cw=False, max_revs=0
        )
    # Compute the delta-v necessary to go there and match its velocity
    DV1 = [a - b for a, b in zip(v1, l.get_v1()[0])]
    DV2 = [a - b for a, b in zip(v2, l.get_v2()[0])]
    DV = np.linalg.norm(DV1) + np.linalg.norm(DV2)

    print(DV)

mycluster.pretty()