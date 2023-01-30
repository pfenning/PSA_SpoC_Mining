import numpy as np

from SpoC_Constants import data
from expand_branch_class import find_idx_start

from funs_multiproc import mp_settings
from tree_search_func import tree_search

if __name__ == '__main__':
    ##################### Hyperparameter für Ausführung #####################
    score_method = ['step']   # branch, branch and guete, sonstwas=step
    fast = False                # Ob möglichst schnell geflogen werden soll
    knn_type = False            # Ob knn für das Cluster verwendet werden soll (sonst ball)



    ##################### Code Läuft #####################
    # Sätzlinge finden :)
    # branch_start = find_idx_start(data, method='alles_clustern')
    branch_start = find_idx_start(data, method='random', k=50)
    branch_start = np.reshape(branch_start, (5,10))

    # Zeitbegrenzung und beta festlegen
    # beta_input = [400, 400, 300, 300, 200, 200, 100]
    # beta_input = [100]
    # beta_input = [100, 90, 70, 50, 50]
    beta_input = [50, 40, 40, 30, 30, 20]
    if isinstance(beta_input, int):
        beta_input = [beta_input]*50
    elif len(beta_input) < 50:
        add = [beta_input[-1]]*(50-len(beta_input))
        beta_input = np.concatenate([beta_input, [beta_input[-1]]*(50-len(beta_input))])

    # Multiprocessing
    mp_settings(branch_start, tree_search, [beta_input, score_method, fast, knn_type])


    # if 0 == len(beendete_Branches):
    #     print("Es wurden keine möglichen Routen für die gegebenen Einstellungen gefunden")

