from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import pykep as pk
 

T_START = pk.epoch_from_iso_string("30190302T000000")  # Start and end epochs
T_END = pk.epoch_from_iso_string("30240302T000000")
T_DAUER = 1827
G = 6.67430e-11  # Cavendish constant (m^3/s^2/kg)
SM = 1.989e30  # Sun_mass (kg)
MS = 8.98266512e-2 * SM  # Mass of the Trappist-1 star
MU_TRAPPIST = G * MS  # Mu of the Trappist-1 star
DV_per_propellant = 10000  # DV per propellant [m/s]
TIME_TO_MINE_FULLY = 30  # Maximum time to fully mine an asteroid


# creating data as kepler-data
data = np.loadtxt("SpoC_Datensatz.txt")
dict_asteroids ={int(line[0]):  # ID
    [pk.planet.keplerian(       # Keplerian-Object
        T_START,
        (
            line[1],
            line[2],
            line[3],
            line[4],
            line[5],
            line[6]
        ),
        MU_TRAPPIST,
        G * line[7],    # mass in planet is not used in UDP, instead separate array below
        1,              # these variable are not relevant for this problem
        1.1,            # these variable are not relevant for this problem
        "Asteroid " + str(int(line[0]))),
        line[-2],               # Mass
        int(line[-1])]          # Material
    for line in data}

# print(dict_asteroids[0][0]) # <class 'pykep.planet.planet.keplerian'>
# print(np.array(dict_asteroids[0][0].eph(T_START.mjd2000)[0])) # r  vom kepler-Element als np-array

# Or-bit-Plot eines einzigen Asteroiden

fig = plt.figure()
ax = pk.orbit_plots.plot_planet(dict_asteroids[3622][0])
plt.show()

fig = plt.figure()
ax = pk.orbit_plots.plot_planet(dict_asteroids[5384][0])
plt.show()

fig = plt.figure()
ax = pk.orbit_plots.plot_planet(dict_asteroids[2257][0])
plt.show()

fig = plt.figure()
ax = pk.orbit_plots.plot_planet(dict_asteroids[925][0])
plt.show()


# start_asts = [3622, 5384, 2257, 925]
# x=[]
# y=[]
# z=[]
# for position in start_asts:
#     # if dict_asteroids[position][-1] == 1:
#     #     x.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[0])
#     #     y.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[1])
#     #     z.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[2])
#     x.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[0])
#     y.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[1])
#     z.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[2])
# # Creating figure
# fig = plt.figure(figsize = (10, 7))
# ax = plt.axes(projection ="3d")
# # Creating plot
# ax.scatter3D(x, y, z, color = "red")
# plt.title("simple 3D scatter plot")
# # show plot
# plt.show()



