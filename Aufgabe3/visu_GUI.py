
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
# with open("Solution.txt","r") as tf:
#     solution = np.array(tf.read()) # np.loadtxt("Solution.txt")
# solution = np.loadtxt("Solution.txt", delimiter=",")
solution = np.array([0.0, 20.0, 71.28207075521709, 119.03880397768823, 156.8729508200197, 203.5609882194199, 244.69382428787384, 285.038710961449, 329.1510636770093, 379.23654964528663, 436.4407344403058, 472.2471685231399, 514.219590609267, 551.9780100820611, 575.1419605512108, 617.9189642078104, 683.3451634457787, 717.578717741857, 752.5658138338164, 805.0688657178272, 851.6554303070845, 914.1194763554862, 950.6907559772899, 981.3403749440956, 1029.1026493833601, 1077.9268690949098, 1128.0758077810108, 1168.9933193745449, 1204.660086270053, 1261.3226381335446, 1296.4219234820632, 1349.1549173163844, 1398.3303688176732, 1431.499641381145, 1474.212693931286, 1519.0129230203136, 1559.933651238005, 1601.5674113816087, 1649.7089937738408, 1694.5215690911004, 1739.707201994975, 1785.883958072634, 0.0, 27.28207075521709, 29.75673322247114, 27.834146842331478, 26.68803739940021, 23.132836068453948, 26.344886673575143, 28.112352715560267, 24.085485968277332, 31.204184795019184, 23.80643408283411, 17.972422086127086, 29.75841947279408, 7.163950469149648, 16.77700365659967, 37.42619923796828, 28.233554296078264, 22.98709609195938, 24.50305188401082, 28.586564589257367, 34.46404604840161, 28.571279621803683, 6.64961896680579, 27.762274439264335, 20.824219711549656, 24.148938686101065, 28.917511593534144, 23.66676689550811, 28.662551863491668, 23.0992853485186, 28.732993834321125, 29.175451501288684, 19.169272563471914, 26.713052550140944, 18.800229089027653, 24.92072821769155, 21.633760143603585, 28.141582392232063, 16.812575317259565, 27.185632903874662, 24.176756077658833, 41.11604192736604, 9577.0, 831.0, 368.0, 8861.0, 1470.0, 7146.0, 145.0, 1219.0, 4905.0, 3764.0, 8387.0, 6928.0, 4532.0, 6323.0, 5254.0, 8844.0, 740.0, 6374.0, 7521.0, 7875.0, 7588.0, 8312.0, 8431.0, 8168.0, 4076.0, 2179.0, 6416.0, 5677.0, 1454.0, 6936.0, 1751.0, 9524.0, 9197.0, 6018.0, 1666.0, 4370.0, 5111.0, 9644.0, 5257.0, 5351.0, 7523.0, 4315.0, ])
idx_split1 = int(len(solution)/3)
idx_split2 = 2*idx_split1
t_arr_test = solution[:idx_split1]
t_m_test = solution[idx_split1:idx_split2]
a_test = [int(a_now) for a_now in solution[idx_split2:]]

trip = TripInSpace(t_arr_test, t_m_test, a_test)

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
    trip.plot_traj_orbits(ax0, schritt, 'up to step')
    trip.plot_traj_orbits(ax1, schritt, 'last_step_count', steps_shown=3)
    trip.plot_traj_orbits(ax2, schritt, 'next')
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
    current_ast = str(a_test[schritt])
    text3.config(text=current_ast)
    text5.config(text=f"{trip.get_material(schritt)}")
    if schritt+1 < len(a_test):
        next_ast = str(a_test[schritt+1])
        text7.config(text=next_ast)
        text9.config(text=f"{trip.get_material(schritt+1)}")
        text11.config(text=f"{trip.get_tof(schritt+1):.1f}")
    else:
        text7.config(text=" - ")
        text9.config(text=" - ")
        text11.config(text=" - ")
    score_2.config(text = f"{trip.get_score(schritt):.3}")

def update_gui(button_num):
    global schritt_wert 
    if button_num == 1:
        if schritt_wert >1: # and schritt_wert<len(a_test)
            schritt_wert = schritt_wert-1
        else:  
            schritt_wert = 0
    elif button_num == 2:
        if schritt_wert<len(a_test)-1:  # schritt_wert >=0 and
            schritt_wert = schritt_wert+1
            button_text.config(text = schritt_wert)
            update_figures(None,schritt_wert)
            update_values(None,schritt_wert)
        else:  
            schritt_wert = len(a_test)-1
    button_text.config(text=schritt_wert)
    update_figures(None, schritt_wert)
    update_values(None, schritt_wert)

root.mainloop()