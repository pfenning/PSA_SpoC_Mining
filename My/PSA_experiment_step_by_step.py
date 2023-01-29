import numpy as np
import time

import pandas as pd
from multiprocessing import freeze_support

from SpoC_Constants import data
from expand_branch_class import find_idx_start

from funs_multiproc import mp_settings
from tree_search_func import tree_search

# Check, dass dieses Script nicht genutzt wird?
if __name__ == '__main__':
    # freeze_support()
    ##################### Hyperparameter für Ausführung #####################
    score_method = ['step']  # branch, branch and guete, sonstwas=step
    fast = False  # Ob möglichst schnell geflogen werden soll
    knn_type = True  # Ob knn für das Clustern verwendet werden soll (sonst ball)
    both = False  # Sowohl fast wie auch nicht fast wird ausgeführt

    ##################### Code Läuft #####################
    # Sätzlinge finden :)
    # branch_start_all = find_idx_start(data, method='examples')
    # branch_start_all = find_idx_start(data, method='alles_clustern', alpha=100)
    # branch_start_all = np.reshape(branch_start_all, (20, 5))
    branch_start_all = find_idx_start(data, method='all', start=0) # Anhand von festen IDs
    print("Sätzlinge gepflanzt :D")

    # Zeitbegrenzung und beta festlegen
    beta_input = [400, 400, 300, 300, 200, 200, 100]
    # beta_input = [100]
    # beta_input = [100, 90, 70, 50, 50]
    # beta_input = [50, 40, 40, 30, 30, 20]
    if isinstance(beta_input, int):
        beta_input = [beta_input] * 50
    elif len(beta_input) < 50:
        add = [beta_input[-1]] * (50 - len(beta_input))
        beta_input = np.concatenate([beta_input, [beta_input[-1]] * (50 - len(beta_input))])

    # Zeitmessung starten
    start_time = time.perf_counter()

    # Multiprocessing
    mp_settings(branch_start_all, tree_search, [beta_input, score_method, fast, knn_type])

    # if 0 == len(beendete_Branches):
    #     print("Es wurden keine möglichen Routen für die gegebenen Einstellungen gefunden")
    # Zeitmessung
    finish_time = time.perf_counter()
    print(f"Dauer der Suche:{finish_time - start_time}")

