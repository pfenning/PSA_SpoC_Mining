import numpy as np
import time


from SpoC_Constants import data
from expand_branch_class import find_idx_start

from funs_multiproc import mp_settings
from tree_search_func import tree_search

# Check, dass dieses Script nicht genutzt wird?
if __name__ == '__main__':
    # freeze_support()
    ##################### Hyperparameter für Ausführung #####################
    score_method = ['branch']  # branch, branch and guete, sonstwas=step
    fast = False  # Ob möglichst schnell geflogen werden soll
    knn_type = True  # Ob knn für das Clustern verwendet werden soll (sonst ball)

    ##################### Code Läuft #####################
    # Sätzlinge finden :)
    # branch_start_all = find_idx_start(data, method='examples')
    branch_start_all = find_idx_start(data, method='alles_clustern', alpha=300)
    # branch_start_all = np.reshape(branch_start_all, (5, 10))    # ToDo Zurück ändern
    # branch_start_all = find_idx_start(data, method='all', start=0) # Anhand von festen IDs
    # branch_start_all = find_idx_start(data, method='all', start=0)  # Anhand von festen IDs
    # branch_start_all = np.reshape(branch_start_all, (20, 500))    # ToDo Testen
    branch_start_all = np.reshape(branch_start_all, (15, 20))
    print("Sätzlinge gepflanzt :D")

    # Zeitbegrenzung und beta festlegen
    # beta_input = [400, 400, 300, 300, 200, 200, 100, 80, 70]
    # beta_input = [50, 50,  15, 300, 300, 300, 200, 200, 100, 80, 70, 50, 30] # ToDo Testen
    # beta_input = [3000, 2500, 2500, 2000, 1500, 1500, 1000, 1000, 900, 700, 600, 500, 400, 300, 250, 150, 100]
    # beta_input = [100]
    # beta_input = [100, 90, 70, 50, 50]
    # beta_input = [35, 30, 30, 25, 25, 20]
    # beta_input = [50, 40, 40, 30, 30, 20]
    beta_input = [15, 25 , 30, 40, 40, 30, 30, 20, 10]
    # beta_input = [70, 60, 60, 50, 50, 40, 40, 40]
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
    print(f"Verwendeter beta-Vektor: {beta_input}")
    print(f"Anzahl Startasteroiden: {branch_start_all.size}")
    print(f"Abgearbeitet in {branch_start_all.shape[0]} Gruppen mit je {branch_start_all.shape[1]} Startpunkten")
    print(f"Dauer der Suche:{finish_time - start_time}s")

