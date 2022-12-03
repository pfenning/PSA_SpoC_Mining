# ToDo - muss noch output-function fine-tunen/besprechen
#      - sprit ist wichtig

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting
import random
from skfuzzy import control as ctrl

# Normierte Werte
# Abweichung, Bestand, Tank nach, Tank jetzt, Delta v, Masse
# inputs
bes = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Bestand')
delt = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Spritverbrauch')
mas = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Masse')
# erst abw, t_j,t_n, delt weglassen --> abw unnötig, wenn wir schon bestand so berechnen!!
# abw = ctrl.Antecedent(np.arange(0, 1, 0.01), 'Abweichung')
# t_n = ctrl.Antecedent(np.arange(0, 1, 0.01), 'Tank nach Wechsel')
# t_j = ctrl.Antecedent(np.arange(0, 1, 0.01), 'Tank vor Wechsel')

# output
out = ctrl.Consequent(np.arange(0, 1, 0.01), 'Güte des Asteroids')

# Generate fuzzy membership functions
# abw['lo'] = fuzz.trimf(abw.universe, [0, 0, 1])
# abw['hi'] = fuzz.trimf(abw.universe, [0, 1, 1])
bes['lo'] = fuzz.trimf(bes.universe, [0, 0, 0.33])
bes['md'] = fuzz.trimf(bes.universe, [0, 0.33, 0.66])
bes['hi'] = fuzz.trapmf(bes.universe, [0.33, 0.66, 1, 1])
# t_n.automf(3)
# t_j.automf(3)
# delt.automf(3)
delt['lo'] = fuzz.trapmf(delt.universe, [0, 0, 0.15, 0.85])
delt['hi'] = fuzz.trapmf(delt.universe, [0.15, 0.85, 1, 1])
mas.automf(3)  # Automatisch X Member-Functions erstellen
out.automf(7)

# Visualize these membership functions
# abw.view()
# bes.view()
# t_n.view()
# t_j.view()
# delt.view()
# mas.view()
# out.view()
# plt.show()

# Rule base
# dismal, poor, mediocre, average, decent, good, excellent
# ToDo muss noch output fine-tunen/ besprechen
rule01 = ctrl.Rule(bes['lo'] & mas['poor'] & delt['lo'], out['average'])
rule02 = ctrl.Rule(bes['lo'] & mas['poor'] & delt['hi'], out['mediocre'])
rule03 = ctrl.Rule(bes['lo'] & mas['average'] & delt['lo'], out['good'])
rule04 = ctrl.Rule(bes['lo'] & mas['average'] & delt['hi'], out['average'])
rule05 = ctrl.Rule(bes['lo'] & mas['good'] & delt['lo'], out['excellent'])
rule06 = ctrl.Rule(bes['lo'] & mas['good'] & delt['hi'], out['decent'])

rule07 = ctrl.Rule(bes['md'] & mas['poor'] & delt['lo'], out['mediocre'])
rule08 = ctrl.Rule(bes['md'] & mas['poor'] & delt['hi'], out['poor'])
rule09 = ctrl.Rule(bes['md'] & mas['average'] & delt['lo'], out['decent'])
rule10 = ctrl.Rule(bes['md'] & mas['average'] & delt['hi'], out['mediocre'])
rule11 = ctrl.Rule(bes['md'] & mas['good'] & delt['lo'], out['good'])
rule12 = ctrl.Rule(bes['md'] & mas['good'] & delt['hi'], out['average'])

rule13 = ctrl.Rule(bes['hi'] & mas['poor'] & delt['lo'], out['dismal'])
rule14 = ctrl.Rule(bes['hi'] & mas['poor'] & delt['hi'], out['dismal'])
rule15 = ctrl.Rule(bes['hi'] & mas['average'] & delt['lo'], out['poor'])
rule16 = ctrl.Rule(bes['hi'] & mas['average'] & delt['hi'], out['dismal'])
rule17 = ctrl.Rule(bes['hi'] & mas['good'] & delt['lo'], out['mediocre'])
rule18 = ctrl.Rule(bes['hi'] & mas['good'] & delt['hi'], out['poor'])

space_ctrl = ctrl.ControlSystem(
    [rule01, rule02, rule03, rule04, rule05, rule06, rule07, rule08, rule09, rule10, rule11, rule12, rule13, rule14,
     rule15, rule16, rule17, rule18])

guete = ctrl.ControlSystemSimulation(space_ctrl)


"""Testformat"""
# Test-Grid erzeugen
bes_test = [0, 0.35, 0.65, 1]
resolution = np.arange(0, 1.1, 0.1)
mas_test = np.arange(0, 1.1, 0.1)
delta_test = np.arange(0, 1.1, 0.1)
x, y = np.meshgrid(mas_test, delta_test)

fig = plt.figure()
# fig, axs = plt.subplots(nrows=2, ncols=2, sharex='all', figsize=(12, 12))

for i in range(0, len(bes_test)):
    out = np.zeros_like(x)
    guete.input['Bestand'] = bes_test[i]

    for m in range(0, len(mas_test)):
        guete.input['Masse'] = mas_test[m]
        for n in range(0, len(delta_test)):
            guete.input['Spritverbrauch'] = delta_test[n]
            guete.compute()

            out[m, n] = guete.output['Güte des Asteroids']

    if i == 0:
        subplot = 221
        ax1 = fig.add_subplot(subplot, projection='3d') # subplot,
        surf = ax1.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
        # ax1.set_title("Bestand = ", bes_test[i])
    elif i == 1:
        subplot = 222
        ax2 = fig.add_subplot(subplot, projection='3d')
        surf = ax2.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
    elif i == 2:
        subplot = 223
        ax3 = fig.add_subplot(subplot, projection='3d')
        surf = ax3.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
    elif i == 3:
        subplot = 224
        ax4 = fig.add_subplot(subplot, projection='3d')
        surf = ax4.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
    plt.xlabel("Masse")
    plt.ylabel("Delta V")
    # Projektion auf Wände
    # cset = ax.contourf(x, y, out, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
    # cset = ax.contourf(x, y, out, zdir='x', offset=3, cmap='viridis', alpha=0.5)
    # cset = ax.contourf(x, y, out, zdir='y', offset=3, cmap='viridis', alpha=0.5)


# Blickwinkel auf 3D-Plots
ax1.view_init(330, 200)
ax2.view_init(330, 200)
ax3.view_init(330, 200)
ax4.view_init(330, 200)

plt.show()


# for x in range(0, 10):
#     a = round(random.random(), 2)
#     b = round(random.random(), 2)
#     c = round(random.random(), 2)
#
#     # a = 0.5
#     # b = 0.5
#     # c = 0.5
#
#     guete.input['Bestand'] = a
#     guete.input['Masse'] = b
#     guete.input['Spritverbrauch'] = c
#
#     # Crunch the numbers
#     guete.compute()
#     print("Der Bestand ", a, "Mit Masse ", b,"Mit ein Spritverbrauch ", c,
#           "Führt zu einer Güte von:", round(guete.output['Güte des Asteroids'], 2))
#     # out.view(sim=guete)
#     plt.show()