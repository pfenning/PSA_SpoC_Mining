
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter import *

import numpy as np
from TripInSpace import TripInSpace


############## EINGABE ##############
solution = np.array([0.0, 6.0, 44.89829432559175, 83.47116357540948, 130.9966784216485, 180.9375413470957, 226.117306761021, 279.79064788951524, 328.20184299414564, 397.1660710199269, 445.2387129518669, 489.9359150142169, 532.2378655762978, 590.5693005187309, 625.8921365907731, 667.5513917986847, 703.9613026661444, 756.9155960745584, 807.3416467840054, 850.1205126139297, 892.8828766265768, 928.8070078722897, 978.9775808769175, 1027.287603616339, 1068.9510570277462, 1119.2098178345923, 1170.142497438265, 1215.8490746101795, 1293.1768923824368, 1338.4589631376539, 1374.1943552729617, 1424.3399412272074, 1479.807002451859, 1544.7504792039024, 1580.221496074216, 1633.6546511649265, 1681.0590242742528, 1720.5595500313777, 1755.7761148850623, 1797.2043048871076, 0.0, 22.89829432559175, 14.572869249817726, 25.525514846239034, 25.940862925447185, 27.179765413925317, 25.673341128494215, 26.41119510463037, 40.964228025781246, 24.07264193193996, 26.697202062350033, 26.301950562080936, 30.331434942433, 29.322836072042275, 17.659255207911563, 22.40991086745975, 28.954293408413893, 26.426050709447047, 24.77886582992423, 18.762364012647105, 19.924131245712886, 22.170573004627844, 28.310022739421548, 27.66345341140705, 28.258760806846166, 28.932679603672707, 23.706577171914414, 49.32781777225733, 27.28207075521709, 27.73539213530777, 28.14558595424574, 27.46706122465157, 44.9434767520434, 23.471016870313733, 29.433155090710454, 27.40437310932633, 21.50052575712502, 21.21656485368463, 21.428190002045326, 29.795695112892417, 5333, 2661, 926, 8370, 1385, 8829, 4745, 2172, 1133, 9332, 2522, 9703, 9588, 6781, 4149, 9717, 3167, 8719, 4467, 555, 2728, 7356, 5793, 6945, 4587, 4722, 601, 4203, 831, 9938, 9018, 6321, 2, 5383, 1070, 3606, 8237, 3690, 404, 7163])


########### Trip initialisieren ############
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
canvas3.get_tk_widget().grid(row=2, column=0,pady=15,rowspan=9)

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
text12 = tk.Label(root, text="Abgebaute Material")
text12.grid(row=5, column=4,sticky='e')
text12.configure(font = Font_small, background = "white" )
text13 = tk.Label(root, text="  -  ", relief="groove" , bd=2)
text13.grid(row=5, column=5)
text13.configure(font = Font_small, background = "white" ,width=4,height=1)
text14 = tk.Label(root, text="Hinterlassene Material")
text14.grid(row=6, column=4,sticky='e')
text14.configure(font = Font_small, background = "white" )
text15 = tk.Label(root, text="  -  ", relief="groove" , bd=2)
text15.grid(row=6, column=5)
text15.configure(font = Font_small, background = "white" ,width=4,height=1)


text6 = tk.Label(root, text="Nächster Asteroid")
text6.grid(row=8, column=4,sticky='e')
text6.configure(font = Font_middle, background = "white" )
text7 = tk.Label(root, text="-", relief="groove" , bd=2)
text7.grid(row=8, column=5)
text7.configure(font = Font_small, background = "white" ,width=4,height=1)
text8 = tk.Label(root, text="Material")
text8.grid(row=9, column=4,sticky='e')
text8.configure(font = Font_small, background = "white" )
text9 = tk.Label(root, text="-", relief="groove" , bd=2)
text9.grid(row=9, column=5)
text9.configure(font = Font_small, background = "white",width=4,height=1 )
text10 = tk.Label(root, text="Time of Flight")
text10.grid(row=10, column=4,sticky='e')
text10.configure(font = Font_small, background = "white" )
text11 = tk.Label(root, text="-", relief="groove" , bd=2)
text11.grid(row=10, column=5)
text11.configure(font = Font_small, background = "white",width=4,height=1 )

score_1 = tk.Label(root, text="Die aktuelle Güte ist")
score_1.grid(row=3, column=1,pady = 5,columnspan=3,sticky="nsew")
score_1.configure(font = Font_head, background = "white" )
score_2 = tk.Label(root, text="  -  ", relief="groove" , bd=2)
score_2.grid(row=4, column=2,pady=15,sticky="nsew",rowspan=3)
score_2.configure(font = Font_middle, background = "green",width=5,height=2 )

# Create two buttons in row 1 that occupy the same column span
text1 = tk.Label(root, text="Wählen Sie den Schritt")
text1.grid(row=8, column=1, pady=5,columnspan=3,sticky="nsew")
text1.configure(font = Font_head, background = "white" )

button1 = Button(root, text="<--", command=lambda: update_gui(1))
button1.grid(row=9, column=1,sticky="nsew", padx=5, pady=5,rowspan=2)
button2 = Button(root, text="-->", command=lambda: update_gui(2))
button2.grid(row=9, column=3,sticky="nsew", padx=5, pady=5,rowspan=2)

button_text = tk.Label(root, text= schritt_wert, relief="groove" , bd=5)
button_text.grid(row=9, column=2,rowspan=2)
button_text.configure(font = Font_small, background = "white",width=15,height=2 )

def update_values(event,schritt):
    schritt = int(schritt)
    current_ast = str(a_test[schritt])
    text3.config(text=current_ast)
    text5.config(text=f"{trip.get_material(schritt)}")
    text13.config(text=f"{trip.get_mined_material(schritt):.1f}")
    text15.config(text=f"{trip.get_missed_material(schritt):.1f}")

    if schritt+1 < len(a_test):
        next_ast = str(a_test[schritt+1])
        text7.config(text=next_ast)
        text9.config(text=f"{trip.get_material(schritt+1)}")
        text11.config(text=f"{trip.get_tof(schritt+1):.1f}")
    else:
        text7.config(text=" - ")
        text9.config(text=" - ")
        text11.config(text=" - ")
        text13.config(text=" - ")
        text15.config(text=" - ")

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

update_figures(None, 0)
update_values(None, 0)

root.mainloop()