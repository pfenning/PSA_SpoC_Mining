from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import pykep as pk
from SpoC_Constants import data, T_START, dict_asteroids, T_START
 



# print(dict_asteroids[0][0]) # <class 'pykep.planet.planet.keplerian'>
# print(np.array(dict_asteroids[0][0].eph(T_START.mjd2000)[0])) # r  vom kepler-Element als np-array

# Or-bit-Plot eines einzigen Asteroiden

# fig = plt.figure()
ax = pk.orbit_plots.plot_planet(dict_asteroids[3622][0])

plt.show()

# fig = plt.figure()
# ax = pk.orbit_plots.plot_planet(dict_asteroids[5384][0])
# plt.show()

# fig = plt.figure()
# ax = pk.orbit_plots.plot_planet(dict_asteroids[2257][0])
# plt.show()

# fig = plt.figure()
# ax = pk.orbit_plots.plot_planet(dict_asteroids[925][0])
# plt.show()


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



