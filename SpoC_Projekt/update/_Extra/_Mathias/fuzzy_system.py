import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from scipy.interpolate import LinearNDInterpolator

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
    def __init__(self, verf_min, verf_max, resolution=0.01):
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

        # Fields
        self.resolution = resolution
        self.t_n_map = np.linspace(0, 1, _item_count(self.resolution))
        self.delt_map = np.linspace(0, 1, _item_count(self.resolution))
        self.verf_map = np.linspace(0, 1, _item_count(self.resolution))
        self.bes_map = np.linspace(0, 1, _item_count(self.resolution))
        self.mas_map = np.linspace(0, 1, _item_count(self.resolution))
        self.sprit_map = np.linspace(0, 1, _item_count(self.resolution))
        self.rele_map = np.linspace(0, 1, _item_count(self.resolution))
        self.out_sub_1_map = np.zeros((len(self.t_n_map), len(self.delt_map)))
        self.out_sub_2_map = np.zeros((len(self.verf_map), len(self.bes_map)))
        self.score_map = np.zeros((len(self.mas_map), len(self.sprit_map), len(self.rele_map)))

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
                self.out_sub_1_map[m, n] = self.sub_sys.output['Ausgang Subsystem 1']
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
                self.out_sub_2_map[m, n] = self.sub_sys_2.output['Ausgang Subsystem 2']
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
                    self.score_map[m, n, k] = self.score.output['Güte des Asteroids']

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
        # ToDo: griddata verwenden für Interpolation
        # ToDo: self.out_sub_1_map.reshape(1)
        # interp = LinearNDInterpolator(list(zip(self.t_n_map, self.delt_map)), self.out_sub_1_map)
        #
        # return interp(t_n, delta_v)

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
            np.save('out_sub_1_map.npy', self.out_sub_1_map)
            np.save('out_sub_2_map.npy', self.out_sub_2_map)
            np.save('score_map.npy', self.score_map)
        else:
            print("Kennfelder müssen erst erzeugt werden")

    def load_maps_from_npy(self):
        """
        Lädt die Kennfelder aus den entsprechenden Dateien.
        Gibt eine Fehlermeldung, falls Dateien noch nicht erzeugt wurden
        :return:
        """
        try:
            self.out_sub_1_map = np.load('out_sub_1_map.npy')
            self.out_sub_2_map = np.load('out_sub_2_map.npy')
            self.score_map = np.load('score_map.npy')
        except FileNotFoundError:
            print("Kennfelder noch nicht erzeugt, oder Dateien gelöscht")


    def plot_by_map(self):
        """
        Plottet Fuzzy-Kennfelder anhand der erstellten Maps
        :return:
        """
        # Überprüfen, ob Kennfeld schon geladen, wenn Nein, dann versuchen es zu laden, ansonsten Neues erstellen
        # if self.out_sub_1_map is None or self.out_sub_2_map is None or self.score_map is None:
        #     try:
        #         self.load_maps_from_npy()
        #     except:
        #         self.creat_score_map()
        pass
