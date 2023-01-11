import numpy as np

import PSA_functions_v3 as psa
import branch_class as bc
from branch_class import Branch
from datetime import datetime, timedelta

data = np.loadtxt("SpoC_Datensatz.txt")
T_DAUER = 1827

branch_v = bc.find_idx_start(data,0.001) # Vektor mit möglichen Startasteroiden
minutes = 1
beta = 4

print("branch_v done")

end_time = datetime.now() + timedelta(minutes=minutes)
print(datetime.now(), end_time)

beendete_Branches = []
while True:
    current_time = datetime.now()
    if current_time >= end_time:
        break

    v_done, top_beta = bc.beam_search(branch_v,beta)
    if v_done != []:
        beendete_Branches = np.concatenate((beendete_Branches, v_done), axis=0)
    if top_beta == []: break
    branch_v = top_beta

print(len(branch_v))
print("beendete_Branches: ", beendete_Branches , len(beendete_Branches))

if beendete_Branches == []:
    beendete_Branches = branch_v

print("beendete_Branches: ", beendete_Branches , len(beendete_Branches))

# Chosing the best path
branch = []
score = [0.0]
for final_branch in beendete_Branches:
    _score = float(final_branch.get_score())
    max_score = float(max(score))
    print("_score: ",_score, np.max(score))
    if branch == []: branch.append(final_branch), score.append(final_branch)
    elif _score >= max_score: 
        branch = [final_branch]
        score = [_score]



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

from from_website.submisson_helper import create_submission
create_submission("spoc-mining","mine-the-belt",x,"TUDa_GoldRush_submission_file_"+ minutes +"minutes_" +".json","TUDa_GoldRush","submission_description")