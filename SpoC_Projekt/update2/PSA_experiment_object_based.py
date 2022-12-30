import numpy as np

import PSA_functions_v3 as psa
from branch_class import Branch
import copy
import random

i_start = 3622  # 3869, 8836,.. Für diesen Asteroiden super weg bisher gefunden! - Ursprünglich: 9953
# i_start = random.randrange(0, 10000, 1)
branch1 = Branch(i_start)
print(f"Startasteroid:{i_start}")

for i in range(50):
    try:
        possible_steps = branch1.get_next_possible_steps()
    except StopIteration:
        break
    if len(possible_steps) is 0:
        print("Es wurden keine weiteren möglichen Schritte gefunden")
        break
    # Neue Branch-Objekte, die erweitert werden mit den möglichen Schritten
    branch_expand = []
    for step in possible_steps:
        branch_expand.append(copy.deepcopy(branch1))
        branch_expand[-1].new_step(step['t_m'], step['step'], step['dv'])

    branch1 = branch_expand[np.argmax([branch.get_score() for branch in branch_expand])]
    branch1.print_last_step()

# Lösungvektoren erzeugen
branch1.print()
ERG_a, ERG_t_m, ERG_t_arr = branch1.get_result()

#################################################
# Lösungszeitplan erstellen
#################################################
from from_website import SpoC_Kontrolle as SpoC

x = ERG_t_arr[0:-2] + ERG_t_m + ERG_a[0:-2]
print(SpoC.udp.pretty(x))

