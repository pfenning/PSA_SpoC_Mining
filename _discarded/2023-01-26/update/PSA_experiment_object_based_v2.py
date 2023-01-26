import numpy as np

import PSA_functions_v4 as psa
import branch_class as bc
from branch_class import Branch
from datetime import datetime, timedelta

from from_website import SpoC_Kontrolle as SpoC
from from_website.submisson_helper import create_submission


data = np.loadtxt("Asteroidengürtel.txt")

T_DAUER = 1827
minutes = 15
beta = 20
branch_v = bc.find_idx_start(data, method='examples')

# # branch_v = bc.find_idx_start(data,0.001) # Vektor mit möglichen Startasteroiden
# starting_branch = np.argpartition(starting_score, -4)[-4:]
# branch_v = []
# for line in starting_branch:
#     branch_v.append(starting_branches[line])

print("branch_v done")

end_time = datetime.now() + timedelta(minutes=minutes)
print(datetime.now(), end_time)

beendete_Branches = []
while datetime.now() < end_time:
    v_done, top_beta = bc.beam_search(branch_v,beta)    # analysis='branch'
    if v_done:              # Fertige Lösungen gefunden
        beendete_Branches = np.concatenate((beendete_Branches, v_done), axis=0)
    if len(top_beta) == 0:  # Keine weiterzuführenden Lösungen gefunden
        break
    branch_v = top_beta

# print(len(branch_v))
# print("beendete_Branches: ", beendete_Branches , len(beendete_Branches))

if len(beendete_Branches) == 0:   # Keine fertigen Lösungen gefunden
    beendete_Branches = branch_v
    print("Keine fertigen Branches gefunden")
print("beendete Branches:")
for branch in beendete_Branches:
    branch.print_summary()
# print("beendete_Branches: ", beendete_Branches , len(beendete_Branches))

# Chosing the best path
final_branch = beendete_Branches[np.argmin([branch.get_guetemass() for branch in beendete_Branches])]

# Lösungvektoren erzeugen
final_branch.print()
ERG_a, ERG_t_m, ERG_t_arr = final_branch.get_result()


#################################################
# Lösungszeitplan erstellen
#################################################
from from_website import SpoC_Kontrolle as SpoC

x = SpoC.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
print(SpoC.udp.pretty(x))

from from_website.submisson_helper import create_submission
create_submission("spoc-mining","mine-the-belt",x,"TUDa_GoldRush_submission_file_"+ str(minutes) +"minutes_" +".json","TUDa_GoldRush","submission_description")

# from from_website import SpoC_Kontrolle as SpoC
# from from_website.submisson_helper import create_submission
# i = 1
# score = []
# for final_branch in beendete_Branches:
#     score.append(final_branch.get_branch_score())
#
# if len(score) > 10:
#     best_branch = np.argpartition(score, -10)[-10:] # Vektor mit den 10 besten Asteroiden
# else:
#     best_branch = range(len(beendete_Branches))
#
# for solution in best_branch:
#     branch = beendete_Branches[solution]
#     # branch.print()
#     ERG_a, ERG_t_m, ERG_t_arr = branch.get_result()
#
#     t_flug = SpoC.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
#     print(SpoC.udp.pretty(t_flug))
#
#     create_submission("spoc-mining","mine-the-belt",t_flug,"TUDa_GoldRush_submission_file_"+ str(minutes) +"minutes_" + str(i) +".json","TUDa_GoldRush","submission_description")
#     i += 1