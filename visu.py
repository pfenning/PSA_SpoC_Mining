# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch
import matplotlib.pyplot as plt
from scipy.stats import kde

# Importieren von Mathekonstanten
from math import pi

# Konstanten und Database Laden
from from_website.SpoC_Kontrolle import data, asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST

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
# Massenverteilung auf Asteroiden
asteroid_masses = data[:, -2]
# Verfügbarkeit der Materialien
asteroid_materials = data[:, -1].astype(int)

for line in data:
    # Beschreibung der Elipse:
    semi_major.append(line[1])
    eccentricity.append(line[2])
    # Orientierung und Lage der Ellipse in der Referenzebene
    inclination.append(line[3] * pk.RAD2DEG)  # Umrechnung rad in Grad
    ascending_node.append(line[4] * pk.RAD2DEG)
    arg_of_perapsis.append(line[5] * pk.RAD2DEG)

# # Plotten der verschiedenen größen einzeln, zur Bestimmung der Dichte-Verteilungen

# Semi-Major
""" Summe von Perarpsis (kleinster Abstand der zwei Himmelskörper) und Apoapsis (größter Abstand) """
prob_density = kde.gaussian_kde(semi_major)
prob_density.covariance_factor = lambda: .15  # Glättung verringern (=kleinere Zahl)
prob_density._compute_covariance()

x = np.linspace(min(semi_major), max(semi_major), 300)
y = prob_density(x)
#plt.subplot(2, 3, 1)
plt.plot(x, y)
plt.title("Density of Semi-Major-Axis [m]")
plt.show()

# Eccentricity
""" Form der Elipse im Vergleich zum Keris """
prob_density = kde.gaussian_kde(eccentricity)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(eccentricity), max(eccentricity), 300)
y = prob_density(x)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

#plt.subplot(2, 3, 2)
plt.plot(x, y)
plt.title("Density of Eccentricity")
plt.show()

# Inclination
""" Neigung der Elipse an der Ascending Node (Schnittpunkt von Elipse und Referenzebene) """
prob_density = kde.gaussian_kde(inclination)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(inclination), max(inclination), 300)
y = prob_density(x)
#plt.subplot(2, 3, 3)
plt.plot(x, y)
plt.title("Density of Inclination [Grad]")
plt.show()

# Longitude of the ascending node
""" Winkel zwischen Referenzrichtung und Ascending Node-Richtung """
prob_density = kde.gaussian_kde(ascending_node)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(ascending_node), max(ascending_node), 300)
y = prob_density(x)
#plt.subplot(2, 3, 4)
plt.plot(x, y)
plt.title("Density of Longitude of the \n ascending node [Grad]")
plt.show()

# Argument of Perapsis
""" Winkel der Periapsis bezogen auf Longitude of ascending node = Orientierung der "Spitze" der Elipse. Ob diese eher am weitesten von Referenzebene entfernt ist (90°/270°), oder in der Ebene liegt (0°/180°)) """
prob_density = kde.gaussian_kde(arg_of_perapsis)
prob_density.covariance_factor = lambda: .05
prob_density._compute_covariance()

x = np.linspace(min(arg_of_perapsis), max(arg_of_perapsis), 300)
y = prob_density(x)
#plt.subplot(2, 3, 5)
plt.plot(x, y)
plt.title("Density of Argument of Perapsis [Grad]")
plt.show()

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
#plt.subplot(2, 3, 6)
plt.plot(x, y)
plt.title("Density of Orbit-Period [days]")
plt.show()

# # Plot anzeigen
# plt.subplots_adjust(left=0.065, bottom=0.065, right=0.935, top=0.885, wspace=0.3, hspace=0.5)
# plt.show()

x = np.arange(0, 10000, 1)
y = asteroid_masses
plt.scatter(x, y,s=2)
plt.xlabel("Asteroid-ID")
plt.ylabel("Masse")
plt.show()

asteroid_masses_rounded = np.round_(data[:, -2], decimals = 2)
unique, counts = np.unique(asteroid_masses_rounded, return_counts=True)
#print(np.asarray((unique, counts)).T)
#plt.bar(unique, counts, color ='maroon',width = 0.005)
plt.plot(unique, counts)
x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
labels = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
plt.xticks(x, labels)
plt.xlabel("Masse")
plt.ylabel("Vorkommen")
plt.show()

semi_major_norm = (semi_major-np.min(semi_major))/(np.max(semi_major)-np.min(semi_major))
y = asteroid_masses
plt.scatter(semi_major_norm, y,s=2)
plt.xlabel("Semi-major")
plt.ylabel("Masse")
plt.show()

unique_2, counts_2 = np.unique(asteroid_materials, return_counts=True)
plt.bar(unique_2, counts_2, color ='maroon',width = 0.5)
#plt.plot(unique, counts)
x = [0,1,2,3]
labels = [0,1,2,3]
plt.xticks(x, labels)
plt.xlabel("Mat. Typ")
plt.ylabel("Anzahl Asteroiden")
plt.show()

mass_mat_0 = asteroid_masses[asteroid_materials == 0]
mass_mat_1 = asteroid_masses[asteroid_materials == 1]
mass_mat_2 = asteroid_masses[asteroid_materials == 2]
mass_mat_3 = asteroid_masses[asteroid_materials == 3]



mat0 = plt.scatter(np.arange(0, mass_mat_0.size, 1), mass_mat_0,s=2)
mat1 = plt.scatter(np.arange(0, mass_mat_1.size, 1), mass_mat_1,s=2)
mat2 = plt.scatter(np.arange(0, mass_mat_2.size, 1), mass_mat_2,s=2)
mat3 = plt.scatter(np.arange(0, mass_mat_3.size, 1), mass_mat_3,s=2)
plt.legend((mat0, mat1, mat2, mat3),
           ('Mat. 0', 'Mat. 1', 'Mat. 2', 'Mat. 3'),
           scatterpoints=1,
           loc='upper right',
           ncol=1,
           fontsize=8)
plt.xlabel("Asteroid-ID")
plt.ylabel("Masse")
plt.show()

asteroid_masses_rounded = np.round_(data[:, -2], decimals = 1)
mass_mat_0_round = asteroid_masses_rounded[asteroid_materials == 0]
mass_mat_1_round = asteroid_masses_rounded[asteroid_materials == 1]
mass_mat_2_round = asteroid_masses_rounded[asteroid_materials == 2]
mass_mat_3_round = asteroid_masses_rounded[asteroid_materials == 3]
unique0, counts0 = np.unique(mass_mat_0_round, return_counts=True)
unique1, counts1 = np.unique(mass_mat_1_round, return_counts=True)
unique2, counts2 = np.unique(mass_mat_2_round, return_counts=True)
unique3, counts3 = np.unique(mass_mat_3_round, return_counts=True)
mat0 = plt.bar(unique0-0.02, counts0, color ='maroon',width = 0.02 )
mat1 = plt.bar(unique1, counts1, color ='k',width = 0.02)
mat2 = plt.bar(unique2+0.02, counts2, color ='g',width = 0.02)
mat3 = plt.bar(unique3+0.04, counts3, color ='b',width = 0.02)
x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
labels = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
plt.xticks(x, labels)
plt.legend((mat0, mat1, mat2, mat3),
           ('Mat. 0', 'Mat. 1', 'Mat. 2', 'Mat. 3'),
           scatterpoints=1,
           loc='upper right',
           ncol=1,
           fontsize=8)
plt.xlabel("Masse")
plt.ylabel("Vorkommen")
plt.show()





