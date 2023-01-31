# Packages laden
import numpy as np
import matplotlib.pyplot as plt

# Importieren von Mathekonstanten
from math import pi

# Konstanten und Database Laden
from SpoC_Constants import data, dict_asteroids, MU_TRAPPIST

plt.rcParams.update({
    "text.usetex": True,
    "font.family" : "serif",
    "font.serif"  : "roman"})

def fig_settings(num):
    scale = 0.6
    return plt.figure(num, (scale*width,3/4*scale*width), dpi=900)

def plot_setting(xlabel, ylabel, ax):
    plt.subplots_adjust(bottom=0.17, left=0.12, right=0.98, top=0.92)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.ticklabel_format(axis='y', scilimits=(0, 0))
    ax.set_xlabel(xlabel, fontsize=14)  # , loc="right"
    ax.set_ylabel(ylabel, fontsize=14)  # , loc="top"

# Maße von DinA4 in inches
width = 8.27
height = 11.69

asteroids, asteroid_masses, asteroid_materials = np.transpose([[ast, mas, mat] for ast, mas, mat in dict_asteroids.values()])


unique_2, counts_2 = np.unique(asteroid_materials, return_counts=True)
fig = fig_settings(1)
plt.bar(unique_2, counts_2, color ='#009D7E',width = 0.5)
#plt.plot(unique, counts)
x = [0,1,2,3]
labels = [0,1,2,3]
plt.xticks(x, labels)
plot_setting(r'Material Typ', r'Anzahl Asteroiden', plt.gca())
plt.savefig('Verteilung_Materialien.eps',format='eps')
plt.show()

mass_mat_0 = asteroid_masses[asteroid_materials == 0]
mass_mat_1 = asteroid_masses[asteroid_materials == 1]
mass_mat_2 = asteroid_masses[asteroid_materials == 2]
mass_mat_3 = asteroid_masses[asteroid_materials == 3]



fig2 = fig_settings(2)
asteroid_masses_rounded = np.round_(data[:, -2], decimals = 1)
mass_mat_0_round = asteroid_masses_rounded[asteroid_materials == 0]
mass_mat_1_round = asteroid_masses_rounded[asteroid_materials == 1]
mass_mat_2_round = asteroid_masses_rounded[asteroid_materials == 2]
mass_mat_3_round = asteroid_masses_rounded[asteroid_materials == 3]
unique0, counts0 = np.unique(mass_mat_0_round, return_counts=True)
unique1, counts1 = np.unique(mass_mat_1_round, return_counts=True)
unique2, counts2 = np.unique(mass_mat_2_round, return_counts=True)
unique3, counts3 = np.unique(mass_mat_3_round, return_counts=True)
mat0 = plt.bar(unique0-0.02, counts0, color ='lightskyblue',width = 0.02 )
mat1 = plt.bar(unique1, counts1, color ='dimgrey',width = 0.02)
mat2 = plt.bar(unique2+0.02, counts2, color ='mediumseagreen',width = 0.02)
mat3 = plt.bar(unique3+0.04, counts3, color ='lightsalmon',width = 0.02)
x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
labels = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
plt.xticks(x, labels)
plt.legend((mat0, mat1, mat2, mat3),
           ('Mat. 0', 'Mat. 1', 'Mat. 2', 'Mat. 3'),
           scatterpoints=1,
           loc='upper right',
           ncol=4,
           fontsize=12,
           handlelength=1.0,
           columnspacing=1.0,
           bbox_to_anchor=(1.0, 1.13),
           borderpad=0.2)
# plt.xlabel("Masse")
# plt.ylabel("Vorkommen")
plot_setting(r'Masse', r'Vorkommen', plt.gca())
plt.subplots_adjust(top=0.9)
plt.savefig('Vorkommen_Rohstoffe.eps',format='eps')
plt.show()





