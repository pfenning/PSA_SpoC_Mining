import numpy as np

import PSA_functions_v3 as psa
import branch_class as bc
from branch_class import Branch
import copy
import random

data = np.loadtxt("SpoC_Datensatz.txt")
T_DAUER = 1827

branch_v = bc.find_idx_start(data) # Vektor mit möglichen Startasteroiden
beta = 10

beendete_Branches = []
for i in range(100):

    v_done, top_beta = bc.beam_search(branch_v, 10)

    # for branch in top_beta:
    #     ERG_a, ERG_t_m, ERG_t_arr = branch.get_result()
    #     if (ERG_t_m, ERG_t_arr) >= T_DAUER:
    #         v_done.append(branch)
    #         top_beta.pop(branch)

    if v_done != []:
        beendete_Branches.append(v_done)
    if top_beta == []: break

    branch_v = top_beta

# Chosing the best path
branch = []
score = []
guete = []
for _branch in beendete_Branches:
    _score = _branch.get_score()
    _guete = _branch.get_guetemass()
    if _score >= np.max(score) and _guete >= np.max(guete): branch = [_branch], core = [_score], guete = [_guete]



# Lösungvektoren erzeugen
branch1 = branch[0]
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