# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde

# Importieren von Mathekonstanten
from math import pi

# Konstanten und Database Laden
from spoc_constants import data, asteroids

##########
# Tests
#########

# Analyse der Keplerparameter auf Cluster:
# Creating Figure object
fig = plt.figure()
# Beschreibung der Ellipse:
semi_major = []
eccentricity = []
# Orientierung und Lage der Elipse in der Referenzebene
inclination = []
ascending_node = []
arg_of_perapsis = []
# True Anomaly nicht wichtig für Orbit-Clustererung

for line in data:
    # Beschreibung der Elipse:
    semi_major.append(line[1])
    eccentricity.append(line[2])
    # Orientierung und Lage der Ellipse in der Referenzebene
    inclination.append(line[3] * pk.RAD2DEG)  # Umrechnung rad in Grad
    ascending_node.append(line[4] * pk.RAD2DEG)
    arg_of_perapsis.append(line[5] * pk.RAD2DEG)

# Plotten der verschiedenen größen einzeln, zur Bestimmung der Dichte-Verteilungen

# Semi-Major
""" Summe von Perarpsis (kleinster Abstand der zwei Himmelskörper) und Apoapsis (größter Abstand) """
prob_density = kde.gaussian_kde(semi_major)
prob_density.covariance_factor = lambda: .15  # Glättung verringern (=kleinere Zahl)
prob_density._compute_covariance()

x = np.linspace(min(semi_major), max(semi_major), 300)
y = prob_density(x)
plt.subplot(2, 3, 1)
plt.plot(x, y)
plt.title("Density of Semi-Major-Axis [m]")

# Eccentricity
""" Form der Elipse im Vergleich zum Keris """
prob_density = kde.gaussian_kde(eccentricity)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(eccentricity), max(eccentricity), 300)
y = prob_density(x)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

plt.subplot(2, 3, 2)
plt.plot(x, y)
plt.title("Density of Eccentricity")

# Inclination
""" Neigung der Elipse an der Ascending Node (Schnittpunkt von Elipse und Referenzebene) """
prob_density = kde.gaussian_kde(inclination)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(inclination), max(inclination), 300)
y = prob_density(x)
plt.subplot(2, 3, 3)
plt.plot(x, y)
plt.title("Density of Inclination [Grad]")

# Longitude of the ascending node
""" Winkel zwischen Referenzrichtung und Ascending Node-Richtung """
prob_density = kde.gaussian_kde(ascending_node)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(ascending_node), max(ascending_node), 300)
y = prob_density(x)
plt.subplot(2, 3, 4)
plt.plot(x, y)
plt.title("Density of Longitude of the \n ascending node [Grad]")

# Argument of Perapsis
""" Winkel der Periapsis bezogen auf Longitude of ascending node = Orientierung der "Spitze" der Elipse. Ob diese eher am weitesten von Referenzebene entfernt ist (90°/270°), oder in der Ebene liegt (0°/180°)) """
prob_density = kde.gaussian_kde(arg_of_perapsis)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(arg_of_perapsis), max(arg_of_perapsis), 300)
y = prob_density(x)
plt.subplot(2, 3, 5)
plt.plot(x, y)
plt.title("Density of Argument of Perapsis [Grad]")

################Verteilung der Periodendauer
# myasteroid = asteroids[3]
# T = myasteroid.compute_period(epoch(5))
# print('Periodendauer von %(name)s sind %(number)f Sekunden' %{"name": myasteroid.name, "number": T})

period = []
for asteroid in asteroids:
    period.append(
        asteroid.compute_period(epoch(0)) / (24 * 60 * 60)  # Sekunden in Tage umrechnen
    )

# Periodendauer einer Orbitumrundung:
prob_density = kde.gaussian_kde(period)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(period), max(period), 300)
y = prob_density(x)
plt.subplot(2, 3, 6)
plt.plot(x, y)
plt.title("Density of Orbit-Period [days]")

# Plot anzeigen
plt.subplots_adjust(left=0.065, bottom=0.065, right=0.935, top=0.885, wspace=0.3, hspace=0.5)
plt.show()
