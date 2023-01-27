import copy
import matplotlib.pyplot as plt
import numpy as np
from pykep.orbit_plots import plot_planet, plot_lambert
from pykep import AU, DAY2SEC
import pykep as pk

from SpoC_Constants import abbau, get_dv, DV_per_propellant, get_asteroid_material, get_asteroid_mass, get_asteroid
from SpoC_Constants import T_START, MU_TRAPPIST

class TripInSpace:
    def __init__(self, t_arr, t_m, a):
        self.t_start = T_START.mjd2000
        assert len(t_arr) == len(t_m) == len(a), f"Eingangsvektoren weisen unterschiedliche Längen auf:{len(t_arr)}, {len(t_m)}, {len(a)} "
        self.t_arr = t_arr  # Ankunftszeit auf Asteroid mit selbem Index (für Start = 0)
        self.t_m = t_m      # Abbauzeit auf Asteroid mit selbem Index
        self.a = a          # Asteroiden
        # Spritverbrauch bestimmen
        self.dv=[0.0]       # Spritverbrauch hin zum Asteroiden mit selbem Index (für Start = 0)
        self._get_dv()
        self.bestand=[[0.0, 0.0, 0.0, 1.0]] # Bestand nach Abbau des Asteroids mit selbem Index (auf 1. Asteroid wird nichts abgebaut)
        self._mine_and_travel()

    def _get_dv(self):
        """
        Bestimmt DV für alle asteroiden
        :return:
        """
        for start, stop, t_arr_last, t_arr, t_m_last \
                in zip(self.a[:-1], self.a[1:], self.t_arr[:-1], self.t_arr[1:], self.t_m[:-1]):
            print(f"Start:{start}, Stopp:{stop}, Abflug:{t_arr_last + t_m_last:.0f}, Flugdauer:{t_arr-t_m_last-t_arr_last:.0f}")
            self.dv.append(get_dv(get_asteroid(start), get_asteroid(stop), t_arr_last + t_m_last, t_arr-t_m_last-t_arr_last))

    def _mine_and_travel(self):
        """
        Bestimmt Bestand nach Abbau auf letztem Asteroiden und Flug zum neuen aktuellen Asteroiden
        :return
        """
        for asteroid_id, t_m, dv in zip(self.a[1:], self.t_m[1:], self.dv[1:]): # Auf Startasteroid wird nicht abgebaut
            self.bestand.append(copy.deepcopy(self.bestand[-1]))
            self.bestand[-1][3] -= dv/DV_per_propellant
            abbau(self.bestand[-1], get_asteroid_mass(asteroid_id), get_asteroid_material(asteroid_id), t_m)

    def plot_trajectory(self, stop, steps_shown):
        """
        Plottet die Trajektorie bis zum Abflug von Asteroid stop
        mit stops_shown als Anzahl zu sehender letzter Asteroiden
        :param stop:        letzter zu plottender Stop (0 => Startasteroid)
        :param steps_shown: Anzahl gleichzeitig zu sehender Asteroiden mit Trajektorie und Orbit
        :return:
        """
        pass

    def abflugzeit(self, index):
        """
        Abflugzeit vom letzten Asteroid, um auf Asteroid an Position stop zu komme
        :param index: Index des Zielasteroiden (0 => Startasteroid
        :return: Abflugzeit
        """
        return self.t_arr[index - 1] + self.t_m[index - 1]

    def plot_traj_orbits(self, ax1, start_, stop):
        """
        Plotten der Trajektorien ausgehend von Schritt start_ (also von Asteroid start_-1 auf Asteroid start_)
        bis zum Schritt stop.
        :param ax1:     Axes-Objekt, in das gezeichnet werden soll
        :param start_:  Start-Schritt (0<start_)
        :param stop:    Letzter anzuzeigender Schritt (start_<stop)
        :return:
        """
        ### Überprüfen der Eingabeparameter ###
        # Type
        if isinstance(start_, float):
            start_ = int(start_)
        elif not isinstance(start_,int):
            raise TypeError("Falscher Datentyp übergeben")
        if isinstance(stop, float):
            stop = int(stop)
        elif not isinstance(stop,int):
            raise TypeError("Falscher Datentyp übergeben")
        # Wertebereich prüfen notfalls anpassen (Ließe sich auch mit Fehlermeldung lösen)
        if start_ < 1:
            start_ = 1
        elif stop < start_:
            stop = start_
        elif len(self.a)-1 < stop:
            stop = len(self.a)-1
            if len(self.a)-1 < start_:
                start_ = stop
        ### Funktion ###
        # Einstellung für Plot
        ax1.scatter([0], [0], [0], color=['y'])
        ax1.set_xlim(-0.3, 0.3)
        ax1.set_ylim(-0.3, 0.3)
        ax1.set_zlim(-0.03, 0.03)
        # Plotten der Trajektorien von Start bis Stop
        for index, el in enumerate(self.a[start_:stop + 1], start=start_):
            # Position abrufen
            t0 = pk.epoch(self.abflugzeit(index)).mjd2000 + self.t_start
            t1 = pk.epoch(self.t_arr[index]).mjd2000 + self.t_start
            tv = pk.epoch(self.abflugzeit[index+1]).mjd2000 + self.t_start
            dt = (t1 - t0) * DAY2SEC  # muss in sec sein

            # pos and velocitiy
            r1, v1 = get_asteroid(self.a[index-1]).eph(t0)
            r2, v2 = get_asteroid(self.a[index]).eph(t1)

            # Lambert
            l = pk.lambert_problem(r1=r1, r2=r2, tof=dt, mu=MU_TRAPPIST, max_revs=2)

            # Plot planet
            plot_planet(get_asteroid(self.a[index-1]), t0=t0, color='r', alpha=0.1, units=AU, axes=ax1, s=5)
            plot_planet(get_asteroid(self.a[index]), t0=t1, color='r', alpha=0.1, units=AU, axes=ax1, s=5)
            # Plot the Lambert solutions
            axes1 = plot_lambert(l, color='b', units=AU, axes=ax1)
            # Plot part of the orbit
            plot_planet(get_asteroid(self.a[index]), t0=t1, tf=tv, color='k', alpha=1, units=AU, axes=ax1, s=5)
            plot_planet(get_asteroid(self.a[index]), t0=tv, color='y', alpha=0, units=AU, axes=ax1, s=5)

    def plot_transfer(self, ax1, start_):
        """
        Plotten den Transfer zum Asteroid mit Index start_ (also von Asteroid start_-1 auf Asteroid start_)
        :param ax1:     Axes-Objekt, in das gezeichnet werden soll
        :param start_:  Anzuzeigender Schritt (0<start_)
        :return:
        """
        ### Überprüfen der Eingabeparameter ###
        # Type
        if isinstance(start_, float):
            start_ = int(start_)
        elif not isinstance(start_,int):
            raise TypeError("Falscher Datentyp übergeben")  # ToDo Fehlermeldung in GUI abfangen?
        # Wertebereich prüfen notfalls anpassen (Ließe sich auch mit Fehlermeldung lösen)
        if start_ < 1:
            start_ = 1
        elif len(self.a) - 1 < start_:
            start_ = len(self.a) - 1

        ### Funktion ###
        # Einstellung für Plot
        ax1.scatter([0], [0], [0], color=['y'])
        ax1.set_xlim(-0.3, 0.3)
        ax1.set_ylim(-0.3, 0.3)
        ax1.set_zlim(-0.03, 0.03)

        for index, el in enumerate(self.a[start_:start_ + 1], start=start_):
            # Position abrufen
            t0 = pk.epoch(self.abflugzeit(index)).mjd2000 + self.t_start
            t1 = pk.epoch(self.t_arr[index]).mjd2000 + self.t_start
            dt = (t1 - t0) * DAY2SEC  # muss in sec sein

            # pos and velocitiy
            r1, v1 = get_asteroid(self.a[index-1]).eph(t0)
            r2, v2 = get_asteroid(self.a[index]).eph(t1)

            # Lambert
            l = pk.lambert_problem(r1=r1, r2=r2, tof=dt, mu=MU_TRAPPIST, max_revs=2)

            # Plot the Lambert solutions
            plot_lambert(l, color='b', units=AU, axes=ax1)
            plot_planet(get_asteroid(self.a[index-1]), t0=t0, color='r', alpha=0.1, units=AU, axes=ax1, s=5)
            plot_planet(get_asteroid(self.a[index]), t0=t1, color='r', alpha=0.1, units=AU, axes=ax1, s=5)

    def plot_bestand(self, index):
        """
        Plotten den Bestand der Rohstoffe ohne Sprit für den übergebenen Stop
        :param index: gefragter Asteroid (0 => Startasteroid)
        :return:
        """
        if not isinstance(index, int):
            raise ValueError("Negative Werte sind nicht erlaubt")
        if (len(self.a)-1) < index:
            index = len(self.a) - 1
        elif index < 0:
            raise ValueError("Negative Werte sind nicht erlaubt")
        bars = ("0", "1", "2")
        y_pos = np.arange(len(bars))
        plt.barh(y_pos, self.bestand[index][:3], color="green")
        plt.yticks(y_pos, bars)
        plt.ylabel("Material")
        plt.xlabel("Bestand")
        for i, v in enumerate(self.bestand[index][:3]):
            plt.text(v+3, i+.25, f"{v:.3f}", color="blue", fontweight="bold")

    def get_tank(self, index):
        """
        Gibt Tankfüllung auf Asteroiden an übergebener Position wieder
        :param index:   gewünschte Position
        :return:        Tankfüllung auf Asteroiden an übergebener Position
        """
        return self.bestand[index][3]

    def pretty(self):
        """
        Tabelle mit allen relevanten Werten für Trip im Stil von udp.pretty
        :return:
        """
        print("Asteroid ID | Ankunft | DV | Tank | Bestand | Güte")
        for asteroid_id, t_arr, dv, bestand in zip(self.a, self.t_arr, self.dv, self.bestand):
            print(f"{asteroid_id}   {t_arr:.0f}   {dv:.0f}   {bestand[3]:.3}   "
                  f"{bestand[0]:.3} | {bestand[1]:.3} | {bestand[2]:.3}   {min(bestand[:3]):.3}")




solution = np.array([0.0, 14.0, 43.05195942972621, 108.44064918789744, 187.72271994311453, 231.58011877338353, 274.29667681758394, 319.0527790883107, 356.48929928069276, 404.82867806311134, 448.0875378535731, 491.1281545876904, 536.8528491725237, 584.17787433059, 638.9214997056258, 697.8197940312176, 749.1426301032599, 778.9435557327355, 835.8978491411494, 877.3022222504758, 915.6380291442449, 951.142865329752, 996.6296072220414, 1041.7845276563035, 1086.3694478305792, 1138.5436615300548, 1180.6041018730295, 1207.9301177581258, 1244.8659200020704, 1288.3865100316102, 1363.5724720762103, 1425.802499753223, 1468.5155523033638, 1522.8169987110996, 1571.4378508464004, 1614.537136194919, 1684.89286632459, 1736.7659544714788, 1783.874577529575, 0.0, 9.051959429726208, 37.388689758171225, 51.28207075521709, 29.857398830269005, 24.716558044200415, 24.75610227072673, 23.436520192382098, 24.339378782418564, 27.258859790461788, 27.040616734117293, 29.7246945848333, 29.325025158066317, 26.74362537503583, 30.89829432559175, 33.32283607204228, 17.800925629475664, 28.954293408413893, 27.40437310932633, 28.335806893769146, 19.50483618550705, 29.48674189228935, 23.15492043426198, 16.58492017427583, 28.17421369947553, 28.06044034297483, 21.326015885096343, 24.93580224394458, 21.520590029539893, 47.18596204460001, 34.23002767701266, 26.713052550140944, 28.301446407735835, 28.620852135300712, 23.0992853485186, 42.355730129670874, 31.873088146888993, 19.108623058096036, 43.125422470425065, 2447.0, 592.0, 6842.0, 831.0, 3965.0, 5051.0, 1552.0, 5694.0, 1202.0, 4671.0, 2378.0, 1409.0, 5268.0, 9509.0, 2661.0, 6781.0, 4771.0, 3167.0, 3606.0, 3709.0, 5120.0, 4934.0, 5231.0, 1139.0, 644.0, 1917.0, 9810.0, 2919.0, 480.0, 2023.0, 7916.0, 6018.0, 4862.0, 63.0, 6936.0, 4069.0, 9524.0, 8292.0, 9008.0, ])
idx_split1 = int(len(solution)/3)
idx_split2 = 2*idx_split1
t_arr_test = solution[:idx_split1]
t_m_test = solution[idx_split1:idx_split2]
a_test = solution[idx_split2:]

a_int = [int(a_now) for a_now in a_test]


trip = TripInSpace(t_arr_test, t_m_test, a_int)

trip.pretty()
trip.plot_bestand(25)
plt.show()

