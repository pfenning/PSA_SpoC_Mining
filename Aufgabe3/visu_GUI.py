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
solution = np.array([0.0, 14.0, 43.05195942972621, 108.44064918789744, 187.72271994311453, 231.58011877338353, 274.29667681758394, 319.0527790883107, 356.48929928069276, 404.82867806311134, 448.0875378535731, 491.1281545876904, 536.8528491725237, 584.17787433059, 638.9214997056258, 697.8197940312176, 749.1426301032599, 778.9435557327355, 835.8978491411494, 877.3022222504758, 915.6380291442449, 951.142865329752, 996.6296072220414, 1041.7845276563035, 1086.3694478305792, 1138.5436615300548, 1180.6041018730295, 1207.9301177581258, 1244.8659200020704, 1288.3865100316102, 1363.5724720762103, 1425.802499753223, 1468.5155523033638, 1522.8169987110996, 1571.4378508464004, 1614.537136194919, 1684.89286632459, 1736.7659544714788, 1783.874577529575, 0.0, 9.051959429726208, 37.388689758171225, 51.28207075521709, 29.857398830269005, 24.716558044200415, 24.75610227072673, 23.436520192382098, 24.339378782418564, 27.258859790461788, 27.040616734117293, 29.7246945848333, 29.325025158066317, 26.74362537503583, 30.89829432559175, 33.32283607204228, 17.800925629475664, 28.954293408413893, 27.40437310932633, 28.335806893769146, 19.50483618550705, 29.48674189228935, 23.15492043426198, 16.58492017427583, 28.17421369947553, 28.06044034297483, 21.326015885096343, 24.93580224394458, 21.520590029539893, 47.18596204460001, 34.23002767701266, 26.713052550140944, 28.301446407735835, 28.620852135300712, 23.0992853485186, 42.355730129670874, 31.873088146888993, 19.108623058096036, 43.125422470425065, 2447.0, 592.0, 6842.0, 831.0, 3965.0, 5051.0, 1552.0, 5694.0, 1202.0, 4671.0, 2378.0, 1409.0, 5268.0, 9509.0, 2661.0, 6781.0, 4771.0, 3167.0, 3606.0, 3709.0, 5120.0, 4934.0, 5231.0, 1139.0, 644.0, 1917.0, 9810.0, 2919.0, 480.0, 2023.0, 7916.0, 6018.0, 4862.0, 63.0, 6936.0, 4069.0, 9524.0, 8292.0, 9008.0, ])
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