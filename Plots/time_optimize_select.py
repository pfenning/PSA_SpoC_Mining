# import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as pp

pp.rcParams.update({
    "text.usetex": True,
    "font.family" : "serif",
    "font.serif"  : "roman"})

def fig_settings(num):
    scale = 0.6
    return pp.figure(num, (scale*width,3/4*scale*width), dpi=900)

def plot_setting(xlabel, ylabel, ax):
    # pp.subplots_adjust(bottom=0.21, left=0.1, right=0.96, top=0.91)
    ax.tick_params(axis='both', which='major', labelsize=9)
    ax.ticklabel_format(axis='y', scilimits=(0, 0))
    ax.set_xlabel(xlabel, fontsize=11)  # , loc="right"
    ax.set_ylabel(ylabel, fontsize=11)  # , loc="top"
    # pp.axes().set_aspect(2.0)

# Maße von DinA4 in inches
width = 8.27
height = 11.69

def flugzeit_starttag(fig, ax):
    ####################
    # Flugzeit auswählen
    ####################
    t_flug_1 = np.linspace(1, 30, 100)
    t_start_var = np.linspace(-7, 30, 100)
    dv_t_flug = np.linspace(500, 5000, 100)

    temperature_flug = np.zeros((len(dv_t_flug), len(t_flug_1)))

    for i in range(len(t_flug_1)):
        for j in range(len(dv_t_flug)):
            temperature_flug[j,i] = 0.3 * t_flug_1[i] / 22 \
                                    + 0.2 * 10000 / 2100 * (dv_t_flug[j] / (10000 - dv_t_flug[j]))
    ####################
    # Starttag auswählen
    ####################
    temperature_start = np.zeros((len(dv_t_flug), len(t_start_var)))

    for i in range(len(t_start_var)):
        for j in range(len(dv_t_flug)):
            temperature_start[j, i] = 0.3 * abs(t_start_var[i]) / 7 \
                                      + 0.2 * 10000 / 2100 * (dv_t_flug[j] / (10000 - dv_t_flug[j]))

    # Levels
    t_min = np.min([temperature_flug, temperature_start])
    t_max = np.max([temperature_flug, temperature_start])
    my_levels = np.linspace(t_min, t_max, 40)

    # print(np.min(temperature_start), np.max(temperature_start))
    # print(np.min(temperature_flug), np.max(temperature_flug))
    # print(t_min, t_max)

    # t_min, t_max = np.min(temperature_flug), np.max(temperature_flug)
    # my_levels = np.linspace(t_min, t_max, 15)
    
    # Plotten
    pp.subplot(121)
    X_f, Y_f = np.meshgrid(t_flug_1, dv_t_flug)
    our_plot = ax[0].contourf(X_f, Y_f, temperature_flug, levels=my_levels, vmin=t_min, v_max=t_max) # , vmin=t_min, v_max=t_max
    plot_setting(r'$t_\mathrm{f} \; (Tage)$', r'$\Delta v \; (\frac{m}{s^2})$', ax[0])

    # t_min, t_max = np.min(temperature_start), np.max(temperature_start)
    # my_levels = np.linspace(t_min, t_max, 15)

    # Plotten
    pp.subplot(122)
    X_s, Y_s = np.meshgrid(t_start_var, dv_t_flug)
    our_plot = ax[1].contourf(X_s, Y_s, temperature_start, levels=my_levels, vmin=t_min, v_max=t_max)    # , vmin=t_min, v_max=t_max
    plot_setting(r'$t_\mathrm{m} -t_\mathrm{opt} \; (Tage)$', r'', ax[1])   # $\Delta v \; (\frac{m}{s^2})$
    # ax[1].set_xticks(np.concatenate((ax[1].get_xticks(),-7)) )
    # Colorbar hinzufügen
    colorbar = fig.colorbar(mappable=None, cmap='viridis', spacing='uniform')
    ticks = np.linspace(0, 1, 4)
    colorbar.set_ticks(ticks)
    colorbar.set_ticklabels(np.linspace(t_min,t_max, 4).round(1))

    return "flugzeit"+"starttag"

# def starttag():
#     ####################
#     # Starttag auswählen
#     ####################
#     t_start_var = np.linspace(-7, 45, 100)
#     dv_t_flug = np.linspace(500, 5000, 100)
#
#     temperature = np.zeros((len(dv_t_flug), len(t_start_var)))
#
#     for i in range(len(t_start_var)):
#         for j in range(len(dv_t_flug)):
#             temperature[j,i] = 0.3 * abs(t_start_var[i])/7 + 0.2* 10000/2100 * (dv_t_flug[j] / (10000-dv_t_flug[j]))
#
#     X,Y = np.meshgrid(t_start_var, dv_t_flug)
#
#     print(temperature)
#
#     # Plotten
#     # fig2 = fig_settings(2)
#     t_min = np.min(temperature)
#     t_max = np.max(temperature)
#     my_levels = np.linspace(t_min,t_max,15)
#
#     plot_setting(r'$t_\mathrm{f} \; (Tage)$', r'$\Delta v \; (\frac{m}{s^2})$', plt.gca())
#     #
#     # ax = plt.gca()
#     # ax.tick_params(axis='both', which='major', labelsize=7)
#     # ax.ticklabel_format(axis='y', scilimits=(0,0))
#     # ax.set_xlabel(r'$t_\mathrm{f}$ (day)', fontsize = 10, loc = "right")
#     # ax.set_ylabel(r'$\Delta v \, (\frac{m}{s^2})$', fontsize = 10, loc = "top")
#     our_plot = pp.contourf(X,Y,temperature,levels=my_levels)
#     return "starttag", my_levels

# name = flugzeit()
# fig = pp.figure(figsize=(0.5*width, 0.25*width), dpi=900)
fig, ax = pp.subplots(1, 2, sharey='all', figsize=(0.5*width, 0.25*width), dpi=900,
                      gridspec_kw={'width_ratios': [1, 1.25]})
pp.subplots_adjust(left=0.1, bottom=0.21, right=0.97, top=0.91, wspace=0.1, hspace=0.2)
# fig.add_subplot(121)
# name1, level1 = flugzeit()
# fig.add_subplot(122)
# name2, level2 = starttag()
# t_min =
# fig.colorbar(mappable=True)
name = flugzeit_starttag(fig, ax)
pp.show()
pp.savefig(name + '.eps', format='eps')