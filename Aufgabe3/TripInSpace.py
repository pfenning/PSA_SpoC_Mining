import copy
import matplotlib.pyplot as plt
import numpy as np
from pykep.orbit_plots import plot_planet, plot_lambert
from pykep import AU, DAY2SEC
import pykep as pk
from SpoC_Constants import abbau, get_dv, DV_per_propellant, get_asteroid_material, get_asteroid_mass, get_asteroid, get_abbau_menge
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
            # print(f"Start:{start}, Stopp:{stop}, Abflug:{t_arr_last + t_m_last:.0f}, Flugdauer:{t_arr-t_m_last-t_arr_last:.0f}")
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

    def abflugzeit(self, index):
        """
        Abflugzeit vom aktuellen Asteroid an Stelle index
        :param index: Index des gesuchten Asteroiden (0 => Startasteroid)
        :return: Abflugzeit
        """
        return self.t_arr[index] + self.t_m[index]

    def plot_traj_orbits(self, ax1, step, use_case='last_step_count', steps_shown=3):
        """
        Plotten der Trajektorien ausgehend von Schritt start_ (also von Asteroid start_-1 auf Asteroid start_)
        bis zum Schritt stop.
        :param ax1:         Axes-Objekt, in das gezeichnet werden soll
        :param step:        letzter Schritt, der geplottet werden soll (0<start_)
        :param use_case:    Anwendung → Setzt automatisch step_count ('next', 'last_step_count', 'up to step'
        :param steps_shown: wie viele Schritte gezeigt werden sollen
        :return:
        """
        ### Überprüfen der Eingabeparameter ###
        # Type
        if isinstance(step, float):
            step = int(step)
        elif not isinstance(step, int):
            raise TypeError("Falscher Datentyp übergeben")
        # Wertebereich prüfen notfalls anpassen (Ließe sich auch mit Fehlermeldung lösen)
        if step < 0:
            step = 0
        elif len(self.a) - 1 < step:
            step = len(self.a) - 1

        ### Funktion ###
        # Einstellung für Plot
        ax1.scatter([0], [0], [0], color=['y'])
        ax1.set_xlim(-0.3, 0.3)
        ax1.set_ylim(-0.3, 0.3)
        ax1.set_zlim(-0.03, 0.03)

        # Start und Stop definieren
        planet = True   # Ob Planeten und Orbits geplottet werden sollen
        mining = True   # Ob die Zeit auf dem Asteroiden geplottet werden soll
        start_ = 0
        stop = step
        # Use-Case Settings
        if use_case == 'next':
            planet = True
            mining = False
            ax1.set_title('Nächste Trajektorie')
            if step < len(self.a)-1:
                start_ = step + 1
                stop = start_
            else:
                return
        elif step == 0: # Nur Asteroid plotten, sonst nichts
            t0 = pk.epoch(self.t_arr[step]).mjd2000 + self.t_start
            plot_planet(get_asteroid(self.a[step]), t0=t0, color='r', alpha=0.1, units=AU, axes=ax1, s=5)
            return
        elif use_case == 'up to step':
            planet = False
            mining = True
            start_ = 1
            stop = step
            ax1.set_title(f'Alle Trajektorien')
        else:   # "last steps_shown"
            planet = True
            mining = True
            ax1.set_title('Letzten drei Trajektorien')
            if step <= steps_shown:
                start_ = 1
                stop = step
            else:
                start_ = step - steps_shown
                stop = step

        # Plotten der Trajektorien von Start bis Stop
        for index in range(start_,stop+1):
            # Position abrufen
            t0 = pk.epoch(self.abflugzeit(index-1)).mjd2000 + self.t_start
            t1 = pk.epoch(self.t_arr[index]).mjd2000 + self.t_start
            tv = pk.epoch(self.abflugzeit(index)).mjd2000 + self.t_start
            dt = (t1 - t0) * DAY2SEC  # muss in sec sein

            # pos and velocitiy
            r1, v1 = get_asteroid(self.a[index-1]).eph(t0)
            r2, v2 = get_asteroid(self.a[index]).eph(t1)

            # Lambert
            l = pk.lambert_problem(r1=r1, r2=r2, tof=dt, mu=MU_TRAPPIST, max_revs=2)
            if planet:
                # Plot planet
                plot_planet(get_asteroid(self.a[index-1]), t0=t0, color='r', alpha=0.1, units=AU, axes=ax1, s=5)
                plot_planet(get_asteroid(self.a[index]), t0=t1, color='r', alpha=0.1, units=AU, axes=ax1, s=5)
            # Plot the Lambert solutions
            plot_lambert(l, color='b', units=AU, axes=ax1)
            if mining:
                # Plot part of the orbit
                plot_planet(get_asteroid(self.a[index]), t0=t1, tf=tv, color='k', alpha=1, units=AU, axes=ax1, s=5)
                plot_planet(get_asteroid(self.a[index]), t0=tv, color='y', alpha=0, units=AU, axes=ax1, s=5)

    def plot_bestand(self,ax1, index):
        """
        Plotten den Bestand für den übergebenen Stop
        :param index: gefragter Asteroid (0 => Startasteroid)
        :return:
        """
        color_mat = ["gold","orange","silver","green"]
        if not isinstance(index, int):
            raise ValueError("Negative Werte sind nicht erlaubt")
        if (len(self.a)-1) < index:
            index = len(self.a) - 1
        elif index < 0:
            raise ValueError("Negative Werte sind nicht erlaubt")
        bars = ("Gold", "Nickel", "Platin", "Sprit")
        x_pos = np.arange(len(bars))
        ax1.barh(x_pos, self.bestand[index], color=color_mat)
        ax1.set_title('Bestand der Materialien')
        # plt.yticks(x_pos, bars)
        # plt.ylabel("Material")
        # plt.xlabel("Bestand")
        for i, v in enumerate(self.bestand[index]):
            v = round(v,2)
            ax1.annotate(str(v), (v, i), xytext=(-30, 0), textcoords='offset points', va='center')

    def get_tank(self, index):
        """
        Gibt Tankfüllung auf Asteroiden an übergebener Position wieder
        :param index:   gewünschte Position
        :return:        Tankfüllung auf Asteroiden an übergebener Position
        """
        return self.bestand[index][3]

    def get_score(self,index):
        """
        Aktuelle Güte
        :param index:   Index von aktuellem Asteroid
        :return:        aktuelle Güte
        """
        return min(self.bestand[index][:3])

    def get_material(self, index):
        """
        Material des aktuellen Asteroids
        :param index: Index von aktuellem Asteroid
        :return: Material des aktuellen Asteroids
        """
        return get_asteroid_material(self.a[index])

    def get_mined_material(self, index):
        """
        Menge des abgebauten Materials auf aktuellem Asteroid
        :param index: Index von aktuellem Asteroid
        :return: Menge des abgebauten Materials
        """
        # ToDo Matthias aktualisieren
        return get_abbau_menge(self.bestand[index][self.get_material(index)],
                               get_asteroid_mass(self.a[index]),
                               self.get_material(index),
                               self.t_m[index]) \
            - self.bestand[index][self.get_material(index)]
    def get_missed_material(self,index):
        """
        Menge des liegengelassenen Materials auf aktuellem Asteroid
        :param index: Index von aktuellem Asteroid
        :return: Menge des liegengelassenen Materials
        """
        return get_asteroid_mass(self.a[index])-self.get_mined_material(index)

    def get_all_missed_materials_yet(self, index):
        """
        Liegengelassenes Material in Summe auf allen Asteroiden bis zum akteuellen Asteroid.
        Asteroid 0 wird ausgeschlossen, da dort nicht abgebaut werden darf
        :param index: Index von aktuellem Asteroid
        :return: insgesamt liegengelassenes Material
        """
        if index == 1:
            return self.get_missed_material(index)
        else:
            return self.get_missed_material(index) + self.get_all_missed_materials_yet(index-1)

    def get_tof(self, index):
        """
        Flugzeit hin zum aktuellen Asteroiden
        :param index: Index von aktuellem Asteroid
        :return: Flugzeit
        """
        if index == 0:
            return " - "
        else:
            return self.t_arr[index] - self.t_arr[index-1] - self.t_m[index-1]

    def pretty(self):
        """
        Tabelle mit allen relevanten Werten für Trip im Stil von udp.pretty
        :return:
        """
        print("Asteroid ID | Ankunft | DV | Tank | Bestand | Güte")
        for asteroid_id, t_arr, dv, bestand in zip(self.a, self.t_arr, self.dv, self.bestand):
            print(f"{asteroid_id}   {t_arr:.0f}   {dv:.0f}   {bestand[3]:.3}   "
                  f"{bestand[0]:.3} | {bestand[1]:.3} | {bestand[2]:.3}   {min(bestand[:3]):.3}")

