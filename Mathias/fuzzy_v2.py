# ToDo
#   - sprit ist wichtig -> spritasteroid?
#   - get_fct für Verfügbarkeit der Materialien => unteres und oberes Limit

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import random
import time
from skfuzzy import control as ctrl

# Normierte Werte
# inputs
mas = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Masse')
sprit = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Güte vom Spritverbrauch')
rele = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Relevanz des Materials')
# subsys 1
t_n = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Tank nach Wechsel')
delt = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Spritverbrauch')
out_sub = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'Ausgang Subsys')
# subsys 2
upper = 0.4  # get fkt für mat den wir am meisten haben
lower = 0.03  # get fkt für mat den wir am wenigsten haben
verf = ctrl.Antecedent(np.arange(lower, upper + 0.01, 0.01), 'Verfügbarkeit des Materials')
bes = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Bestand des Materials')
out_sub_2 = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'Ausgang Subsys 2')
# output
out = ctrl.Consequent(np.arange(0, 1, 0.01), 'Güte des Asteroids')

# Generate fuzzy membership functions
bes['lo'] = fuzz.trimf(bes.universe, [0, 0, 0.33])
bes['md'] = fuzz.trimf(bes.universe, [0, 0.33, 0.66])
bes['hi'] = fuzz.trapmf(bes.universe, [0.33, 0.66, 1, 1])
delt['lo'] = fuzz.trapmf(delt.universe, [0, 0, 0.1, 0.23])
delt['md'] = fuzz.trimf(delt.universe, [0.1, 0.23, 0.37])
delt['hi'] = fuzz.trapmf(delt.universe, [0.23, 0.37, 1, 1])
t_n.automf(3)
rele.automf(3)
verf['lo'] = fuzz.trimf(verf.universe, [lower, lower, upper])
verf['hi'] = fuzz.trimf(verf.universe, [lower, upper, upper])
sprit['lo'] = fuzz.trimf(sprit.universe, [0, 0, 1])
sprit['hi'] = fuzz.trimf(sprit.universe, [0, 1, 1])
mas.automf(3)
out_sub.automf(7)
out_sub_2.automf(5)
out.automf(7)

# Visualize these membership functions
# bes.view()
# t_n.view()
# delt.view()
# sprit.view()
# rele.viwe()
# verf.view()
# mas.view()
# out_sub.view()
# out_sub_2.view()
# out.view()
# plt.show()

# Rule base
# dismal, poor, mediocre, average, decent, good, excellent

# Abfrage von Tank Todo
# Hyperparam --> Schwellwert

# subsys 1 - Sprit
rule_subs1 = ctrl.Rule(t_n['poor'] & delt['lo'], out_sub['mediocre'])
rule_subs2 = ctrl.Rule(t_n['poor'] & delt['md'], out_sub['poor'])
rule_subs3 = ctrl.Rule(t_n['poor'] & delt['hi'], out_sub['dismal'])
rule_subs4 = ctrl.Rule(t_n['average'] & delt['lo'], out_sub['decent'])
rule_subs5 = ctrl.Rule(t_n['average'] & delt['md'], out_sub['average'])
rule_subs6 = ctrl.Rule(t_n['average'] & delt['hi'], out_sub['mediocre'])
rule_subs7 = ctrl.Rule(t_n['good'] & delt['lo'], out_sub['excellent'])
rule_subs8 = ctrl.Rule(t_n['good'] & delt['md'], out_sub['good'])
rule_subs9 = ctrl.Rule(t_n['good'] & delt['hi'], out_sub['decent'])

sub_ctrl = ctrl.ControlSystem(
    [rule_subs1, rule_subs2, rule_subs3, rule_subs4, rule_subs5, rule_subs6, rule_subs7, rule_subs8, rule_subs9])
sub_sys = ctrl.ControlSystemSimulation(sub_ctrl)

# subsys 2 - Relevanz Material
rule_subs_2_1 = ctrl.Rule(verf['lo'] & bes['lo'], out_sub_2['good'])
rule_subs_2_2 = ctrl.Rule(verf['lo'] & bes['md'], out_sub_2['decent'])
rule_subs_2_3 = ctrl.Rule(verf['lo'] & bes['hi'], out_sub_2['average'])
rule_subs_2_4 = ctrl.Rule(verf['hi'] & bes['lo'], out_sub_2['average'])
rule_subs_2_5 = ctrl.Rule(verf['hi'] & bes['md'], out_sub_2['mediocre'])
rule_subs_2_6 = ctrl.Rule(verf['hi'] & bes['hi'], out_sub_2['poor'])

sub_ctrl_2 = ctrl.ControlSystem(
    [rule_subs_2_1, rule_subs_2_2, rule_subs_2_3, rule_subs_2_4, rule_subs_2_5, rule_subs_2_6])
sub_sys_2 = ctrl.ControlSystemSimulation(sub_ctrl_2)

# sys
rule1 = ctrl.Rule(rele['good'] & mas['poor'] & sprit['hi'], out['average'])
rule2 = ctrl.Rule(rele['good'] & mas['poor'] & sprit['lo'], out['mediocre'])
rule3 = ctrl.Rule(rele['good'] & mas['average'] & sprit['hi'], out['good'])
rule4 = ctrl.Rule(rele['good'] & mas['average'] & sprit['lo'], out['average'])
rule5 = ctrl.Rule(rele['good'] & mas['good'] & sprit['hi'], out['excellent'])
rule6 = ctrl.Rule(rele['good'] & mas['good'] & sprit['lo'], out['decent'])

rule7 = ctrl.Rule(rele['average'] & mas['poor'] & sprit['hi'], out['mediocre'])
rule8 = ctrl.Rule(rele['average'] & mas['poor'] & sprit['lo'], out['poor'])
rule9 = ctrl.Rule(rele['average'] & mas['average'] & sprit['hi'], out['decent'])
rule10 = ctrl.Rule(rele['average'] & mas['average'] & sprit['lo'], out['mediocre'])
rule11 = ctrl.Rule(rele['average'] & mas['good'] & sprit['hi'], out['good'])
rule12 = ctrl.Rule(rele['average'] & mas['good'] & sprit['lo'], out['average'])

rule13 = ctrl.Rule(rele['poor'] & mas['poor'] & sprit['hi'], out['dismal'])
rule14 = ctrl.Rule(rele['poor'] & mas['poor'] & sprit['lo'], out['dismal'])
rule15 = ctrl.Rule(rele['poor'] & mas['average'] & sprit['hi'], out['poor'])
rule16 = ctrl.Rule(rele['poor'] & mas['average'] & sprit['lo'], out['dismal'])
rule17 = ctrl.Rule(rele['poor'] & mas['good'] & sprit['hi'], out['mediocre'])
rule18 = ctrl.Rule(rele['poor'] & mas['good'] & sprit['lo'], out['poor'])

space_ctrl = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15,
     rule16, rule17, rule18])
guete = ctrl.ControlSystemSimulation(space_ctrl)


"""Testformat:
    Subsysteme einzeln,
    daraus Wertebereiche Bestimmen
    Hauptsystem für die gegebenen Wertebereiche
"""
fig = plt.figure(figsize=(12, 18))

# Subsystem 1 - Sprit
# Inputs festlegen
t_n_test = np.arange(0, 1.1, 0.1)
delt_test = np.arange(0, 1.1, 0.1)
x_sub1, y_sub1 = np.meshgrid(t_n_test, delt_test, indexing='ij')
out_sub1_test = np.zeros_like(x_sub1)
# Auswerten
for m in range(0, len(t_n_test)):
    sub_sys.input['Tank nach Wechsel'] = t_n_test[m]
    for n in range(0, len(delt_test)):
        sub_sys.input['Spritverbrauch'] = delt_test[n]
        sub_sys.compute()

        out_sub1_test[m, n] = sub_sys.output['Ausgang Subsys']
# Plotten
subplot = 321
ax1 = fig.add_subplot(subplot, projection='3d')
surf = ax1.plot_surface(x_sub1, y_sub1, out_sub1_test, rstride=1, cstride=1, cmap='viridis',
                        linewidth=0.4, antialiased=True)
plt.xlabel("Tank nach Wechsel")
plt.ylabel("Delta V")
plt.title("Subsystem Sprit")

# Subsystem 2 - Material
bes_test = np.arange(0, 1.1, 0.1)
verf_test = np.linspace(lower, upper, 11)
x_sub2, y_sub2 = np.meshgrid(bes_test, verf_test, indexing='ij')
out_sub2_test = np.zeros_like(x_sub2)
# Auswerten
for m in range(0, len(bes_test)):
    sub_sys_2.input['Bestand des Materials'] = bes_test[m]
    for n in range(0, len(verf_test)):
        sub_sys_2.input['Verfügbarkeit des Materials'] = verf_test[n]
        sub_sys_2.compute()

        out_sub2_test[m, n] = sub_sys_2.output['Ausgang Subsys 2']
# Plotten
subplot = 322
ax2 = fig.add_subplot(subplot, projection='3d')
surf = ax2.plot_surface(x_sub2, y_sub2, out_sub2_test, rstride=1, cstride=1, cmap='viridis',
                        linewidth=0.4, antialiased=True)
plt.xlabel("Bestand")
plt.ylabel("Verfügbarkeit")
plt.title("Subsystem Material")

# Hauptsystem
mas_test = np.linspace(0, 1, 4)
# Wertebereich von Güte des Sprits:
sprit_test = np.linspace(out_sub1_test.min(), out_sub1_test.max(), 11)
rele_test = np.linspace(out_sub2_test.min(), out_sub2_test.max(), 11)
x, y = np.meshgrid(sprit_test, rele_test, indexing='ij')
# Speicher für Minimum und Maximum
out_min = 1
out_max = 0
# Auswertung
for i in range(0, len(mas_test)):
    out = np.zeros_like(x)
    guete.input['Masse'] = mas_test[i]

    for m in range(0, len(sprit_test)):
        guete.input['Güte vom Spritverbrauch'] = sprit_test[m]
        for n in range(0, len(rele_test)):
            guete.input['Relevanz des Materials'] = rele_test[n]
            guete.compute()

            out[m, n] = guete.output['Güte des Asteroids']

    # Maximum und Minimum bestimmen
    if out.min() < out_min:
        out_min = out.min()
    if out.max() > out_max:
        out_max = out.max()

    # Subplot generieren
    if i == 0:
        subplot = 323
        ax3 = fig.add_subplot(subplot, projection='3d') # subplot,
        surf = ax3.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
    elif i == 1:
        subplot = 324
        ax4 = fig.add_subplot(subplot, projection='3d')
        surf = ax4.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
    elif i == 2:
        subplot = 325
        ax5 = fig.add_subplot(subplot, projection='3d')
        surf = ax5.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
    elif i == 3:
        subplot = 326
        ax6 = fig.add_subplot(subplot, projection='3d')
        surf = ax6.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
    plt.xlabel("Bewertung Sprit")
    plt.ylabel("Materialrelevanz")
    mas_now = mas_test[i]
    plt.title(f'Masse = {mas_now:.2}')

# Einstellung Plot Darstellung
# Blickwinkel auf 3D-Plots
ax1.view_init(20, 120)
ax1.set_zlim(0, 1)
ax2.view_init(20, 70)
ax2.set_zlim(0, 1)
ax3.view_init(15, 190)
ax3.set_zlim(0, 1)
ax4.view_init(15, 190)
ax4.set_zlim(0, 1)
ax5.view_init(15, 190)
ax5.set_zlim(0, 1)
ax6.view_init(15, 190)
ax6.set_zlim(0, 1)

plt.subplots_adjust(left=0.065, bottom=0.065, right=0.935, top=0.885, wspace=0.3, hspace=0.5)
plt.show()
# Subsystem 1
print(f'Ausgabewerte des Sprit-Subsystems: {out_sub1_test.min():.2} '
      f'bis {out_sub1_test.max():.2}')
# Subsystem 2
print(f'Ausgabewerte des Material-Subsystems: {out_sub2_test.min():.2} '
      f'bis {out_sub2_test.max():.2}')
# Hauptsystem
print(f'Ausgabewerte des Hauptsystems: {out_min:.2} '
      f'bis {out_max:.2}')


# for x in range(0, 10):
#     a = round(random.random(), 2)
#     b = round(random.random(), 2)
#     c = round(random.uniform(lower, upper), 2)
#     d = round(random.random(), 2)
#     e = round(random.random(), 2)
#
#     sub_sys.input['Tank nach Wechsel'] = a
#     sub_sys.input['Spritverbrauch'] = b
#     sub_sys.compute()
#
#     sub_sys_2.input['Verfügbarkeit des Materials'] = c
#     sub_sys_2.input['Bestand des Materials'] = d
#     sub_sys_2.compute()
#
#     guete.input['Masse'] = e
#     guete.input['Güte vom Spritverbrauch'] = sub_sys.output['Ausgang Subsys']  # output vom anderem sys
#     guete.input['Relevanz des Materials'] = sub_sys_2.output['Ausgang Subsys 2']
#     guete.compute()
#
#     # Crunch the numbers
#     guete.compute()
#     print("Tank ", a, "Verbrauch ", b, "Sub1 ", round(sub_sys.output['Ausgang Subsys'], 2), "Verfügbarkeit ", c,
#           "Bestand ", d, "Sub2 ", round(sub_sys_2.output['Ausgang Subsys 2'], 2), "Masse ", e, "Güte/Note:",
#           round(guete.output['Güte des Asteroids'], 2))
# #     # out.view(sim=guete)
# #     plt.show()
