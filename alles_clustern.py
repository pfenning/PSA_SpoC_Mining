import numpy as np
import pykep as pk
from pykep import phasing
# from pykep import _dbscan
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

import SpoC_Constants as SpoC
from SpoC_Constants import data, dict_asteroids,T_START


alpha = 15


############################
# VORBEREITUNG DER DATEN   
############################
asteroids = [dict_asteroids[line][0] for line in dict_asteroids]


##########################################################################
# ITERATION VON CLUSTERN ALLER ASTEROIDEN FÜR VERSCHIEDENE STARTZEITEN
##########################################################################
# start_asts = [3622, 5384, 2257, 925]
# laenge_start_cl = []
# time_start = ["30190302T000000", "30190322T000000", "30190410T000000", "30190420T000000", "30190502T000000"]
# for time in time_start:
#     T_START = pk.epoch_from_iso_string(time)
#     knn = phasing.knn(asteroids, T_START, 'orbital', T=30)  # .mjd2000 + i
    
#     hilfe = []
#     for line in start_asts:
#         # ast_id = int(line[0])
#         _, neighb_idx, _ = knn.find_neighbours(line,query_type='ball', r=5000)
#         neighb_idx = list(neighb_idx)
#         hilfe.append(len(neighb_idx))
#         # if ast_id>=9999:print(ast_id)
#     laenge_start_cl.append(hilfe)

# laenge_start_cluster = np.transpose(laenge_start_cl)
# print(laenge_start_cluster)

# mittlere_laenge_cluster = [] # Durchschnitt je Asteroid
# for line in laenge_start_cluster:
#     mittlere_laenge_cluster.append(np.mean(line))


# top_ast = np.argpartition(mittlere_laenge_cluster, -alpha)[-alpha:]
# print(top_ast)




laenge_start_cl = []
knn = phasing.knn(asteroids, T_START, 'orbital', T=30)  # .mjd2000 + i
for line in data:
    ast_id = int(line[0])
    print(ast_id)
    if SpoC.get_asteroid_material(ast_id) != 1 and SpoC.get_asteroid_material(ast_id) != 3:
        _, neighb_idx, _ = knn.find_neighbours(ast_id,query_type='ball', r=5000)
        neighb_idx = list(neighb_idx)
        hilfe = []
        for mat in neighb_idx:
            if SpoC.get_asteroid_material(mat) == 1: hilfe.append(mat)
        laenge_start_cl.append(len(hilfe))     # [len(neighb_idx), ]
    else: laenge_start_cl.append(0)     # [len(neighb_idx), ]

    if ast_id >2:break

print(laenge_start_cl)
# top_starts = np.argpartition(laenge_start_cl, -alpha)[-alpha:]
# start_branches = []


#### WAS NOCH FEHLT: DIE 1ER ASTEROIDEN DÜRFEN NICHT ALS STARTASTEROIDEN GEWÄHLT WERDEN. NUR MAT 0 UND 2



# for line in laenge_start_cluster:
#     mittlere_laenge_cluster.append(np.mean(line))
# top_starts = np.argpartition(mittlere_laenge_cluster, -alpha)[-alpha:]


# for ID in top_starts:
#     start_branches.append(Seed(ID))






#####################################
# PLOT DER BESTEN STARTASTEROIDEN
#####################################
# x=[]
# y=[]
# z=[]
# for position in top_ast:
#     # if dict_asteroids[position][-1] == 1:
#     #     x.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[0])
#     #     y.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[1])
#     #     z.append(np.array(dict_asteroids[position][0].eph(T_START.mjd2000+60)[0])[2])
#     x.append(np.array(asteroids[position].eph(T_START.mjd2000)[0])[0])
#     y.append(np.array(asteroids[position].eph(T_START.mjd2000)[0])[1])
#     z.append(np.array(asteroids[position].eph(T_START.mjd2000)[0])[2])
# # Creating figure
# fig = plt.figure(figsize = (10, 7))
# ax = plt.axes(projection ="3d")
# # Creating plot
# ax.scatter3D(x, y, z, color = "red")
# plt.title("simple 3D scatter plot")
# # show plot
# plt.show()