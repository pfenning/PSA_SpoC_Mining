
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter import *

import numpy as np
from TripInSpace import TripInSpace

########### Trip initialisieren ############
t_arr_test = np.array([0.0,
                  20.0,
                  46.83879022985213,
                  88.97969529198664,
                  135.96216293541772,
                  183.36653604474407,
                  222.05218625679345,
                  262.0417348142814,
                  319.2459196093006,
                  375.1631426027095,
                  411.6589977831119,
                  457.71575317095886,
                  503.7349322072007,
                  550.4107526093931,
                  602.1719144645192,
                  642.898416252558,
                  682.5402316054478,
                  736.3735100926535,
                  794.2870672119819,
                  829.4727001158566,
                  867.2736257453322,
                  906.2610971023935,
                  949.1593914279853,
                  995.7466989057391,
                  1034.5112702151794,
                  1082.3776115899673,
                  1120.7888066945977,
                  1166.2079509635387,
                  1202.2134728516376,
                  1246.9106749139876,
                  1281.2105989454244,
                  1327.9463000443225,
                  1384.8638116378565,
                  1424.2086983114316,
                  1466.9193933851811,
                  1513.634430731889,
                  1562.0019197417091,
                  1599.42787011835,
                  1643.400902507891,
                  1671.608969842855,
                  1689.1883153381993,
                  1740.4703860934164,
                  1787.1834386435573])
t_m_test = np.array([0.0,
                  6.8387902298521315,
                  26.140905062134514,
                  26.982467643431075,
                  27.40437310932633,
                  24.685650212049367,
                  19.989548557487986,
                  31.204184795019184,
                  27.917222993408913,
                  22.49585518040235,
                  18.056755387846984,
                  28.01917903624183,
                  26.675820402192304,
                  29.761161855126097,
                  28.726501788038814,
                  17.6418153528898,
                  29.83327848720574,
                  29.913557119328452,
                  27.185632903874662,
                  17.800925629475664,
                  22.987471357061327,
                  22.89829432559175,
                  28.587307477753836,
                  22.76457130944022,
                  21.866341374787808,
                  26.41119510463037,
                  29.419144268940922,
                  18.00552188809892,
                  26.697202062350033,
                  14.299924031436893,
                  28.73570109889804,
                  28.917511593534144,
                  23.344886673575143,
                  18.710695073749605,
                  28.715037346708055,
                  26.367489009820087,
                  15.425950376640884,
                  21.973032389540933,
                  4.208067334963956,
                  5.579345495344229,
                  27.28207075521709,
                  26.713052550140944,
                  39.81656135644266])
a_test = [2257.0,
                  2578.0,
                  4719.0,
                  3979.0,
                  3606.0,
                  1545.0,
                  4784.0,
                  3764.0,
                  8866.0,
                  5629.0,
                  5827.0,
                  780.0,
                  350.0,
                  5500.0,
                  1044.0,
                  8734.0,
                  3021.0,
                  3687.0,
                  5351.0,
                  4771.0,
                  9117.0,
                  2661.0,
                  6781.0,
                  8810.0,
                  4142.0,
                  2172.0,
                  5434.0,
                  6065.0,
                  2522.0,
                  6782.0,
                  6264.0,
                  6416.0,
                  145.0,
                  1876.0,
                  3022.0,
                  2694.0,
                  3659.0,
                  8988.0,
                  7115.0,
                  7016.0,
                  831.0,
                  6018.0,
                  5037.0]
a_int = [int(a_now) for a_now in a_test]


trip = TripInSpace(t_arr_test, t_m_test, a_int)

######### GUI ######################

root = tk.Tk()
root.title("Image Viewer")

def update_figures(event, start, stop):
    stop = int(stop)
    start = int(start)
    ax1.clear()
    ax2.clear()
    trip.plot_traj_orbits(ax1, start, stop)
    trip.plot_transfer(ax2, start)
    canvas1.draw()
    canvas2.draw()

figure1 = Figure(figsize=(5, 4), dpi=100)
ax1 = figure1.add_subplot(111, projection = '3d')
#plot_traj_orbits(asteroid_abfolge, abflug_zeit, anreise_zeit, verweil_zeit, ax1, 0, 0)
canvas1 = FigureCanvasTkAgg(figure1, master=root)
canvas1.draw()
canvas1.get_tk_widget().grid(row=0, column=0)

figure2 = Figure(figsize=(5, 4), dpi=100)
ax2 = figure2.add_subplot(111,projection = '3d')
#plot_transfer(asteroid_abfolge, abflug_zeit, anreise_zeit, ax2, 0)
canvas2 = FigureCanvasTkAgg(figure2, master=root)
canvas2.draw()
canvas2.get_tk_widget().grid(row=0, column=1)



# #TEST Create a second frame for the second row
# second_row_frame = Frame(root)
# second_row_frame.grid(row=1, column=0, sticky='w')

# # Create two labels in column 0 and 1
# label3 = Label(second_row_frame, text="Column 1, row 2")
# label3.grid(row=0, column=0)

# label4 = Label(second_row_frame, text="Column 2, row 2")
# label4.grid(row=0, column=1)

# text1 = tk.Label(root, text="Current Asteroid")
# text1.grid(row=1, column=1, sticky='w')



# Create four progress bars
progress1 = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress1.grid(row=2, column=0, sticky='w')
progress1.configure(value=20)
progress1_labels = tk.Label(root, text= "Material 0:")
progress1_labels.grid(row=1, column=0, sticky='w')

progress2 = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress2.grid(row=4, column=0, sticky='w')
progress2.configure(value=25)
progress2_labels = tk.Label(root, text= "Material 1:")
progress2_labels.grid(row=3, column=0, sticky='w')

progress3 = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress3.grid(row=6, column=0, sticky='w')
progress3.configure(value=30)
progress3_labels = tk.Label(root, text= "Material 2:")
progress3_labels.grid(row=5, column=0, sticky='w')

progress4 = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress4.grid(row=8, column=0, sticky='w')
progress4.configure(value=35)
progress4_labels = tk.Label(root, text= "Material 3:")
progress4_labels.grid(row=7, column=0, sticky='w')

# Create two labels to display text
text1 = tk.Label(root, text="Current Asteroid")
text1.grid(row=1, column=1, sticky='w')
text2 = tk.Label(root, text="Asteroid 50")
text2.grid(row=2, column=1, sticky='w')
text3 = tk.Label(root, text="Time to mine")
text3.grid(row=3, column=1, sticky='w')
text4 = tk.Label(root, text="13 days")
text4.grid(row=4, column=1, sticky='w')
text5 = tk.Label(root, text="Next Asteroid")
text5.grid(row=5, column=1, sticky='w')
text6 = tk.Label(root, text="Asteroid 152")
text6.grid(row=6, column=1, sticky='w')
text7 = tk.Label(root, text="Time of flight")
text7.grid(row=7, column=1, sticky='w')
text7 = tk.Label(root, text="7 days")
text7.grid(row=8, column=1, sticky='w')

# text_var = tk.StringVar()
# text_box = tk.Entry(root, textvariable=text_var)
# text_box.grid(row=9, column=1, sticky='w')
# text_box.bind('<Return>', lambda event: update_figures(event,text_var.get()))

text_var1 = tk.StringVar()
text_box1 = tk.Entry(root, textvariable=text_var1)
text_box1.insert(0,"Start")
text_box1.grid(row=9, column=1, sticky = 'w')

text_var2 = tk.StringVar()
text_box2 = tk.Entry(root, textvariable=text_var2)
text_box2.insert(0,"Stop")
text_box2.grid(row=10, column=1, sticky = 'w')

text_box1.bind('<Return>', lambda event: update_figures(event, text_var1.get(), text_var2.get()))
text_box2.bind('<Return>', lambda event: update_figures(event, text_var1.get(), text_var2.get()))


root.mainloop()


#idea: usar columnspan com mais colunas, mas falar q as 2 images ocupam mais espaco