import numpy as np

import PSA_functions_v3 as psa
from branch_class import Branch
import copy
import random

i_start = 3869 # 6 (0,0 aber 1!) # 2 (0,77) #8836 (0,43) # 3869 (0,0) # 9953 (0,0 ) #3622 (1,46)  # .. Für diesen Asteroiden super weg bisher gefunden! - Ursprünglich: 9953
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

x = SpoC.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
print(SpoC.udp.pretty(x))

from from_website.submisson_helper import create_submission
create_submission("spoc-mining","mine-the-belt",x,"TUDa_GoldRush_"+str(i_start)+"_submission_file.json","TUDa_GoldRush","submission_description")