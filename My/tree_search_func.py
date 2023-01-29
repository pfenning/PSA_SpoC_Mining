import numpy as np
import time

from SpoC_Constants import data
from expand_branch_class import beam_search, Seed

from from_website import SpoC_Kontrolle
from from_website.submisson_helper import create_submission

def tree_search(branch_start, settings, lck, final_guete):
    beta_input, score_method, fast, knn_type = settings
    # Beam-Search-Tree erstellen
    beendete_Branches = []
    # final_guete = 0.0
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
                                           knn_type=knn_type)
            if v_done:  # Fertige Lösungen gefunden
                beendete_Branches = np.concatenate((beendete_Branches, v_done), axis=0)
            branch_v = top_beta
            if len(top_beta) == 0:
                break
        # Zwischenzeit ausgeben:
        time_part_finish = time.perf_counter()
        with lck:
            print(f"Dauer der Suche eines Abschnitts:{time_part_finish - time_part_start:.0f}s")
            print(f"Betrachtet bis Asteroid{asteroid_counter}")
        # Bestes Zwischenergebnis speichern & Submission erstellen
        if 0 < len(beendete_Branches):
            best_branch_in_part = beendete_Branches[np.argmin([branch.get_guetemass() for branch in beendete_Branches])]
            if best_branch_in_part.get_guetemass() < final_guete.value:
                final_guete.value = best_branch_in_part.get_guetemass()
                ERG_a, ERG_t_m, ERG_t_arr = best_branch_in_part.get_result()
                print(ERG_t_arr + ERG_t_m + ERG_a)
                # Submission-File
                x = SpoC_Kontrolle.convert_to_chromosome(ERG_t_arr + ERG_t_m + ERG_a)
                create_submission("spoc-mining", "mine-the-belt", x,
                                  "TUDa_GoldRush_submission_file_" + str(
                                      best_branch_in_part.get_start_asteroid()) + ".json",
                                  "TUDa_GoldRush", "submission_description")
                # ToDo Auskommentieren
                with lck:
                    print("Aktueller Bestwert:")
                    best_branch_in_part.print_summary()
# return beendete_Branches > 0
