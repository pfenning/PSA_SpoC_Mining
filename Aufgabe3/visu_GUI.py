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
solution = np.array([0.0, 16.0, 62.45105066575198, 135.43351830918306, 184.35326981635265, 230.9121897504506, 288.2350258224929, 319.178306733055, 361.2828297752968, 404.342770222788, 453.36195568021793, 507.05309623337564, 546.7200918140377, 594.5652909975905, 636.4141983404985, 711.5399832226511, 758.894890637341, 804.7590069285344, 838.55993255801, 879.0295433554976, 947.8604984547422, 989.7780689814829, 1041.5859434873178, 1085.0224636797, 1142.5656157273322, 1188.1309648564277, 1236.9839401733548, 1277.2287040933024, 1314.3836245275645, 1348.3731730850525, 1393.0588232971018, 1439.6146060580775, 1485.9703361877484, 1526.6954244259296, 1573.6006820795346, 1624.858639800528, 1674.5390655073606, 1710.7106354242333, 1753.849975216157, 1789.9766156767644, 0.0, 24.45105066575198, 46.98246764343108, 20.919751507169583, 18.55891993409795, 29.322836072042275, 14.943280910562102, 22.104523042241794, 29.05994044749116, 27.019185457429966, 29.691140553157695, 29.666995580662036, 21.845199183552847, 21.84890734290797, 47.125784882152644, 29.354907414689773, 23.864116291193472, 17.800925629475664, 28.469610797487555, 40.830955099244605, 25.91757052674068, 23.807874505834942, 23.436520192382098, 29.543152047632216, 29.56534912909546, 24.852975316927076, 26.244763919947747, 23.15492043426198, 19.989548557487986, 26.685650212049367, 26.55578276097568, 26.35573012967087, 24.72508823818114, 28.905257653605187, 29.257957720993403, 27.6804257068326, 18.171569916872656, 29.139339791923593, 26.126640460607362, 37.02338432323563, 2447.0, 3385.0, 3979.0, 735.0, 4618.0, 6781.0, 4056.0, 7316.0, 3413.0, 2992.0, 10.0, 9187.0, 1444.0, 7060.0, 4433.0, 854.0, 2515.0, 4771.0, 4802.0, 1839.0, 6867.0, 6747.0, 5694.0, 8547.0, 390.0, 1844.0, 2630.0, 5231.0, 4784.0, 1545.0, 4121.0, 4069.0, 4204.0, 394.0, 6358.0, 9334.0, 9368.0, 5568.0, 1038.0, 4087.0, ])
idx_split1 = int(len(solution)/3)
idx_split2 = 2*idx_split1
t_arr_test = solution[:idx_split1]
t_m_test = solution[idx_split1:idx_split2]
a_test = [int(a_now) for a_now in solution[idx_split2:]]

trip = TripInSpace(t_arr_test, t_m_test, a_test)
# trip.pretty()

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