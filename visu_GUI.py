
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
root.configure(bg="white")
schritt_wert = 0

def update_figures(event, schritt):
    schritt = int(schritt)
    ax0.clear()
    ax1.clear()
    ax2.clear()
    ax3.clear()
    trip.plot_traj_complete(ax0, schritt)
    trip.plot_traj_orbits(ax1, schritt)
    trip.plot_transfer(ax2, schritt)
    trip.plot_bestand(ax3,schritt)
    canvas0.draw()
    canvas1.draw()
    canvas2.draw()
    canvas3.draw()

figure0 = Figure(figsize=(4, 3), dpi=100)
ax0 = figure0.add_subplot(111, projection = '3d')
canvas0 = FigureCanvasTkAgg(figure0, master=root)
canvas0.draw()
canvas0.get_tk_widget().grid(row=0, column=0,pady=15)

figure1 = Figure(figsize=(4, 3), dpi=100)
ax1 = figure1.add_subplot(111, projection = '3d')
canvas1 = FigureCanvasTkAgg(figure1, master=root)
canvas1.draw()
canvas1.get_tk_widget().grid(row=0, column=1,pady=15,columnspan=3)

figure2 = Figure(figsize=(4, 3), dpi=100)
ax2 = figure2.add_subplot(111,projection = '3d')
canvas2 = FigureCanvasTkAgg(figure2, master=root)
canvas2.draw()
canvas2.get_tk_widget().grid(row=0, column=4,pady=15,columnspan=3)

figure3 = Figure(figsize=(4, 3), dpi=100)
ax3 = figure3.add_subplot(111)
canvas3 = FigureCanvasTkAgg(figure3, master=root)
canvas3.draw()
canvas3.get_tk_widget().grid(row=2, column=0,pady=15,rowspan=8)

# Create two labels to display text
Font_head = ("Cambria", 18, "bold")
Font_middle = ("Cambria", 13, "bold")
Font_small = ("Cambria", 10)

text2 = tk.Label(root, text="Aktueller Asteroid")
text2.grid(row=3, column=4,sticky='e')
text2.configure(font = Font_middle, background = "white" )
text3 = tk.Label(root, text="  -  ", relief="groove" , bd=2)
text3.grid(row=3, column=5)
text3.configure(font = Font_small, background = "white" ,width=4,height=1)
text4 = tk.Label(root, text="Material")
text4.grid(row=4, column=4,sticky='e')
text4.configure(font = Font_small, background = "white" )
text5 = tk.Label(root, text="  -  ", relief="groove" , bd=2)
text5.grid(row=4, column=5)
text5.configure(font = Font_small, background = "white" ,width=4,height=1)

text6 = tk.Label(root, text="Nächster Asteroid")
text6.grid(row=5, column=4,sticky='e')
text6.configure(font = Font_middle, background = "white" )
text7 = tk.Label(root, text="-", relief="groove" , bd=2)
text7.grid(row=5, column=5)
text7.configure(font = Font_small, background = "white" ,width=4,height=1)
text8 = tk.Label(root, text="Material")
text8.grid(row=6, column=4,sticky='e')
text8.configure(font = Font_small, background = "white" )
text9 = tk.Label(root, text="-", relief="groove" , bd=2)
text9.grid(row=6, column=5)
text9.configure(font = Font_small, background = "white",width=4,height=1 )
text10 = tk.Label(root, text="Time of Flight")
text10.grid(row=7, column=4,sticky='e')
text10.configure(font = Font_small, background = "white" )
text11 = tk.Label(root, text="-", relief="groove" , bd=2)
text11.grid(row=7, column=5)
text11.configure(font = Font_small, background = "white",width=4,height=1 )

score_1 = tk.Label(root, text="Die aktuelle Güte ist")
score_1.grid(row=3, column=1,pady = 5,columnspan=3,sticky="nsew")
score_1.configure(font = Font_head, background = "white" )
score_2 = tk.Label(root, text="  -  ", relief="groove" , bd=2)
score_2.grid(row=4, column=2,pady=15,sticky="nsew")
score_2.configure(font = Font_middle, background = "green",width=5,height=2 )

# Create two buttons in row 1 that occupy the same column span

text1 = tk.Label(root, text="Wählen sie den Schritt")
text1.grid(row=6, column=1, pady=5,columnspan=3,sticky="nsew")
text1.configure(font = Font_head, background = "white" )

button1 = Button(root, text="<--", command=lambda: update_gui(1))
button1.grid(row=7, column=1,sticky="nsew", padx=5, pady=5)
button2 = Button(root, text="-->", command=lambda: update_gui(2))
button2.grid(row=7, column=3,sticky="nsew", padx=5, pady=5)

button_text = tk.Label(root, text= schritt_wert, relief="groove" , bd=5)
button_text.grid(row=7, column=2)
button_text.configure(font = Font_small, background = "white",width=15,height=2 )

def update_values(event,schritt):
    schritt = int(schritt)
    current_ast = str(a_int[schritt-1])
    next_ast = str(a_int[schritt])
    text3.config(text=current_ast)
    text7.config(text=next_ast)
    score_2.config(text = trip.get_score(schritt) ) 

def update_gui(button_num):
    global schritt_wert 
    if button_num == 1:
        if schritt_wert >0 and schritt_wert<len(a_int):
            schritt_wert = schritt_wert-1
            button_text.config(text = schritt_wert)
            update_figures(None,schritt_wert)
            update_values(None,schritt_wert)
        else:  
            schritt_wert = 0
        
    elif button_num == 2:
        if schritt_wert >=0 and schritt_wert<len(a_int):
            schritt_wert = schritt_wert+1
            button_text.config(text = schritt_wert)
            update_figures(None,schritt_wert)
            update_values(None,schritt_wert)
        else:  
            schritt_wert = len(a_int)-1

root.mainloop()