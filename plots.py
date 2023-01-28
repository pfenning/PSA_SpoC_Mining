# Packages laden
import numpy as np
import pykep as pk
from pykep import epoch, AU
import matplotlib.pyplot as plt
from scipy.stats import kde
from SpoC_Constants import data, T_START, dict_asteroids, abbau, get_dv, DV_per_propellant, get_asteroid_material, get_asteroid_mass, get_asteroid

# Importieren von Mathekonstanten
from math import pi

# Konstanten und Database Laden
from from_website.SpoC_Kontrolle import asteroids, asteroid_masses, asteroid_materials, MU_TRAPPIST

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



#####################
#   Eccentricity    #
#####################

""" Form der Elipse im Vergleich zum Kreiis """
x = np.arange(0, 9999, 1)
y = np.linspace(min(eccentricity), max(eccentricity))


# prob_density = kde.gaussian_kde(eccentricity)
# prob_density.covariance_factor = lambda: .05
# prob_density._compute_covariance()

# x = np.linspace(min(eccentricity), max(eccentricity), 100)
# y = prob_density(x)
# prob_density.covariance_factor = lambda: .05
# prob_density._compute_covariance()

#plt.subplot(2, 3, 2)
# plt.plot(x, y)
# plt.title("Density of Eccentricity")
# plt.show()


# x=[]
# y=[]
# for ast in data:
#     # if dict_asteroids[position][-1] == 1:
#     #     x.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[0])
#     #     y.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[1])
#     #     z.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[2])
#     x.append(ast[0])
#     y.append(ast[2])
# # Creating figure
# # fig = plt.figure(figsize = (10, 7))
# # ax = plt.axes(projection ="3d")
# fig, ax = plt.subplots()
# # Creating plot
# ax.scatter(x, y, color = "grey")
# plt.title("Verteilung der Exzentrizität")
# show plot
# plt.show()



#######################
#   Plots of orbits   #
#######################


import matplotlib.pyplot as plt
from pykep.orbit_plots import plot_planet, plot_lambert
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from tkinter import *

import numpy as np
from TripInSpace import TripInSpace

t0 = T_START.mjd2000

fig = plt.figure()
ax1 = plt.axes(projection='3d')
ax1.scatter([0],[0],[0], color=['y'])

ax1.view_init(90,0)
# pk.orbit_plots.plot_planet(dict_asteroids[5125][0], t0=5, color='b', units=AU, axes=ax1, s=0)
# pk.orbit_plots.plot_planet(dict_asteroids[3767][0], t0=5, color='b', units=AU, axes=ax1, s=0)
# pk.orbit_plots.plot_planet(dict_asteroids[9146][0], t0=5, color='r', units=AU, axes=ax1, s=0)
# pk.orbit_plots.plot_planet(dict_asteroids[205][0], t0=5, color='r', units=AU, axes=ax1, s=0)

x=[]
y=[]
z=[]
for position in asteroids:
    x.append(np.array(position.eph(T_START.mjd2000+60)[0])[0])
    y.append(np.array(position.eph(T_START.mjd2000+60)[0])[1])
    z.append(np.array(position.eph(T_START.mjd2000+60)[0])[2])

# x1=x[0:3]
# y1=y[0:3]
# z1=z[0:3]
# x2=x[4:7]
# y2=y[4:7]
# z2=z[4:7]
ax1.scatter3D(x,y,z, alpha=0.1)

# # Exzentrizität
# ax1.scatter3D(x[5125],y[5125],z[5125], color='b')
# ax1.scatter3D(x[3767],y[3767],z[3767], color='b')

# # Semimajor
# ax1.scatter3D(x[9146],y[9146],z[9146], color='b')
# ax1.scatter3D(x[205],y[205],z[205], color='b')


plt.show()


