import pykep as pk
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.subplots()
pl = pk.planet.jpl_lp('earth')
ax = pk.orbit_plots.plot_planet(pl, t0=0, tf=None, N=60, units=1.0,  color='b', axes= None)
plt.show()