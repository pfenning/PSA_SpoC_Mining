import numpy as np
import pykep as pk
from pykep import phasing
# from pykep import _dbscan
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from SpoC_Constants import data, dict_asteroids


alpha = 15


############################
# VORBEREITUNG DER DATEN   
############################
asteroids = [dict_asteroids[line][0] for line in dict_asteroids]


##########################################################################
# ITERATION VON CLUSTERN ALLER ASTEROIDEN FÜR VERSCHIEDENE STARTZEITEN
##########################################################################
laenge_start_cl = []
time_start = ["30190302T000000", "30190322T000000", "30190410T000000", "30190420T000000", "30190502T000000"]
for time in time_start:
    T_START = pk.epoch_from_iso_string(time)
    knn = phasing.knn(asteroids, T_START, 'orbital', T=30)  # .mjd2000 + i
    
    hilfe = []
    for line in data:
        ast_id = int(line[0])
        _, neighb_idx, _ = knn.find_neighbours(ast_id,query_type='ball', r=5000)
        neighb_idx = list(neighb_idx)
        hilfe.append(len(neighb_idx))
        # if ast_id>=9999:print(ast_id)
    laenge_start_cl.append(hilfe)

laenge_start_cluster = np.transpose(laenge_start_cl)

mittlere_laenge_cluster = [] # Durchschnitt je Asteroid
for line in laenge_start_cluster:
    mittlere_laenge_cluster.append(np.mean(line))


top_ast = np.argpartition(mittlere_laenge_cluster, -alpha)[-alpha:]
print(top_ast)


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