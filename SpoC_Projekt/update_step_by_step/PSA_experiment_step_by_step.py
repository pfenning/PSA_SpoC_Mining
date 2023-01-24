import time

import numpy as np
from datetime import datetime, timedelta

from SpoC_Constants import T_DAUER, data
from expand_branch_class import beam_search, find_idx_start, Seed

from from_website import SpoC_Kontrolle
from from_website.submisson_helper import create_submission


##################### Hyperparameter für Ausführung #####################
score_method = ['branch']   # branch and guete, sonstwas=step
fast = False                # Ob möglichst schnell geflogen werden soll
knn_type = False            # Ob knn für das Clustern verwendet werden soll (sonst ball)



##################### Code Läuft #####################
# Sätzlinge finden :)
# branch_start = find_idx_start(data, method='examples') # Anhand von festen IDs
# branch_start = find_idx_start(data,0.001) # Anhand von anderen Methoden
# branch_start = find_idx_start(data, method='random',k=50) # Anhand von festen IDs
# branch_start = np.reshape(branch_start, (10,5)) # ToDo: Testen
# branch_start = find_idx_start(data, method='test') # Anhand von festen IDs
branch_start = find_idx_start(data, method='all') # Anhand von festen IDs
# branch_start = find_idx_start(data, method='alles_clustern')
# branch_start = np.reshape(branch_start, (5,10)) # ToDo: Testen
print("Sätzlinge gepflanzt :D")

# Zeitbegrenzung und beta festlegen
beta_input = [400, 400, 300, 300, 200, 200, 100]
# beta_input = [100]
# beta_input = [100, 90, 70, 50, 50]
# beta_input = [50, 30, 30, 20]
if isinstance(beta_input, int):
    beta_input = [beta_input]*50
elif len(beta_input) < 50:
    add = [beta_input[-1]]*(50-len(beta_input))
    beta_input = np.concatenate([beta_input, [beta_input[-1]]*(50-len(beta_input))])

# Zeitmessung
time_start = time.perf_counter_ns()

# Beam-Search-Tree erstellen
beendete_Branches = []
final_guete = 0.0
for branch_v in branch_start:
    time_part_start = time.perf_counter()
    if isinstance(branch_v, Seed):
        branch_v = [branch_v]
    # Beam-Search durchführen
    for beta in beta_input:
        v_done, top_beta = beam_search(branch_v, beta, analysis=score_method, fuzzy=True, fast=fast, knn_type=knn_type)
        if v_done:              # Fertige Lösungen gefunden
            beendete_Branches = np.concatenate((beendete_Branches, v_done), axis=0)
        branch_v = top_beta
        if len(top_beta) == 0:
            break
    # Zwischenzeit ausgeben:
    time_part_finish = time.perf_counter()
    try:
        finish_time = datetime.now()
        print(f"Dauer der Suche eines Abschnitts:{time_part_finish - time_part_start:.0f}s")
    except NameError:
        print("Zeitmessung konnte nicht durchgeführt werden")
    # Bestes Zwischenergebnis speichern
    best_branch_in_part = beendete_Branches[np.argmin([branch.get_guetemass() for branch in beendete_Branches])]
    if best_branch_in_part.get_guetemass() < final_guete:
        final_branch = best_branch_in_part
        final_guete = final_branch.get_guetemass()
        print("Aktueller Bestwert:")
        final_branch.print_summary()
        # Lösung speichern
        ERG_a, ERG_t_m, ERG_t_arr = final_branch.get_result()
        x = SpoC_Kontrolle.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
        create_submission("spoc-mining", "mine-the-belt", x,
                          "TUDa_GoldRush_submission_file_" + str(final_branch.get_start_asteroid()) + ".json",
                          "TUDa_GoldRush", "submission_description")

# Beste beendete Pfade ausgeben
# print("============ beendete Branches: ============")
# for branch in beendete_Branches:
#     branch.print_summary()

# Chosing the best path
final_branch = beendete_Branches[np.argmin([branch.get_guetemass() for branch in beendete_Branches])]

# Zeitmessung
try:
    finish_time = time.perf_counter()
    print(f"Dauer der Suche:{finish_time - time_start}")
except NameError:
    print("Zeitmessung konnte nicht durchgeführt werden")


# Lösungvektoren erzeugen
final_branch.print()
ERG_a, ERG_t_m, ERG_t_arr = final_branch.get_result()
# np.save("final_branch_a_tm_tarr", [ERG_a, ERG_t_m, ERG_t_arr])


#################################################
# Lösungszeitplan erstellen
#################################################

x = SpoC_Kontrolle.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
print(SpoC_Kontrolle.udp.pretty(x))

create_submission("spoc-mining","mine-the-belt",x,"TUDa_GoldRush_submission_file_" + "TEST" +".json","TUDa_GoldRush","submission_description")

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