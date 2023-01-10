import numpy as np

import PSA_functions_v3 as psa
import branch_class as bc
from branch_class import Branch
import copy
import random

data = np.loadtxt("SpoC_Datensatz.txt")

possible_starts = bc.find_idx_start(data) # Vektor mit möglichen Startasteroiden

possible_i_start = []
start_branch_v = []
for idx_start in possible_starts:
    branch1 = Branch(idx_start)
    try:
        possible_steps = branch1.get_next_possible_steps()
    except StopIteration:
        break
    if len(possible_steps) is 0:
        break
    # Neue Branch-Objekte, die erweitert werden mit den möglichen Schritten
    branch_expand = []
    score = []
    for step in possible_steps:
        branch_expand.append(copy.deepcopy(branch1))
        branch_expand[-1].new_step(step['t_m'], step['step'], step['dv'])
        score.append(branch_expand[-1].get_score())

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

# from from_website.submisson_helper import create_submission
# create_submission("spoc-mining","mine-the-belt",x,"TUDa_GoldRush_"+str(i_start)+"_submission_file.json","TUDa_GoldRush","submission_description")