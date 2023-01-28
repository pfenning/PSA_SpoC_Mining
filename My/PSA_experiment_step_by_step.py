import numpy as np
import time

from SpoC_Constants import data
from expand_branch_class import beam_search, find_idx_start, Seed

from from_website import SpoC_Kontrolle
from from_website.submisson_helper import create_submission


##################### Hyperparameter für Ausführung #####################
score_method = ['step']    # branch, branch and guete, sonstwas=step
fast = True                # Ob möglichst schnell geflogen werden soll
knn_type = False            # Ob knn für das Clustern verwendet werden soll (sonst ball)
both = True                # Sowohl fast wie auch nicht fast wird ausgeführt



##################### Code Läuft #####################
# Sätzlinge finden :)
# branch_start = find_idx_start(data, method='examples')
branch_start = find_idx_start(data, method='alles_clustern')
# branch_start = find_idx_start(data, method='all', start=0) # Anhand von festen IDs
print("Sätzlinge gepflanzt :D")

# Zeitbegrenzung und beta festlegen
# beta_input = [400, 400, 300, 300, 200, 200, 100]
# beta_input = [100]
beta_input = [100, 90, 70, 50, 50]
# beta_input = [50, 30, 30, 20]
if isinstance(beta_input, int):
    beta_input = [beta_input]*50
elif len(beta_input) < 50:
    add = [beta_input[-1]]*(50-len(beta_input))
    beta_input = np.concatenate([beta_input, [beta_input[-1]]*(50-len(beta_input))])

# Zeitmessung starten
time_start = time.perf_counter()

# Beam-Search-Tree erstellen
beendete_Branches = []
final_guete = 0.0
asteroid_counter = 0
for branch_v in branch_start:
    # asteroid_counter += len(branch_v)
    time_part_start = time.perf_counter()
    if isinstance(branch_v, Seed):
        branch_v = [branch_v]
    # Beam-Search durchführen
    for beta in beta_input:
        v_done, top_beta = beam_search(branch_v, beta,
                                       analysis=score_method,
                                       fuzzy=True,
                                       fast=fast,
                                       knn_type=knn_type,
                                       both=both)
        if v_done:              # Fertige Lösungen gefunden
            beendete_Branches = np.concatenate((beendete_Branches, v_done), axis=0)
        branch_v = top_beta
        if len(top_beta) == 0:
            break
    # Zwischenzeit ausgeben:
    time_part_finish = time.perf_counter()
    print(f"Dauer der Suche eines Abschnitts:{time_part_finish - time_part_start:.0f}s")
    print(f"Betrachtet bis Asteroid{asteroid_counter}")
    # Bestes Zwischenergebnis speichern & Submission erstellen
    if 0 < len(beendete_Branches):
        best_branch_in_part = beendete_Branches[np.argmin([branch.get_guetemass() for branch in beendete_Branches])]
        if best_branch_in_part.get_guetemass() < final_guete:
            final_branch = best_branch_in_part
            final_guete = final_branch.get_guetemass()
            ERG_a, ERG_t_m, ERG_t_arr = final_branch.get_result()
            solution = np.concatenate([ERG_t_arr, ERG_t_m, ERG_a])
            # Solution.txt erstellen
            with open("Solution.txt", "w") as output:
                output.write("[")
                for ele in solution:
                    output.write(f"{ele}, ")
                output.write("]")
            # Submission-File
            x = SpoC_Kontrolle.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
            create_submission("spoc-mining", "mine-the-belt", x,
                              "TUDa_GoldRush_submission_file_" + str(final_branch.get_start_asteroid()) + ".json",
                              "TUDa_GoldRush", "submission_description")
            # ToDo Auskommentieren
            print("Aktueller Bestwert:")
            final_branch.print_summary()

if 0 == len(beendete_Branches):
    print("Es wurden keine möglichen Routen für die gegebenen Einstellungen gefunden")
# Zeitmessung
try:
    finish_time = time.perf_counter()
    print(f"Dauer der Suche:{finish_time - time_start}")
finally:
    pass

