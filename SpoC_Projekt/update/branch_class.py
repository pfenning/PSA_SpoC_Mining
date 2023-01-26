import numpy as np
import pykep as pk
from pykep import phasing
import copy
from _Extra._Mathias.fuzzy_system import FuzzySystem
import PSA_functions_v4 as psa



class Branch:
    #########################
    # Static Class Constants
    #########################
    T_START = pk.epoch_from_iso_string("30190302T000000")  # Start and end epochs
    T_END = pk.epoch_from_iso_string("30240302T000000")
    T_DAUER = 1827
    G = 6.67430e-11  # Cavendish constant (m^3/s^2/kg)
    SM = 1.989e30  # Sun_mass (kg)
    MS = 8.98266512e-2 * SM  # Mass of the Trappist-1 star
    MU_TRAPPIST = G * MS  # Mu of the Trappist-1 star
    DV_per_propellant = 10000  # DV per propellant [m/s]
    TIME_TO_MINE_FULLY = 30  # Maximum time to fully mine an asteroid

    #################
    # ASTEROIDS:  Creating lists with indices of asteroids
    #################

    # Lists to be created
    asteroids_kp = []
    dict_asteroids = dict()     # "Beispiel Dictionary für neue Objekte"
    # Loading data as keplerian elements (planets) in an "array"
    data = np.loadtxt("candidates.txt")
    for line in data:
        p = pk.planet.keplerian(
            T_START,
            (
                line[1],
                line[2],
                line[3],
                line[4],
                line[5],
                line[6],
            ),
            MU_TRAPPIST,
            G * line[7],  # mass in planet is not used in UDP, instead separate array below
            1,  # these variable are not relevant for this problem
            1.1,  # these variable are not relevant for this problem
            "Asteroid " + str(int(line[0])),
            )
        asteroids_kp.append(p)
        dict_asteroids[int(line[0])] = [p, line[-2], int(line[-1])]  # Key = ID, Liste mit [Kaplerian, Masse, Material]
    # Putzen - wahrscheinlich nicht notwendig
    del p

    #########
    # GÜTE
    #########
    verf, norm_material = psa.verfuegbarkeit(data)
    # print(f"Verfügbarkeit der Materialien:{verf}")
    # print(f"Bestmögliches Gütemass:{norm_material}")
    my_system = FuzzySystem(verf.min(), verf.max(), resolution=0.02)

    ################
    # Branch Objekt
    ################
    def __init__(self, i_start):
        """
        Erzeugt einen ganz neuen Pfad ausgehend einem übergebenden Startasteroiden
        :param i_start: ID des Startasteroiden
        """
        self.visited = [{'id': i_start, 't_m': 0.0, 't_arr': 0.0, 'score last step': 0.0, 'branch score yet': 0.0}]
        # Jedes Branch-Objekt hat eigene Visited-Asteroiden-Liste
        self.not_visited = copy.deepcopy(Branch.dict_asteroids)
        self.bestand = [0.0, 0.0, 0.0, 1.0]
        self.sprit_bei_start = 1.0;
        self.asteroid_1_id = self.visited[0]['id']
        self.asteroid_1_kp, self.asteroid_1_mas, self.asteroid_1_mat = self.not_visited[self.asteroid_1_id]
        self.t_opt = 0.0

    def _update_current_asteroid(self):
        """
        Setzt ID, Planet-Objekt, Masse, Material und optimale Abbauzeit auf Werte zuletzt besuchten Asteroids
        :return:
        """
        self.asteroid_1_id = self.visited[-1]['id']
        self.asteroid_1_kp, self.asteroid_1_mas, self.asteroid_1_mat = Branch.dict_asteroids[self.asteroid_1_id]
        # Abbauzeit für gesamte Masse bestimmen
        if self.asteroid_1_id == self.visited[0]['id']:
            self.t_opt = 0
        else:
            self.t_opt = self.asteroid_1_mas*Branch.TIME_TO_MINE_FULLY

    def _sort_material_types(self):
        sort_items = enumerate(self.bestand[:3])
        sorted_material = sorted(sort_items, key=lambda item: item[1])
        sorted_material_types = []
        sorted_materials = []
        for i, x in sorted_material:
            sorted_material_types.append(i)
            sorted_materials.append(x)
        return sorted_material_types, sorted_materials

    def _get_cluster_case(self):
        """
        Bestimmt den Cluster-Case
        :return: Array von Material-Type-Arrays für Clusterbildung
        """
        # Materialtypen nach Bestand sortieren (ohne Sprit)
        sorted_material_types, sorted_materials = self._sort_material_types()
        # for value in sorted_materials:
        #     types = np.argwhere(self.bestand[:3] == value)
        #     for material_type in types:
        #         if material_type not in sorted_material_types:
        #             sorted_material_types.append(material_type)
        # sorted_material_types = [self.bestand[:3].index(value) for value in sorted_materials]
        # ToDo: Softe Grenze mit Berech Sprit zwischen 0.2 und 0.4, oder so, ansonsten gar kein Sprit?
        # Fallunterscheidung
        if self.visited[-1]['t_arr'] > Branch.T_DAUER-100:   # Letzer Asteroid
            cluster_iteration = [[sorted_material_types[0]], [sorted_material_types[1], sorted_material_types[2], 3]]
        else:
            if self.sprit_bei_start < 0.3:       # Tanken fast leer
                cluster_iteration = [[3]]
            elif self.sprit_bei_start < 0.6:     # Tank halbvoll
                if 3 * sorted_materials[0] < sorted_materials[1] and 3 * sorted_materials[1] < sorted_materials[2]:
                    # geringste Verfügbarkeit, mittlere, häufigstes oder Sprit
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1]],
                                         [sorted_material_types[2], 3]]
                elif 3 * sorted_materials[0] < sorted_materials[1]:
                    # geringste Verfügbarkeit, ansonsten Rest
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1], sorted_material_types[2], 3]]
                elif 3 * sorted_materials[1] < sorted_materials[2]:
                    # beiden geringsten, ansonsten Rest
                    cluster_iteration = [sorted_material_types[:2],
                                         [sorted_material_types[2], 3]]
                else:
                    cluster_iteration = [range(4)]
            else:                           # Tank noch voll
                if 3 * sorted_materials[0] < sorted_materials[1] and 3 * sorted_materials[1] < sorted_materials[2]:
                    # geringste Verfügbarkeit, mittlere, häufigstes oder Sprit
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1]],
                                         [sorted_material_types[2]],
                                         [3]]
                elif 3 * sorted_materials[0] < sorted_materials[1]:
                    # geringste Verfügbarkeit, ansonsten Rest
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1], sorted_material_types[2]],
                                         [3]]
                elif 3 * sorted_materials[1] < sorted_materials[2]:
                    # beiden geringsten, ansonsten Rest
                    cluster_iteration = [sorted_material_types[:2],
                                         [sorted_material_types[2]],
                                         [3]]
                else:
                    cluster_iteration = [range(3), [3]]

        return cluster_iteration

    def _get_cluster_by_material(self, materials, radius=5000):
        """
        Erstellt Cluster für aktuellen Asteroiden aus allen Asteroiden, die übergebene Materialien besitzen
        :param materials: int oder list of ints - Liste von Materialien, die geclustert werden sollen
        :param radius: Cluster-Radius
        :return: ASteroid-IDs der Nachbarasteroiden
        """
        if isinstance(materials, int):
            materials = [materials]

        candidates_id = [asteroid_id for asteroid_id, values in self.not_visited.items() if values[-1] in materials]
        candidates = [self.not_visited[asteroid_id][0] for asteroid_id in candidates_id]

        if not candidates:
            print(f"Keine Asteroiden mit den Materialien {materials} mehr vorhanden.")
            return []
        knn = phasing.knn(candidates, self.visited[-1]['t_arr'] + self.t_opt, 'orbital', T=30)
        # neighb_inds = psa.clustering(knn, Branch.asteroids_kp, self.asteroid_1_id, radius)
        neighb, neighb_inds, neighb_dis = knn.find_neighbours(Branch.asteroids_kp[self.asteroid_1_id],
                                                              query_type='ball', r=radius)
        neighb_inds = list(neighb_inds)
        # ToDo: Eventuell knn anstatt ball?

        # Prüfen, dass Cluster wie gewollt:
        neighb_id = [candidates_id[index] for index in neighb_inds if candidates_id[index] != self.asteroid_1_id]

        # Testverfahren ToDo auskommentieren
        # print(f"Cluster wurde für die Materialien {materials} gebildet.")
        assert self._control_cluster_materials(neighb_id, materials), \
            f"Expected: {materials}, Actual: {self._control_cluster_materials(neighb_id)}"

        return neighb_id

    def _control_cluster_materials(self, neighb_id, materials):
        for asteroid_id in neighb_id:
            if self.dict_asteroids[asteroid_id][-1] not in materials:
                return False
        return True

    def _calc_sprit_bei_start(self):
        """
        Berechnet den Sprit beim Start von Asteroid 1
        :return:
        """
        # Limit nach abbau, es werden mindestens 70 % abgebaut
        if self.asteroid_1_mat == 3:
            self.sprit_bei_start = psa.get_abbau_menge(self.bestand[-1], self.asteroid_1_mas, self.asteroid_1_mat, 0.7 * self.t_opt)
        else:
            self.sprit_bei_start = self.bestand[-1]

    def get_next_possible_steps(self):
        """
        Bestimmt die Menge von Asteroiden, die für Expand-Schritt verwendet werden sollen.
        - Cluster gewinnen
        - Durch Cluster iterieren: siehe Vorversion (Zeitoptimierung, Score, SCORE PFAD)
        - Prüfen, ob leere Menge, wenn ja Kandidaten erweitern und neu anfangen (Rekursion mit Hilfsfunktion?)
        :return: {'t_m': Verweilzeit auf aktuellem ASteroiden
                  'step': neue Zeile im Stil von Visited,
                  'dv': DV für Schritt}
        """
        # Prüfen, ob noch ein Schritt notwendig
        if Branch.T_DAUER-30 < self.visited[-1]['t_arr']:  # ToDo: Warum klappt es nicht mit -40?
            print("Letzter Asteroid")
            self.visited[-1]['t_m'] = Branch.T_DAUER-self.visited[-1]['t_arr']
            raise StopIteration
        # Update von Asteroid 1
        self._update_current_asteroid()
        # Speicher für mögliche Schritte
        possible_steps = []
        masses = []
        # ToDo: Sprit bei Start approximieren/nach unten abschätzen
        self._calc_sprit_bei_start()
        # Cluster-Fall bestimmen
        cluster_iteration = self._get_cluster_case()
        # Durch Fälle iterieren, bis possible_steps nicht leer & Massen > 0.5, oder Cluster_Iteration fertig
        for materials in cluster_iteration:
            # Cluster bilden für die Materialien aus materials
            neighbour_ids = self._get_cluster_by_material(materials)
            # Iteration durch Nachbar. Hinzufügen zu Menge, wenn erreichbar
            for asteroid_2_id in neighbour_ids:
                asteroid_2_kp, asteroid_2_mas, asteroid_2_mat = self.not_visited[asteroid_2_id]

                # Prüfen, dass Clusterbildung korrekt verlaufen ist
                assert asteroid_2_mat in materials, f"Asteroid 2 besitzt ein Material, das nicht gesucht wird"

                t_m_opt_, t_flug_min_dv_, dv_min_ = psa.time_optimize(self.asteroid_1_kp,
                                                                      self.asteroid_1_mas,
                                                                      self.asteroid_1_mat,
                                                                      asteroid_2_kp,
                                                                      t_arr=self.visited[-1]['t_arr'],
                                                                      t_opt=self.t_opt,
                                                                      limit=self.sprit_bei_start)
                # Bewertung nur durchführen, wenn Asteroid auch erreichbar
                if (dv_min_ / Branch.DV_per_propellant) < self.sprit_bei_start:
                    # Bewertung des Asteroids und des Wechsels
                    score = Branch.my_system.calculate_score(  # ToDo: Über Normierung des delta_v sprechen
                        # Tank nach Flug → dv muss normiert werden
                        t_n=(self.sprit_bei_start - (dv_min_ / Branch.DV_per_propellant)),
                        delta_v=(dv_min_ / 4000),  # Diese Normierung in Ordnung? - Dachte ganz sinnvoll
                        bes=psa.norm_bestand(self.bestand, asteroid_2_mat, Branch.norm_material),
                        verf=self.verf[asteroid_2_mat],
                        mas=asteroid_2_mas)
                    # Alle Daten für Schritt speichern
                    possible_steps.append(
                        {'t_m': t_m_opt_,
                         'step': {'id': asteroid_2_id,
                                  't_m': 0.0,
                                  't_arr': self.visited[-1]['t_arr']+t_m_opt_+t_flug_min_dv_,
                                  'score last step': score,
                                  'branch score yet': 0.0},
                         'dv': dv_min_}
                    )
                    masses.append(asteroid_2_mas)
            # Wenn possible_steps nicht mehr leer & Masse der möglichen Zielasteroiden größer 0.5
            # → Mögliche Schritte gefunden, kann weiter gehen
            if len(possible_steps) != 0:
                if max(masses) > 0.5:
                    break
        return possible_steps

    def _calculate_branch_score(self):
        self.visited[-1]['branch score yet'] = \
            ((len(self.visited)-1) * self.visited[-2]['branch score yet']
             + self.visited[-1]['score last step'])/len(self.visited)

    def new_step(self, t_m, step, dv):
        """
        Führt neuen Schritt aus:
        - berechnet t_m von aktuellem Asteroiden
        - fügt Asteroiden zu Visited hinzu
        - aktualisiert Bestand von Rohstoffen und Tank
        - entfernt aktuellen Asteroiden aus Not_Visited
        - berechnet Score des Pfades nach neuem Schritt
        :return:
        """
        self._update_current_asteroid()     # ToDo: Notwendig? - zurzeit sicher sein, dass asteroid_1 aktuell ist
        self.visited[-1]['t_m'] = t_m
        # Abbau des Rohstoffs von Asteroid 1:
        psa.abbau(self.bestand, self.asteroid_1_mas, self.asteroid_1_mat, t_m)
        # letzten Asteroid entfernen (nicht den neuen Asteroiden)
        self.not_visited.pop(self.asteroid_1_id)
        # Neuen Schritt hinzufügen
        self.visited.append(step)
        # Spritverbrauch des neuen Schritts abziehen
        self.bestand[-1] -= dv / Branch.DV_per_propellant
        # Branch-Score bestimmen
        self._calculate_branch_score()

    def print_last_step(self):
        print(f"=================== Neuer Schritt =================== \n"
              f"Abbauzeit auf letztem Assteroiden:{self.visited[-2]['t_m']:.0f} Tage, \n"
              f"Neuer Asteroid:\n"
              f"ID {self.visited[-1]['id']}, "
              f"Ankunftstag: {self.visited[-1]['t_arr']:.0f}, ",
              f"Material:{Branch.dict_asteroids[self.visited[-1]['id']][-1]}", "\n",
              f"Bestand bei Ankunft am neuen Asteroiden:", self.bestand)

    def get_score(self):
        """
        Gibt Score des letzten Schritts zurück
        :return: Score des letzten Schritts
        """
        return self.visited[-1]['score last step']

    def get_branch_score(self):
        """
                Gibt Mittelwert von allen Schritt_Scores als Bewertung des Pfades zurück
                :return: Bewertung des Pfades
                """
        return self.visited[-1]['branch score yet']

    def get_guetemass(self):
        """
        Gibt aktuelles Gütemaß, also -(min(Bestand)) zurück
        :return: Gütemaß
        """
        return -min(self.bestand[:3])

    def get_result(self):
        """
        Erstellt die Lösungsvektoren
        :return: ERG_a, ERG_t_m, ERG_t_arr
        """
        res_a = []
        res_t_m = []
        res_t_arr = []
        res_list = [[out for out in step.values()] for step in self.visited]
        for a, t_m, t_arr, _, _ in res_list:
            res_a.append(a)
            res_t_m.append(t_m)
            res_t_arr.append(t_arr)
        return res_a, res_t_m, res_t_arr

    def print(self):
        # print(self.visited)
        res_list = [[out for out in step.values()] for step in self.visited]
        for a, t_m, t_arr, _, _ in res_list:
            print(f'Asteroid ID:{a}, Ankunftszeit:{t_arr:.0f}, Verweildauer:{t_m:.0f}')

    def print_summary(self):
        print("Zusammenfassung des Pfads:")
        print(f"Startasteroid:{self.visited[0]['id']}, "
              f"Anzahl gemachter Schritte:{len(self.visited)},"
              f"Mittlerer Step-Score:{self.get_branch_score()},"
              f"Gütemaß:{self.get_guetemass()}")



def beam_search(branch_v, beta, analysis="step", method="Fuzzy"):
    """
    Übergeben wird ein Vektor, der die beta-Besten Branches beinhaltet aus dem vorherigen Iterationsschritt.
    Führt ausgehend davon die neuen möglichen Schritte aus und gibt davon die beta besten zurück.

    :param branch_v: Vektor mit bisherigen Branches
    :param beta:
    :param analysis: Gibt die Art der Score-Bewertung an:
                step: nur den Score des aktuellen steps
                branch: Mittelwert des entstandenen Pfades
    :param method: gibt die Methode an, mit welcher die Branches ausgewertet & -gewählt  werden
        default == Fuzzy
    :return: v_done: Beendete Vektorpfade
             v_continue: Branches, die weitergeführt werden können
    """
    v_done = []
    branch_expand = []
    score = []
    for branch in branch_v:
        branch_expand_ = []
        # score_ = []
        try:
            next_possible_steps = branch.get_next_possible_steps()
        except StopIteration:
            v_done.append(branch)
        else:
            for step in next_possible_steps:
                branch_expand_.append(copy.deepcopy(branch))
                branch_expand_[-1].new_step(step['t_m'], step['step'], step['dv'])
                # ToDo: Methodenauswahl für Score-Berechnung
                if analysis == 'branch':
                    score.append(branch_expand_[-1].get_branch_score())
                else:
                    score.append(branch_expand_[-1].get_score()) # hier soll übergeben werden, welche Methode ausgewählt wird
        
        branch_expand = np.concatenate((branch_expand, branch_expand_), axis=0)
        # score = np.concatenate((score, score_), axis=0)

    print("branch_expand length: ", len(branch_expand))

    # Beste Branches auswählen
    top_beta = []
    # Nach Score sortierte Index-Reihenfolge erstellen
    if beta < len(branch_expand): # Kontrollieren, ob branch_expand lang genug, um beta-Beste zu finden
        idx = np.argpartition(score, -beta)[-beta:]     # performance is better than with argsort(), returns an array with indices
        for line in idx:
            top_beta.append(branch_expand[line])
    else:
        top_beta = branch_expand

    print("beam search done, top-beta length: ", len(top_beta))

    return v_done, top_beta


def find_idx_start(data, intervall=0.01, method='mean semimajor'):
    '''
        Hier wird aus dem Datensatz ein Vektor mit möglichen Startasteroiden gebildet.
        Return:
            Ein Vektor der möglichen Start-Asteroiden als Branch-Objekte
                start_branches:     Vektor mit branches der Start-Asteroiden
    '''
    #### Auswahl des Start-Materials. Das kann durch Verfügbarkeit bestimmt werden! Optimalerweise max. Material --> Verf-Funktion benutzen
    start_branches = []
    # Erstellen des Vektors der möglichen Start-Asteroiden
    if method=='mean semimajor':
        mitte_semimajor = np.mean(data[:,1])
        grenze = intervall * mitte_semimajor
        for line in data:
            if (line[-1] == 3) and ((mitte_semimajor-grenze) <= line[1] < (mitte_semimajor+grenze)):
                start_branches.append(Branch(int(line[0])))
    elif method == 'examples':
        start_ids = [5384]
        # 3622 -> 2.38, 5384 -> 4.23
        for id in start_ids:
            start_branches.append(Branch(id))

    return start_branches








