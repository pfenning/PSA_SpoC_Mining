import numpy as np

from SpoC_Constants import data
from expand_branch_class import beam_search, find_idx_start, Seed


##################### Hyperparameter für Ausführung #####################
score_method = ['step']   # branch, branch and guete, sonstwas=step
fast = False                # Ob möglichst schnell geflogen werden soll
knn_type = False            # Ob knn für das Clustern verwendet werden soll (sonst ball)



##################### Code Läuft #####################
# Sätzlinge finden :)
branch_start = find_idx_start(data, method='alles_clustern')
branch_start = np.reshape(branch_start, (5,10))

# Zeitbegrenzung und beta festlegen ToDo: Auskommentieren
# beta_input = [400, 400, 300, 300, 200, 200, 100]
# beta_input = [100]
# beta_input = [100, 90, 70, 50, 50]
beta_input = [50, 30, 30, 20]
if isinstance(beta_input, int):
    beta_input = [beta_input]*50
elif len(beta_input) < 50:
    add = [beta_input[-1]]*(50-len(beta_input))
    beta_input = np.concatenate([beta_input, [beta_input[-1]]*(50-len(beta_input))])

# Beam-Search-Tree erstellen
beendete_Branches = []
final_guete = 0.0
for branch_v in branch_start:
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
    # Bestes Zwischenergebnis speichern & Submission erstellen
    if 0 < len(beendete_Branches):
        best_branch_in_part = beendete_Branches[np.argmin([branch.get_guetemass() for branch in beendete_Branches])]
        if best_branch_in_part.get_guetemass() < final_guete:
            final_branch = best_branch_in_part
            final_guete = final_branch.get_guetemass()
            ERG_a, ERG_t_m, ERG_t_arr = final_branch.get_result()
            solution = np.concatenate([ERG_t_arr, ERG_t_m, ERG_a])
            # Ausgabestring erstellen
            print_solution = "["
            for ele in solution:
                print_solution += f"{ele}, "
            print_solution += "]"
            print(print_solution)
            # ToDo Auskommentieren
            print("Aktueller Bestwert:")
            final_branch.print_summary()

if 0 == len(beendete_Branches):
    print("Es wurden keine möglichen Routen für die gegebenen Einstellungen gefunden")

