import numpy as np
import time

from SpoC_Constants import data
from expand_branch_class import beam_search, Seed

def tree_search(branch_start, settings, final_guete):
    beta_input, score_method, fast, knn_type = settings
    # Beam-Search-Tree erstellen
    beendete_Branches = []
    if isinstance(branch_start, Seed):
        branch_v = [branch_start]

    for branch_v in branch_start:
        if isinstance(branch_v, Seed):
            branch_v = [branch_v]
        # Beam-Search durchführen
        for beta in beta_input:
            v_done, top_beta = beam_search(branch_v, beta, analysis=score_method, fuzzy=True, fast=fast,
                                           knn_type=knn_type)
            if 0 < len(v_done):  # Fertige Lösungen gefunden
                beendete_Branches = np.concatenate((beendete_Branches, v_done), axis=0)
            branch_v = top_beta
            if len(top_beta) == 0:
                break
        # Bestes Zwischenergebnis speichern & Submission erstellen
        if 0 < len(beendete_Branches):
            best_branch_in_part = beendete_Branches[np.argmin([branch.get_guetemass() for branch in beendete_Branches])]
            with final_guete.get_lock():
                if best_branch_in_part.get_guetemass() < final_guete.value:
                    final_branch = best_branch_in_part
                    final_guete.value = final_branch.get_guetemass()
                    ERG_a, ERG_t_m, ERG_t_arr = final_branch.get_result()
                    print(f"{ERG_t_arr + ERG_t_m + ERG_a}")
                    # print("Aktueller Bestwert:")
                    # final_branch.print_summary()