import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from scipy.interpolate import LinearNDInterpolator
import matplotlib.pyplot as plt

# ToDo: Es wird vorausgesetzt, dass die Auflösung so gewählt wird, das gilt: 1/resolution={Integer}


def _fit_to_resolution(num, resolution, fit_type='true'):
    """
    :param num: Number
    :param resolution: Resolution
    :param fit_type: string,
        'lower': abgerundet;
        'upper': aufgerundet;
        'true': korrekt gerundet;
    :return: Number fit to resolution
    """
    if fit_type == 'lower':
        return resolution * int(num / resolution)
    elif fit_type == 'upper':
        return resolution * (int(num / resolution)+1)
    else:
        return resolution * int(round(num/resolution))


def _item_count(resolution, lower=0, upper=1):
    """
    Berechnet Anzahl items, damit linspace Abstand von "resolution" erzeugt
    :param resolution: Resolution
    :param lower: untere Grenze von linspace
    :param upper: obere Grenze von linspace
    :return: number
    """
    return int((upper-lower)/resolution)+1


def _transform(x, x_min=0, x_max=1):
    return (x-x_min)/(x_max-x_min)


class FuzzySystem:
    def __init__(self, verf_min, verf_max, resolution=0.01, load_map=False):
        """
        Erzeugt das Fuzzy-System zur Bewertung von Asteroidenwechseln
        verf_min:

        verf_max: double

        :param verf_min: double,
            Verfügbarkeit des seltensten Materials
        :param verf_max: double,
            Verfügbarkeit des am häufigsten vorkommenen Materials
        :param resolution: 0.01, 0.02, 0.025, 0.05;
            Auflösung der Membership-Funktionen und der Eingangsmatrix
        """
        ############
        # Variablen
        ############
        # Hauptsystem
        self.mas = ctrl.Antecedent(np.linspace(0, 1, _item_count(resolution)), 'Masse')
        self.sprit = ctrl.Antecedent(np.linspace(0, 1, _item_count(resolution)), 'Güte vom Spritverbrauch')
        self.rele = ctrl.Antecedent(np.linspace(0, 1, _item_count(resolution)), 'Relevanz des Materials')
        self.out = ctrl.Consequent(np.linspace(0, 1, _item_count(resolution)), 'Güte des Asteroids')
        # Subsystem 1 - Sprit
        self.t_n = ctrl.Antecedent(np.linspace(0, 1, _item_count(resolution)), 'Tank nach Wechsel')
        self.delt = ctrl.Antecedent(np.linspace(0, 1, _item_count(resolution)), 'Spritverbrauch')
        self.out_sub = ctrl.Consequent(np.linspace(0, 1, _item_count(resolution)), 'Ausgang Subsystem 1')
        # Subsystem 2 - Material
        self.verf = ctrl.Antecedent(np.linspace(0, 1, _item_count(resolution)), 'Verfügbarkeit des Materials')
        self.bes = ctrl.Antecedent(np.linspace(0, 1, _item_count(resolution)), 'Bestand des Materials')
        self.out_sub_2 = ctrl.Consequent(np.linspace(0, 1, _item_count(resolution)), 'Ausgang Subsystem 2')

        ############
        # Generate fuzzy membership functions
        ############
        # Hauptsystem
        self.mas.automf(3)
        self.sprit.automf(3, names=['poor', 'average', 'good'])
        self.rele.automf(3)
        self.out.automf(7)
        # Subsystem 1 - Sprit
        self.t_n.automf(3)
        self.delt['lo'] = fuzz.trapmf(self.delt.universe, [0, 0, 0.1, 0.23])
        self.delt['md'] = fuzz.trimf(self.delt.universe, [0.1, 0.23, 0.37])
        self.delt['hi'] = fuzz.trapmf(self.delt.universe, [0.23, 0.37, 1, 1])
        self.out_sub.automf(7)
        # Subsystem 2 - Material
        self.verf['lo'] = fuzz.trimf(self.verf.universe, [0, 0, 1])
        self.verf['hi'] = fuzz.trimf(self.verf.universe, [0, 1, 1])
        self.bes.automf(3, names=['lo', 'md', 'hi'])    # ToDo: Hab ich an meine Definition von Input angepasst
        self.out_sub_2.automf(5)

        ############
        # Rules & System Initialization
        ############
        # Subsystem 1 - Sprit
        self.rule_subs1 = ctrl.Rule(self.t_n['poor'] & self.delt['lo'], self.out_sub['mediocre'])
        self.rule_subs2 = ctrl.Rule(self.t_n['poor'] & self.delt['md'], self.out_sub['poor'])
        self.rule_subs3 = ctrl.Rule(self.t_n['poor'] & self.delt['hi'], self.out_sub['dismal'])
        self.rule_subs4 = ctrl.Rule(self.t_n['average'] & self.delt['lo'], self.out_sub['decent'])
        self.rule_subs5 = ctrl.Rule(self.t_n['average'] & self.delt['md'], self.out_sub['average'])
        self.rule_subs6 = ctrl.Rule(self.t_n['average'] & self.delt['hi'], self.out_sub['mediocre'])
        self.rule_subs7 = ctrl.Rule(self.t_n['good'] & self.delt['lo'], self.out_sub['excellent'])
        self.rule_subs8 = ctrl.Rule(self.t_n['good'] & self.delt['md'], self.out_sub['good'])
        self.rule_subs9 = ctrl.Rule(self.t_n['good'] & self.delt['hi'], self.out_sub['decent'])

        self.sub_ctrl = ctrl.ControlSystem(
            [self.rule_subs1, self.rule_subs2, self.rule_subs3, self.rule_subs4, self.rule_subs5, self.rule_subs6,
             self.rule_subs7, self.rule_subs8, self.rule_subs9])
        self.sub_sys = ctrl.ControlSystemSimulation(self.sub_ctrl, cache=False)     # ToDo: Cache -> schöner lösen

        # Subsystem 2 - Material
        self.rule_subs_2_1 = ctrl.Rule(self.verf['lo'] & self.bes['lo'], self.out_sub_2['good'])
        self.rule_subs_2_2 = ctrl.Rule(self.verf['lo'] & self.bes['md'], self.out_sub_2['decent'])
        self.rule_subs_2_3 = ctrl.Rule(self.verf['lo'] & self.bes['hi'], self.out_sub_2['average'])
        self.rule_subs_2_4 = ctrl.Rule(self.verf['hi'] & self.bes['lo'], self.out_sub_2['average'])
        self.rule_subs_2_5 = ctrl.Rule(self.verf['hi'] & self.bes['md'], self.out_sub_2['mediocre'])
        self.rule_subs_2_6 = ctrl.Rule(self.verf['hi'] & self.bes['hi'], self.out_sub_2['poor'])

        self.sub_ctrl_2 = ctrl.ControlSystem(
            [self.rule_subs_2_1, self.rule_subs_2_2, self.rule_subs_2_3, self.rule_subs_2_4, self.rule_subs_2_5,
             self.rule_subs_2_6])
        self.sub_sys_2 = ctrl.ControlSystemSimulation(self.sub_ctrl_2, cache=False)     # ToDo: Cache -> schöner lösen

        # Hauptsystem
        self.rule1 = ctrl.Rule(self.rele['good'] & self.mas['poor'] & self.sprit['poor'], self.out['poor'])
        self.rule2 = ctrl.Rule(self.rele['good'] & self.mas['poor'] & self.sprit['average'], self.out['mediocre'])
        self.rule3 = ctrl.Rule(self.rele['good'] & self.mas['poor'] & self.sprit['good'], self.out['decent'])
        self.rule4 = ctrl.Rule(self.rele['good'] & self.mas['average'] & self.sprit['poor'], self.out['poor'])
        self.rule5 = ctrl.Rule(self.rele['good'] & self.mas['average'] & self.sprit['average'], self.out['average'])
        self.rule6 = ctrl.Rule(self.rele['good'] & self.mas['average'] & self.sprit['good'], self.out['good'])
        self.rule7 = ctrl.Rule(self.rele['good'] & self.mas['good'] & self.sprit['poor'], self.out['mediocre'])
        self.rule8 = ctrl.Rule(self.rele['good'] & self.mas['good'] & self.sprit['average'], self.out['decent'])
        self.rule9 = ctrl.Rule(self.rele['good'] & self.mas['good'] & self.sprit['good'], self.out['excellent'])

        self.rule10 = ctrl.Rule(self.rele['average'] & self.mas['poor'] & self.sprit['poor'], self.out['dismal'])
        self.rule11 = ctrl.Rule(self.rele['average'] & self.mas['poor'] & self.sprit['average'], self.out['poor'])
        self.rule12 = ctrl.Rule(self.rele['average'] & self.mas['poor'] & self.sprit['good'], self.out['average'])
        self.rule13 = ctrl.Rule(self.rele['average'] & self.mas['average'] & self.sprit['poor'], self.out['poor'])
        self.rule14 = ctrl.Rule(self.rele['average'] & self.mas['average'] & self.sprit['average'], self.out['mediocre'])
        self.rule15 = ctrl.Rule(self.rele['average'] & self.mas['average'] & self.sprit['good'], self.out['decent'])
        self.rule16 = ctrl.Rule(self.rele['average'] & self.mas['good'] & self.sprit['poor'], self.out['poor'])
        self.rule17 = ctrl.Rule(self.rele['average'] & self.mas['good'] & self.sprit['average'], self.out['average'])
        self.rule18 = ctrl.Rule(self.rele['average'] & self.mas['good'] & self.sprit['good'], self.out['good'])

        self.rule19 = ctrl.Rule(self.rele['poor'] & self.mas['poor'] & self.sprit['poor'], self.out['dismal'])
        self.rule20 = ctrl.Rule(self.rele['poor'] & self.mas['poor'] & self.sprit['average'], self.out['dismal'])
        self.rule21 = ctrl.Rule(self.rele['poor'] & self.mas['poor'] & self.sprit['good'], self.out['dismal'])
        self.rule22 = ctrl.Rule(self.rele['poor'] & self.mas['average'] & self.sprit['poor'], self.out['dismal'])
        self.rule23 = ctrl.Rule(self.rele['poor'] & self.mas['average'] & self.sprit['average'], self.out['dismal'])
        self.rule24 = ctrl.Rule(self.rele['poor'] & self.mas['average'] & self.sprit['good'], self.out['mediocre'])
        self.rule25 = ctrl.Rule(self.rele['poor'] & self.mas['good'] & self.sprit['poor'], self.out['dismal'])
        self.rule26 = ctrl.Rule(self.rele['poor'] & self.mas['good'] & self.sprit['average'], self.out['poor'])
        self.rule27 = ctrl.Rule(self.rele['poor'] & self.mas['good'] & self.sprit['good'], self.out['average'])

        self.space_ctrl = ctrl.ControlSystem(
            [self.rule1, self.rule2, self.rule3, self.rule4, self.rule5, self.rule6, self.rule7, self.rule8, self.rule9,
             self.rule10, self.rule11, self.rule12, self.rule13, self.rule14, self.rule15, self.rule16, self.rule17,
             self.rule18, self.rule19, self.rule20, self.rule21, self.rule22, self.rule23, self.rule24, self.rule25,
             self.rule26, self.rule27])
        self.score = ctrl.ControlSystemSimulation(self.space_ctrl, cache=False)     # ToDo: Cache -> schöner lösen

        # Boundaries
        # ToDo: Falls Varianz zu gering ist, Grenzen auf 0 und 1 setzen,
        #  sonst Materialverfügbarkeit ungleich behandelt, obwohl sie etwa gleich
        if verf_max/verf_min < 2:
            self.verf_min = 0
            self.verf_max = 1
        else:
            self.verf_min = verf_min
            self.verf_max = verf_max

        # Auflösung
        self.resolution = resolution
        # Achsen der Kennfelder
        self.t_n_map = np.linspace(0, 1, _item_count(self.resolution))
        self.delt_map = np.linspace(0, 1, _item_count(self.resolution))
        self.verf_map = np.linspace(0, 1, _item_count(self.resolution))
        self.bes_map = np.linspace(0, 1, _item_count(self.resolution))
        self.mas_map = np.linspace(0, 1, _item_count(self.resolution))
        self.sprit_map = np.linspace(0, 1, _item_count(self.resolution))
        self.rele_map = np.linspace(0, 1, _item_count(self.resolution))
        # Kennfelder
        size = len(np.linspace(0, 1, _item_count(self.resolution)))
        self.out_sub_1_map = np.zeros([size, size])
        self.out_sub_2_map = np.zeros([size, size])
        self.score_map = np.zeros([size, size, size])
        # self.sprit_data = []
        # self.material_data = []
        # self.main_data = []
        # self.out_sub_1_map = []
        # self.out_sub_2_map = []
        # self.score_map = []
        # # Interpolations-Objekte
        # self.main = None
        # self.sub2 = None
        # self.sub1 = None

        if load_map:
            self.load_maps_from_npy()

    def calculate_score(self, t_n, delta_v, bes, verf, mas):
        """
        Bewertung bestimmen für gegebenen Asteroidenwechsel
        :param t_n: Tank nach dem Wechsel
        :param delta_v: Spritverbrauch für Wechsel
        :param bes: Bestand des Materials vom Zielasteroiden
        :param verf: Verfügbarkeit des Materials vom Zielasteroid
        :param mas: Masse des Zielasteroiden
        :return: Bewertung des Asteroidenwechsels
        """
        # Skalierung der Verfügbarkeit
        verf = _transform(verf, self.verf_min, self.verf_max)

        # Subsystem 1 - Sprit
        self.sub_sys.input['Tank nach Wechsel'] = t_n
        self.sub_sys.input['Spritverbrauch'] = delta_v
        self.sub_sys.compute()
        sprit = self.sub_sys.output['Ausgang Subsystem 1']
        # return sprit    # ToDo: Nur zum Testen eingefügt
        # Subsystem 2 - Material
        self.sub_sys_2.input['Bestand des Materials'] = bes
        self.sub_sys_2.input['Verfügbarkeit des Materials'] = verf
        self.sub_sys_2.compute()
        rele = self.sub_sys_2.output['Ausgang Subsystem 2']
        # Hauptsystem - Score
        self.score.input['Masse'] = mas
        self.score.input['Güte vom Spritverbrauch'] = sprit
        self.score.input['Relevanz des Materials'] = rele
        self.score.compute()
        
        return self.score.output['Güte des Asteroids']

    def creat_score_map(self):
        """
        Bestimmt das zum Fuzzy-System gehörige Kennfeld
        :param: resolution: 0.01 (1m Elemente für Main), 0.02 (125k Elemente), 0.025 (64k Elemente), 0.05 (8k Elemente);
            für 1/resolution sollte ein Integer rauskommen;
            Auflösung des Kennfelds, wenn nichts übergeben = Auflösung des Systems
        :return:
        """
        #####################
        # Subsystem 1 - Sprit
        #####################
        # Map füllen
        for m in range(len(self.t_n_map)):
            for n in range(len(self.delt_map)):
                # ToDo: Noch eine bessere Lösung finden - Unschön, genauso unschön ist: flush_after_run=item_count**
                self.sub_sys.input['Tank nach Wechsel'] = self.t_n_map[m]
                self.sub_sys.input['Spritverbrauch'] = self.delt_map[n]
                self.sub_sys.compute()
                # self.sprit_data.append([t_n_map[m], delt_map[n]])
                # self.out_sub_1_map.append(self.sub_sys.output['Ausgang Subsystem 1'])
                self.out_sub_1_map[m, n] = self.sub_sys.output['Ausgang Subsystem 1']
        print("Kennfeld für Sprit fertig")
        ########################
        # Subsystem 2 - Material
        ########################
        # Map füllen
        for m in range(len(self.bes_map)):
            for n in range(len(self.verf_map)):
                # ToDo: Noch eine bessere Lösung finden - Unschön, genauso unschön ist: flush_after_run=item_count**
                self.sub_sys_2.input['Bestand des Materials'] = self.bes_map[m]
                self.sub_sys_2.input['Verfügbarkeit des Materials'] = self.verf_map[n]
                self.sub_sys_2.compute()
                # self.material_data.append([bes_map[m], verf_map[n]])
                # self.out_sub_2_map.append(self.sub_sys_2.output['Ausgang Subsystem 2'])
                self.out_sub_2_map[m, n] = self.sub_sys_2.output['Ausgang Subsystem 2']
        print("Kennfeld für Material fertig")
        #############
        # Hauptsystem
        #############
        # Map füllen
        for m in range(len(self.mas_map)):
            for n in range(len(self.sprit_map)):
                for k in range(len(self.rele_map)):
                    self.score.input['Masse'] = self.mas_map[m]
                    self.score.input['Güte vom Spritverbrauch'] = self.sprit_map[n]
                    self.score.input['Relevanz des Materials'] = self.rele_map[k]
                    self.score.compute()
                    # self.main_data.append([mas_map[m], sprit_map[n], rele_map[k]])
                    # self.score_map.append(self.score.output['Güte des Asteroids'])
                    self.score_map[m, n, k] = self.score.output['Güte des Asteroids']
        print("Hauptkennfeld fertig")
        ############
        # Speichern
        ############
        self.save_maps_to_npy()

    def calculate_score_by_map(self, t_n, delta_v, bes, verf, mas):
        """
        Bewertung mittels Kennfeld bestimmen für gegebenen Asteroidenwechsel
        :param t_n: Tank nach dem Wechsel
        :param delta_v: Spritverbrauch für Wechsel
        :param bes: Bestand des Materials vom Zielasteroiden
        :param verf: Verfügbarkeit des Materials vom Zielasteroid
        :param mas: Masse des Zielasteroiden
        :return: Bewertung des Asteroidenwechsels
        """
        # Skalierung der Verfügbarkeit
        verf = _transform(verf, self.verf_min, self.verf_max)

        # Inputs an Auflösung anpassen
        t_n = _fit_to_resolution(t_n, self.resolution)
        delta_v = _fit_to_resolution(delta_v, self.resolution)
        bes = _fit_to_resolution(bes, self.resolution)
        verf = _fit_to_resolution(verf, self.resolution)
        mas = _fit_to_resolution(mas, self.resolution)

        # Subystem 1 - Sprit
        ind_t_n = np.argwhere(self.t_n_map == t_n)[0][0]
        ind_delt = np.argwhere(self.delt_map == delta_v)[0][0]
        sprit = _fit_to_resolution(self.out_sub_1_map[ind_t_n, ind_delt], self.resolution)
        # Subsystem 2 - Material
        ind_bes = np.argwhere(self.bes_map == bes)[0][0]
        ind_verf = np.argwhere(self.verf_map == verf)[0][0]
        rele = _fit_to_resolution(self.out_sub_1_map[ind_bes, ind_verf], self.resolution)
        # Hauptsystem
        ind_mas = np.argwhere(self.mas_map == mas)[0][0]
        ind_sprit = np.argwhere(self.sprit_map == sprit)[0][0]
        ind_rele = np.argwhere(self.rele_map == rele)[0][0]

        return self.score_map[ind_mas, ind_sprit, ind_rele]

    def save_maps_to_npy(self):
        """
        Speichert die Kennfelder der Subsysteme in die Dateien:
        out_sub_1_map.npy
        out_sub_2_map.npy
        score_map.npy
        :return:
        """
        if self.out_sub_1_map is not None and self.out_sub_2_map is not None and self.score_map is not None:
            # np.save('sprit_data.npy', self.sprit_data)
            # np.save('material_data.npy', self.material_data)
            # np.save('main_data.npy', self.main_data)
            np.save('out_sub_1_map.npy', self.out_sub_1_map)
            np.save('out_sub_2_map.npy', self.out_sub_2_map)
            np.save('score_map.npy', self.score_map)
        else:
            raise ValueError("Kennfelder müssen erst erzeugt werden")

    def load_maps_from_npy(self):
        """
        Lädt die Kennfelder aus den entsprechenden Dateien.
        Gibt eine Fehlermeldung, falls Dateien noch nicht erzeugt wurden
        :return:
        """
        try:
            # self.sprit_data = np.load('sprit_data.npy')
            # self.material_data = np.load('material_data.npy')
            # self.main_data = np.load('main_data.npy')
            self.out_sub_1_map = np.load('out_sub_1_map.npy')
            self.out_sub_2_map = np.load('out_sub_2_map.npy')
            self.score_map = np.load('score_map.npy')
        except FileNotFoundError:
            raise FileNotFoundError("Kennfelder noch nicht erzeugt, oder Dateien gelöscht")


    def plot(self):
        """
        Plottet Fuzzy-Kennfelder anhand der erstellten Maps
        :return:
        """
        fig = plt.figure(figsize=(12, 18))

        # Subsystem 1 - Sprit
        # Inputs festlegen
        t_n_test = np.arange(0, 1.1, 0.1)
        delt_test = np.arange(0, 1.1, 0.1)
        x_sub1, y_sub1 = np.meshgrid(t_n_test, delt_test, indexing='ij')
        out_sub1_test = np.zeros_like(x_sub1)
        # Auswerten
        for m in range(0, len(t_n_test)):
            for n in range(0, len(delt_test)):
                self.sub_sys.input['Tank nach Wechsel'] = t_n_test[m]
                self.sub_sys.input['Spritverbrauch'] = delt_test[n]
                self.sub_sys.compute()

                out_sub1_test[m, n] = self.sub_sys.output['Ausgang Subsystem 1']
        # Plotten
        subplot = 321
        ax1 = fig.add_subplot(subplot, projection='3d')
        surf = ax1.plot_surface(x_sub1, y_sub1, out_sub1_test, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
        plt.xlabel("Tank nach Wechsel")
        plt.ylabel("Delta V")
        plt.title("Subsystem Sprit")

        # Subsystem 2 - Material
        bes_test = np.arange(0, 1.1, 0.1)
        verf_test = np.linspace(self.verf_min, self.verf_max, 11)
        x_sub2, y_sub2 = np.meshgrid(bes_test, verf_test, indexing='ij')
        out_sub2_test = np.zeros_like(x_sub2)
        # Auswerten
        for m in range(0, len(bes_test)):
            for n in range(0, len(verf_test)):
                self.sub_sys_2.input['Bestand des Materials'] = bes_test[m]
                self.sub_sys_2.input['Verfügbarkeit des Materials'] = verf_test[n]
                self.sub_sys_2.compute()

                out_sub2_test[m, n] = self.sub_sys_2.output['Ausgang Subsystem 2']
        # Plotten
        subplot = 322
        ax2 = fig.add_subplot(subplot, projection='3d')
        surf = ax2.plot_surface(x_sub2, y_sub2, out_sub2_test, rstride=1, cstride=1, cmap='viridis',
                                linewidth=0.4, antialiased=True)
        plt.xlabel("Bestand")
        plt.ylabel("Verfügbarkeit")
        plt.title("Subsystem Material")

        # Hauptsystem
        mas_test = np.linspace(0, 1, 4)
        # Wertebereich von Güte des Sprits:
        sprit_test = np.linspace(out_sub1_test.min(), out_sub1_test.max(), 11)
        rele_test = np.linspace(out_sub2_test.min(), out_sub2_test.max(), 11)
        x, y = np.meshgrid(sprit_test, rele_test, indexing='ij')
        # Speicher für Minimum und Maximum
        out_min = 1
        out_max = 0
        # Auswertung
        for i in range(0, len(mas_test)):
            out = np.zeros_like(x)
            for m in range(0, len(sprit_test)):
                for n in range(0, len(rele_test)):
                    self.score.input['Masse'] = mas_test[i]
                    self.score.input['Güte vom Spritverbrauch'] = sprit_test[m]
                    self.score.input['Relevanz des Materials'] = rele_test[n]
                    self.score.compute()

                    out[m, n] = self.score.output['Güte des Asteroids']

            # Maximum und Minimum bestimmen
            if out.min() < out_min:
                out_min = out.min()
            if out.max() > out_max:
                out_max = out.max()

            # Subplot generieren
            if i == 0:
                subplot = 323
                ax3 = fig.add_subplot(subplot, projection='3d')  # subplot,
                surf = ax3.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                        linewidth=0.4, antialiased=True)
            elif i == 1:
                subplot = 324
                ax4 = fig.add_subplot(subplot, projection='3d')
                surf = ax4.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                        linewidth=0.4, antialiased=True)
            elif i == 2:
                subplot = 325
                ax5 = fig.add_subplot(subplot, projection='3d')
                surf = ax5.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                        linewidth=0.4, antialiased=True)
            elif i == 3:
                subplot = 326
                ax6 = fig.add_subplot(subplot, projection='3d')
                surf = ax6.plot_surface(x, y, out, rstride=1, cstride=1, cmap='viridis',
                                        linewidth=0.4, antialiased=True)
            plt.xlabel("Bewertung Sprit")
            plt.ylabel("Materialrelevanz")
            mas_now = mas_test[i]
            plt.title(f'Masse = {mas_now:.2}')

        # Einstellung Plot Darstellung
        # Blickwinkel auf 3D-Plots
        ax1.view_init(20, 120)
        ax1.set_zlim(0, 1)
        ax2.view_init(20, 70)
        ax2.set_zlim(0, 1)
        ax3.view_init(15, 190)
        ax3.set_zlim(0, 1)
        ax4.view_init(15, 190)
        ax4.set_zlim(0, 1)
        ax5.view_init(15, 190)
        ax5.set_zlim(0, 1)
        ax6.view_init(15, 190)
        ax6.set_zlim(0, 1)

        plt.subplots_adjust(left=0.065, bottom=0.065, right=0.935, top=0.885, wspace=0.3, hspace=0.5)
        plt.show()

        # Subsystem 1
        print(f'Ausgabewerte des Sprit-Subsystems: {out_sub1_test.min():.2} '
              f'bis {out_sub1_test.max():.2}')
        # Subsystem 2
        print(f'Ausgabewerte des Material-Subsystems: {out_sub2_test.min():.2} '
              f'bis {out_sub2_test.max():.2}')
        # Hauptsystem
        print(f'Ausgabewerte des Hauptsystems: {out_min:.2} '
              f'bis {out_max:.2}')
