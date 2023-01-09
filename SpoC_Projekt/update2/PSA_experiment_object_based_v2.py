import numpy as np

import PSA_functions_v4 as psa
from branch_class import Branch
import copy
import random

i_start = 3622 # 6 (0,0 aber 1!) # 2 (0,77) #8836 (0,43) # 3869 (0,0) # 9953 (0,0 ) #3622 (1,46)  # .. Für diesen Asteroiden super weg bisher gefunden! - Ursprünglich: 9953
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


    branch1, branch1_score, branch2, branch2_score, branch1_before, branch1_before_score = psa.beam_search_vector(branch1)

    if branch1_before_score >= branch2_score: # das stimmt noch nicht ganz...hier muss quasi rückwirkend ein Wert gespeichert werden!
        branch1 = branch1_before
    else: branch1 = branch2

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