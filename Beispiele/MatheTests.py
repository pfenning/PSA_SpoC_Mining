import numpy as np
import matplotlib.pyplot as plt

"""Billige Syntax Tests"""
# resF = np.array([[1,2, 3],[4, 5, 6]])
# weights = np.array([0.2, 0.4, 0.4])
#
# rank = sum(weights*resF[0])
#
# print(rank)

# A = [1, 2, 3]
# B = [4, 5, 6]
# results = []
# for i in range(0, len(A)):
#     results.append([A[i], B[i]])
#
# print(results)

"""Überlegungen zur Auswahl von t_flug aus t_flug_1"""
# results_t_flug = [[15, 800],       # mäßige Flugzeit, super Spritverbrauch
#                   [10, 1500],      # recht kurze Flugzeit, guter Spritverbrauch
#                   [45, 800],       # längere Flugzeit, super geringer Spritverbrauch
#                   [8, 2000],       # sehr kurze Flugzeit mäßiger Spritverbrauch
#                   [5, 5000]]       # kurze Flugzeit aber zu hoher Spritverbrauch
# # Normierung der Werte
# norm_t_flug = 30
# norm_dv = 2000
# for results in results_t_flug:
#     results[0] = results[0]/norm_t_flug
#     results[1] = results[1]/norm_dv
# print(results_t_flug)
#
# # Gewichtete Summe
# weights = np.array([0.3, 0.7])
# rank_t_flug = []
# for sol in results_t_flug:
#     rank_t_flug.append(sum(weights * sol))  # Bewertung aus gewichteter Summe
# print(rank_t_flug)

"""Überlegungen zur Auswahl von t_start aus t_start_var"""
t_opt = 20
# ToDo: Unterscheidung, ob gewartet, oder zu früh geflogen?? & t_var bei Wertepaaren noch definieren
#       Ansätze: separate Betrachten, t_var < 0, noch mehr?
#       Bisheriges Ergebnis: Bei negativen Werten immer zu gut bewertet
# Beispielfälle:
# 75% abgebaut, 90% abgebaut, optimal, +25 % Tage warten, +100 % Tage warten (-2 bis 2)
# super Spritverbrauch, mäßiger Spritverbrauch, schlechter Spritverbrauch (0 bis 2)
results_t_start = [[0, 800],    # 00:  0, 0
                   [5, 800],    # 01:  1, 0
                   [-2, 800],   # 02: -1, 0
                   [0, 2000],   # 03:  0, 1
                   [20, 800],   # 04:  2, 0
                   [5, 2000],   # 05:  1, 1
                   [-5, 800],   # 06: -2, 0
                   [-2, 2000],  # 07: -1, 1
                   [20, 2000],  # 08:  2, 1
                   [0, 3500],   # 09:  0, 2
                   [5, 3500],   # 10:  1, 2
                   [-2, 3500],  # 11: -1, 2
                   [-5, 2000],  # 12: -2, 1
                   [20, 3500],  # 13:  2, 2
                   [-5, 3500]]  # 14: -2, 2
# Normierung der Werte
# norm_t_start = t_opt
norm_dv = 2000
t_start_var = []
for results in results_t_start:
    t_start_var.append(results[0])
    results[0] = abs(results[0]/(t_opt/2))
    results[1] = results[1]/norm_dv
print(results_t_start)

# Gewichtete Summe
weights_neg_var = np.array([1.5, 0.7])
weights_pos_var = np.array([0.3, 0.7])
weights = weights_pos_var
rank_t_start = []
for i in range(0, len(results_t_start)):
    if t_start_var[i] < 0:
        weights = weights_neg_var
    else:
        weights = weights_pos_var

    rank_t_start.append(sum(weights * results_t_start[i]))  # Bewertung aus gewichteter Summe
print(rank_t_start)

plt.plot(rank_t_start)
plt.show()

