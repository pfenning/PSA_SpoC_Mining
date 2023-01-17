import numpy as np
from datetime import datetime, timedelta

from SpoC_Constants import T_DAUER, data
from expand_branch_class import beam_search, find_idx_start

from from_website import SpoC_Kontrolle
from from_website.submisson_helper import create_submission


# Sätzlinge finden :)
# branch_start = find_idx_start(data, method='examples') # Anhand von festen IDs
# branch_start = find_idx_start(data,0.001) # Anhand von anderen Methoden
branch_start = find_idx_start(data, method='random',k=30) # Anhand von festen IDs
# branch_start = find_idx_start(data, method='test') # Anhand von festen IDs

print("Sätzlinge gepflanzt :D")

# Zeitbegrenzung und beta festlegen
beta = 80
minutes = 20
start_time = datetime.now()
end_time = datetime.now() + timedelta(minutes=minutes)
print(datetime.now(), end_time)

# Beam-Search-Tree erstellen
method = ['branch']
beendete_Branches = []
for branch_v in branch_start:
    branch_v = [branch_v]
    while datetime.now() < end_time:
        v_done, top_beta = beam_search(branch_v, beta, analysis=method, fuzzy=True)    # analysis='branch'
        if v_done:              # Fertige Lösungen gefunden
            beendete_Branches = np.concatenate((beendete_Branches, v_done), axis=0)
        branch_v = top_beta
        if len(top_beta) == 0:
            break


# Beste beendete Pfade ausgeben
if len(beendete_Branches) == 0:   # Keine fertigen Lösungen gefunden
    beendete_Branches = branch_v
    print("Keine fertigen Branches gefunden")
print("============ beendete Branches: ============")
for branch in beendete_Branches:
    branch.print_summary()

# Chosing the best path
final_branch = beendete_Branches[np.argmin([branch.get_guetemass() for branch in beendete_Branches])]

# Zeitmessung
finish_time = datetime.now()
print(f"Dauer der Suche:{finish_time-start_time}")

# Lösungvektoren erzeugen
final_branch.print()
ERG_a, ERG_t_m, ERG_t_arr = final_branch.get_result()


#################################################
# Lösungszeitplan erstellen
#################################################

x = SpoC_Kontrolle.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
print(SpoC_Kontrolle.udp.pretty(x))

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
#     x = SpoC.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
#     print(SpoC.udp.pretty(x))
#
#     create_submission("spoc-mining","mine-the-belt",x,"TUDa_GoldRush_submission_file_"+ str(minutes) +"minutes_" + str(i) +".json","TUDa_GoldRush","submission_description")
#     i += 1