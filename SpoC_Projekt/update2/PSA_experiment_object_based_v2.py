import numpy as np

import PSA_functions_v3 as psa
import branch_class as bc
from branch_class import Branch
from datetime import datetime, timedelta

data = np.loadtxt("SpoC_Datensatz.txt")
T_DAUER = 1827

branch_v = bc.find_idx_start(data) # Vektor mit möglichen Startasteroiden
beta = 1

print("branch_v done")

end_time = datetime.now() + timedelta(minutes=3)
print(datetime.now(), end_time)

beendete_Branches = []
while True:
    current_time = datetime.now()
    if current_time == end_time:
        break
    for i in range(500):

        v_done, top_beta = bc.beam_search(branch_v,beta)
    
        # for branch in top_beta:
        #     ERG_a, ERG_t_m, ERG_t_arr = branch.get_result()
        #     if (ERG_t_m, ERG_t_arr) >= T_DAUER:
        #         v_done.append(branch)
        #         top_beta.pop(branch)

        if v_done != []:
            beendete_Branches = np.concatenate((beendete_Branches, v_done), axis=0)
        if top_beta == []: break

        branch_v = top_beta
        print(branch_v)

print(beendete_Branches)

# Chosing the best path
branch = []
score = []
guete = []
for final_branch in beendete_Branches:
    _score = final_branch.get_score()
    _guete = final_branch.get_guetemass()
    if branch == [] and score == [] and guete == []: branch.append(final_branch), score.append(final_branch), guete.append(final_branch)
    elif _score >= np.max(score) and _guete >= np.max(guete): branch = [final_branch], score = [_score], guete = [_guete]



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