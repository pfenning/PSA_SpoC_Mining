#ToDo - muss noch outfkt finetunen/besprechen
#     - sprit ist wichtig





import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import random
from skfuzzy import control as ctrl

# Normierte Werte
# Abweichung, Bestand, Tank nach, Tank jetzt, Delta v, Masse
#inputs
#erst abw,t_j,t_n, delt weglassen --> abw unnötig wenn wir schon bestand so berrechnen!!

#abw = ctrl.Antecedent(np.arange(0, 1, 0.01), 'Abweichung')
bes = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Bestand')
#t_n = ctrl.Antecedent(np.arange(0, 1, 0.01), 'Tank nach Wechsel')
#t_j = ctrl.Antecedent(np.arange(0, 1, 0.01), 'Tank vor Wechsel')
delt = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Spritverbrauch')
mas = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'Masse')
#output
out = ctrl.Consequent(np.arange(0, 1, 0.01), 'Güte des Asteroids')

# Generate fuzzy membership functions
#abw['lo'] = fuzz.trimf(abw.universe, [0, 0, 1])
#abw['hi'] = fuzz.trimf(abw.universe, [0, 1, 1])
bes['lo'] = fuzz.trimf(bes.universe, [0, 0, 0.33])
bes['md'] = fuzz.trimf(bes.universe, [0, 0.33, 0.66])
bes['hi'] = fuzz.trapmf(bes.universe, [0.33, 0.66, 1, 1])
#t_n.automf(3)
#t_j.automf(3)
#delt.automf(3)
delt['lo'] = fuzz.trapmf(delt.universe, [0, 0, 0.15, 0.85])
delt['hi'] = fuzz.trapmf(delt.universe, [0.15, 0.85, 1, 1])
mas.automf(3)
out.automf(7)

# Visualize these membership functions
# abw.view()
#bes.view()
# t_n.view()
# t_j.view()
#delt.view()
# mas.view()
#out.view()
#plt.show()

#Rule base
# dismal, poor, mediocre, average, decent, good, excellent
#ToDo muss noch outfut finetunen/besprechen
rule1 =  ctrl.Rule(bes['lo'] & mas['poor']    & delt['lo'], out['average'])
rule2 =  ctrl.Rule(bes['lo'] & mas['poor']    & delt['hi'], out['mediocre'])
rule3 =  ctrl.Rule(bes['lo'] & mas['average'] & delt['lo'], out['good'])
rule4 =  ctrl.Rule(bes['lo'] & mas['average'] & delt['hi'], out['average'])
rule5 =  ctrl.Rule(bes['lo'] & mas['good']    & delt['lo'], out['excellent'])
rule6 =  ctrl.Rule(bes['lo'] & mas['good']    & delt['hi'], out['decent'])

rule7 =  ctrl.Rule(bes['md'] & mas['poor']    & delt['lo'], out['mediocre'])
rule8 =  ctrl.Rule(bes['md'] & mas['poor']    & delt['hi'], out['poor'])
rule9 =  ctrl.Rule(bes['md'] & mas['average'] & delt['lo'], out['decent'])
rule10 = ctrl.Rule(bes['md'] & mas['average'] & delt['hi'], out['mediocre'])
rule11 = ctrl.Rule(bes['md'] & mas['good']    & delt['lo'], out['good'])
rule12 = ctrl.Rule(bes['md'] & mas['good']    & delt['hi'], out['average'])

rule13 = ctrl.Rule(bes['hi'] & mas['poor']    & delt['lo'], out['dismal'])
rule14 = ctrl.Rule(bes['hi'] & mas['poor']    & delt['hi'], out['dismal'])
rule15 = ctrl.Rule(bes['hi'] & mas['average'] & delt['lo'], out['poor'])
rule16 = ctrl.Rule(bes['hi'] & mas['average'] & delt['hi'], out['dismal'])
rule17 = ctrl.Rule(bes['hi'] & mas['good']    & delt['lo'], out['mediocre'])
rule18 = ctrl.Rule(bes['hi'] & mas['good']    & delt['hi'], out['poor'])

space_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,rule13,rule14,rule15,rule16,rule17,rule18])

güte = ctrl.ControlSystemSimulation(space_ctrl)

#Test
for x in range (0,10):
    a = round(random.random(),2)
    b = round(random.random(),2)
    c = round(random.random(),2)

    # a = 0.5
    # b = 0.5
    # c = 0.5

    güte.input['Bestand'] = a
    güte.input['Masse'] = b
    güte.input['Spritverbrauch'] = c

    #Crunch the numbers
    güte.compute()
    print("Der Bestand ",a , "Mit Masse ",b ,"Mit ein Spritverbrauch ",c, "Führt zu einer Güte von:" , round(güte.output['Güte des Asteroids'],2))
    # out.view(sim=güte)
    plt.show()