import random

import numpy as np
from pykep import phasing
import copy
import SpoC_Constants as SpoC

from SpoC_Constants import dict_asteroids, DV_per_propellant, T_DAUER

##############################################
# Statische Funktionen für die Branch-Klassen
##############################################
def calc_candidate_ids(branch, materials):
    """
    Bestimmt Asteroiden, die als Kandidaten infrage kommen.
    Also die noch nicht besucht wurden und eins der gewünschten Materialien besitzen
    :param branch: Pfad, für den gesucht wird
    :param materials: Materialien, die gesucht werden
    :return: IDs der Kandidaten
    """
    if isinstance(materials, int):
        materials = [materials]

    return [asteroid_id for asteroid_id, values in zip(dict_asteroids.keys(), dict_asteroids.values())
            if values[-1] in materials and not branch.is_visited(asteroid_id)]


class Seed:
    # Konstanten initialisieren
    if dict_asteroids == {}:
        SpoC.initialize()
    ##############################
    # Methoden und Objektattribute
    ##############################
    def __init__(self, asteroid_id):
        """
        Objekt zum Speichern des ersten ASteroids
        :type asteroid_id:         int
        :param asteroid_id:        initialer Asteroid
        """
        self.asteroid_id = asteroid_id
        # Initiale Parameter für Start
        self.t_arr = 0.0
        self.step_score = 0.0
        self.branch_score_yet = 0.0
        self.bestand = [0.0, 0.0, 0.0, 1.0]
        self.t_opt = 0.0

    def __str__(self):
        return f"Startasteroid:{self.asteroid_id}"

    def get_step_count(self):
        """
        Initialer Asteroid => Step-Count  = 0
        :return: 0
        """
        return 0

    def get_branch_score(self):
        """
        Gibt den Branch-Score, also den Mittelwert der Step-Scores, für den erweiterten Branch zurück
        :return: Branch-Score des erweiterten Branches
        """
        return self.branch_score_yet

    def is_visited(self, asteroid_id):
        """
        Bestimmt, ob Asteroid vom gesamten Branch bereits besucht wurde
        :param asteroid_id: Asteroid-ID
        :return: Boolean, ob besucht oder nicht besucht
        """
        return asteroid_id == self.asteroid_id

    def get_result_vectors(self):
        """
        Gibt Ausgangspunkt für Lösungsvektoren zurück. t_m ist noch unbekannt und im kommenden Schritt gespeichert
        :return: res_a, res_t_arr, res_t_m
        """
        return [], [self.asteroid_id], [self.t_arr]

    def get_start_asteroid(self):
        return self.asteroid_id

    def print_summary(self):
        print("Wir sind nicht sehr weit gekommen")

    def print(self):
        print(f"Startasteroid:{self.asteroid_id}")

    ################################# Bestimmen der neuen möglichen Schritte #################################
    def _sort_material_types(self):
        sort_items = enumerate(self.bestand[:3])
        sorted_material = sorted(sort_items, key=lambda item: item[1])
        sorted_material_types = []
        sorted_materials = []
        for i, x in sorted_material:
            sorted_material_types.append(i)
            sorted_materials.append(x)
        return sorted_material_types, sorted_materials

    def _get_cluster_case(self, sprit_bei_start):
        """
        Bestimmt den Cluster-Case
        :param: sprit_bei_start: Füllstand des Tanks beim Start zum neuen Asteroiden
        :return: Array von Material-Typ-Arrays für Clusterbildung
        """
        # Materialtypen nach Bestand sortieren (ohne Sprit)
        sorted_material_types, sorted_materials = self._sort_material_types()
        # Fallunterscheidung
        if self.t_arr > T_DAUER-100:   # Letzer Asteroid
            cluster_iteration = [[sorted_material_types[0]], [sorted_material_types[1], sorted_material_types[2], 3]]
        else:
            if sprit_bei_start < 0.3:       # Tanken fast leer
                cluster_iteration = [[3]]
            elif sprit_bei_start < 0.6:     # Tank halbvoll
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
        :return: Asteroid-IDs der Nachbarasteroiden
        """
        candidates_id = calc_candidate_ids(self, materials)
        candidates = [SpoC.get_asteroid(asteroid_id) for asteroid_id in candidates_id]

        if not candidates:
            print(f"Keine Asteroiden mit den Materialien {materials} mehr vorhanden.")
            return []
        knn = phasing.knn(candidates, self.t_arr + self.t_opt, 'orbital', T=30) # ToDo T lässt sich auch anders wählen
        _, neighb_idx, _ = knn.find_neighbours(SpoC.get_asteroid(self.asteroid_id),
                                                             query_type='ball', r=radius)
        neighb_idx = list(neighb_idx)

        # Prüfen, dass Cluster wie gewollt:
        neighb_id = [candidates_id[index] for index in neighb_idx if candidates_id[index] != self.asteroid_id]

        # Testverfahren ToDo auskommentieren
        # print(f"Cluster wurde für die Materialien {materials} gebildet.")
        assert self._control_cluster_materials(neighb_id, materials), \
            f"Expected: {materials}, got {np.unique([SpoC.get_asteroid_material(asteroid_id) for asteroid_id in neighb_id])}"

        return neighb_id

    def _control_cluster_materials(self, neighb_id, materials):
        for asteroid_id in neighb_id:
            if SpoC.get_asteroid_material(asteroid_id) not in materials:
                return False
        return True

    def _calc_sprit_bei_start(self):
        """
        Berechnet den minimalen Tankfüllstand beim Start vom Asteroiden
        :return:
        """
        # Limit nach abbau, es werden mindestens 70 % abgebaut
        if SpoC.get_asteroid_material(self.asteroid_id) == 3:
            return SpoC.get_abbau_menge(self.bestand[3],
                                        SpoC.get_asteroid_mass(self.asteroid_id),
                                        SpoC.get_asteroid_material(self.asteroid_id),
                                        0.7 * self.t_opt)
        else:
            return self.bestand[-1]

    def get_next_possible_steps(self):
        """
        Bestimmt die Menge von Asteroiden, die für Expand-Schritt verwendet werden sollen.
        - Cluster gewinnen
        - Durch Cluster iterieren: siehe Vorversion (Zeitoptimierung, Score, SCORE PFAD)
        - Prüfen, ob leere Menge, wenn ja Kandidaten erweitern und neu anfangen (Rekursion mit Hilfsfunktion?)
        :return: Liste von Dictionaries mit der Form {'last_t_m', 'dv', 'asteroid_2_id', 't_arr', 'step_score'}
        """
        # Prüfen, ob noch ein Schritt notwendig
        if T_DAUER-30 < self.t_arr:  # ToDo: Warum klappt es nicht mit -40?
            print("Letzter Asteroid")
            # self.visited[-1]['t_m'] = Branch.T_DAUER-self.visited[-1]['t_arr']
            raise StopIteration
        # Speicher für mögliche Schritte
        possible_steps = []
        masses = []
        # Sprit bei Start approximieren/nach oben abschätzen
        sprit_bei_start = self._calc_sprit_bei_start()
        # Cluster-Fall bestimmen
        cluster_iteration = self._get_cluster_case(sprit_bei_start)
        # Durch Fälle iterieren, bis possible_steps nicht leer & Massen > 0.5, oder Cluster_Iteration fertig
        for materials in cluster_iteration:
            # Cluster bilden für die Materialien aus materials
            neighbour_ids = self._get_cluster_by_material(materials)
            # Iteration durch Nachbar. Hinzufügen zu Menge, wenn erreichbar
            for asteroid_2_id in neighbour_ids:
                # Prüfen, dass Clusterbildung korrekt verlaufen ist
                assert SpoC.get_asteroid_material(asteroid_2_id) in materials, f"Asteroid 2 besitzt ein Material, das nicht gesucht wird"

                t_m_opt_, t_flug_min_dv_, dv_min_ = SpoC.time_optimize(SpoC.get_asteroid(self.asteroid_id),
                                                                      SpoC.get_asteroid_mass(self.asteroid_id),
                                                                      SpoC.get_asteroid_material(self.asteroid_id),
                                                                      SpoC.get_asteroid(asteroid_2_id),
                                                                      t_arr=self.t_arr,
                                                                      t_opt=self.t_opt,
                                                                      limit=sprit_bei_start)
                # Bewertung nur durchführen, wenn Asteroid auch erreichbar
                if (dv_min_ / DV_per_propellant) < sprit_bei_start:
                    # Bewertung des Asteroids und des Wechsels
                    score = SpoC.my_system.calculate_score(  # ToDo: Über Normierung des delta_v sprechen
                        # Tank nach Flug → dv muss normiert werden
                        t_n=(sprit_bei_start - (dv_min_/DV_per_propellant)),
                        delta_v=(dv_min_/3000),  # Diese Normierung in Ordnung? - Dachte ganz sinnvoll
                        bes=SpoC.norm_bestand(self.bestand, SpoC.get_asteroid_material(asteroid_2_id)), # , Branch.norm_material
                        verf=SpoC.verf[SpoC.get_asteroid_material(asteroid_2_id)],
                        mas=SpoC.get_asteroid_mass(asteroid_2_id))
                    # Alle Daten für Schritt speichern
                    possible_steps.append(
                        {'last_t_m': t_m_opt_,
                         'dv': dv_min_,
                         'asteroid_2_id': asteroid_2_id,
                         't_arr': self.t_arr + t_m_opt_ + t_flug_min_dv_,
                         'step_score': score}
                    )
                    masses.append(SpoC.get_asteroid_mass(asteroid_2_id))
            # Wenn possible_steps nicht mehr leer & Masse der möglichen Zielasteroiden größer 0.5
            # → Mögliche Schritte gefunden, kann weiter gehen
            if len(possible_steps) != 0:
                if max(masses) > 0.5:
                    break
        return possible_steps




# ToDo: Nachdem entschieden wurde, dass ein Branch-Objekt weitergeführt wird, muss das t_m des letzten angepasst werden
#   PROBLEM: Das t_m kann für verschiedene Ausführungen unterschiedlich sein!!!
#   => Es muss im aktuellen Branch das t_m vom letzten Asteroiden gespeichert werden
#   => Erstellen des finalen Branches: t_m des letzten Asteroiden wird nach dessen Ankunftszeit gewählt.
#       Keine Optimierung notwendig
# ToDo: Wird der Bestand, da als Referenz übergeben, auch bei den anderen Verändert? Wäre schlecht -> Deepcopy
class ExpandBranch(Seed):
    def __init__(self, origin_branch, last_t_m, dv, asteroid_id, t_arr, step_score):
        """
        Objekt, zum Speichern des Expand-Schrittes im Beam-Search-Algorithmus.
        Speichert nur eine Referenz des zu erweiternden Branches, sowie den möglichen Expand-Schritt.
        :param origin_branch: Ursprungs-Pfad
        :param asteroid_id: Asteroid-Id des Ziel-Asteroiden vom neuen Schritt
        :param t_arr: Ankunftszeit auf Ziel-Asteroiden
        :param step_score: Bewertung des Schritts zum Ziel-Asteroiden
        :return: Objekt, dass Schritt zu Ziel-Asteroiden beschreibt
        """
        super().__init__(asteroid_id)
        # super(Seed).__init__(asteroid_id)
        # Ursprungspfad
        self.origin_branch = origin_branch
        # Abbauzeit auf VORHERIGEM Asteroiden (muss, da Abzweigungen vom letzten Pfad sich in t_m unterscheiden können
        self.last_t_m = last_t_m
        # Bestand vor Abbau und Flug
        self.bestand = copy.deepcopy(self.origin_branch.bestand)
        # Bestand nach Abbau und Flug
        self.mine_and_travel(dv)
        # Parameter nach Schritt
        self.t_arr = t_arr
        self.step_score = step_score

        # Abbauzeit und Branch-Score bestimmen
        self.t_opt = SpoC.get_t_opt(self.asteroid_id)
        self.branch_score_yet = self.calc_branch_score()

    def __str__(self):
        print(self.origin_branch)
        return f"Abbauzeit auf Asteroiden {self.last_t_m:.0f}, \n" \
               f"Neuer Asteroid: {self.asteroid_id}, Material: {SpoC.get_asteroid_material(self.asteroid_id)}, \n" \
               f"Bestand: {self.bestand}"

    def is_visited(self, asteroid_id):
        """
        Prüft, ob Asteroid-ID die aktuelle Asteroid-ID ist und fragt, ob er zuvor besucht wurde
        :param asteroid_id: Asteroid-ID
        :return: Boolean, ob ID bereits besucht wurde
        """
        return self.asteroid_id == asteroid_id or self.origin_branch.is_visited(asteroid_id)

    def mine_and_travel(self,dv):
        """
        Bestimmt Bestand nach Abbau auf letztem Asteroiden und Flug zum neuen aktuellen Asteroiden
        :param dv: Spritverbrauch bei Flug zu aktuellem Asteroiden
        :return
        """
        # Abbau der Rohstoffe auf LETZTEM Asteroiden
        SpoC.abbau(self.bestand,
                   SpoC.get_asteroid_mass(self.origin_branch.asteroid_id),
                   SpoC.get_asteroid_material(self.origin_branch.asteroid_id),
                   self.last_t_m)
        # Spritverbrauch bei Flug
        self.bestand[3] -= dv/DV_per_propellant

    def get_step_count(self):
        """
        Gibt an, auf wievielter Schritt das ist.
        :return: Schritt-Anzahl
        """
        return 1 + self.origin_branch.get_step_count()

    def calc_branch_score(self):
        """
        Gibt den Branch-Score, also den Mittelwert der Step-Scores, für den erweiterten Branch zurück
        :return: Branch-Score des erweiterten Branches
        """
        assert self.get_step_count()>0, "Step-Count wird falsch bestimmt"
        return (self.origin_branch.get_step_count() * self.origin_branch.get_branch_score() + self.step_score) \
            /self.get_step_count()

    # def print_last_step(self):
    #     print(f"=================== Neuer Schritt =================== \n"
    #           f"Abbauzeit auf letztem Assteroiden:{self.last_t_m:.0f} Tage, \n"
    #           f"Neuer Asteroid:\n"
    #           f"ID {self.asteroid_id}, "
    #           f"Ankunftstag: {self.t_arr:.0f}, ",
    #           f"Material:{SpoC.get_asteroid_material(self.asteroid_id)}", "\n",
    #           f"Bestand bei Ankunft am neuen Asteroiden:", self.bestand)

    def get_guetemass(self):
        """
        Gibt aktuelles Gütemaß, also -(min(Bestand)) zurück.
        Gütemass wird entweder für kompletten Abbau des akutellen Asteroiden,
        oder Abbau, bis Zeit abgelaufen
        :return: Gütemaß
        """
        bestand = copy.deepcopy(self.bestand)
        SpoC.abbau(bestand,
                   SpoC.get_asteroid_mass(self.asteroid_id),
                   SpoC.get_asteroid_material(self.asteroid_id),
                   T_DAUER - self.t_arr)
        return bestand


    def get_result_vectors(self):
        """
        Gibt Lösungsvektoren bis zum aktuellen Stand zurück. Für t_m ist das nur bis zum letzten Asteroiden
        :return: res_a, res_t_arr, res_t_m
        """
        res_t_m, res_a, res_t_arr = self.origin_branch.get_result_vectors()
        # Abbauzeit auf letztem Asteroid
        res_t_m.append(self.last_t_m)
        # Neue Asteroid-ID
        res_a.append(self.asteroid_id)
        # Ankunftszeit auf neuem Asteroid
        res_t_arr.append(self.t_arr)
        return res_t_m, res_a, res_t_arr

    def get_result(self):
        """
        Gibt Lösungsvektoren bis zum aktuellen Schritt zurück
        wählt letztes t_m so, dass Expedition nach T_DAUER aufhört, falls Spanne > 60 => Fehler?
        :return: Ergebnis, dass sich aus Abfolge der im Expand-Schritt referenzierten Objekte ergibt
        """
        res_t_m, res_a, res_t_arr =  self.get_result_vectors()
        # Letzte Abbauzeit bestimmen
        res_t_m.append(T_DAUER - res_t_arr[-1])
        if res_t_m[-1] > 60.0:
            print("Auf letztem Asteroid gestrandet")

        return res_a, res_t_m, res_t_arr

    def get_start_asteroid(self):
        return self.origin_branch.get_start_asteroid()

    def print_step(self):
        """
        Gibt aktuellen Schritt aus
        :return:
        """
        print(f"Abbauzeit auf Asteroid {self.origin_branch.asteroid_id}:{self.last_t_m:.0f}, \n"
              f"Neuer Asteroid: {self.asteroid_id}, Material: {SpoC.get_asteroid_material(self.asteroid_id)}, \n"
              f"Bestand: {self.bestand}")

    def print_summary(self):
        """
        Gibt Zusammenfassung aus
        :return:
        """
        print("Zusammenfassung des Pfads:")
        print(f"Startasteroid:{self.get_start_asteroid()},"
              f"Mittlerer Step-Score:{self.get_branch_score()},"
              f"Gütemaß:{self.get_guetemass()}")

    def print(self):
        """
        Gibt gesamten Ablauf aus
        :return:
        """
        self.origin_branch.print()
        self.print_step()



######################################################
# Funktionen zur Ausführung von Beam-Search und Start
######################################################
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
                # step = {'last_t_m', 'dv', 'asteroid_2_id', 't_arr', 'step_score'}
                branch_expand_.append(ExpandBranch(origin_branch=branch,
                                                   last_t_m=step['last_t_m'],
                                                   dv=step['dv'],
                                                   asteroid_id=step['asteroid_2_id'],
                                                   t_arr=step['t_arr'],
                                                   step_score=step['step_score']))
                # ToDo: Methodenauswahl für Score-Berechnung:
                #  hier soll übergeben werden, welche Methode ausgewählt wird
                if analysis == 'branch':
                    score.append(branch_expand_[-1].get_branch_score())
                else:
                    score.append(branch_expand_[-1].step_score)

        branch_expand = np.concatenate((branch_expand, branch_expand_), axis=0)
        # score = np.concatenate((score, score_), axis=0)

    print("branch_expand length: ", len(branch_expand))

    # Beste Branches auswählen
    top_beta = []
    # Nach Score sortierte Index-Reihenfolge erstellen
    if beta < len(branch_expand):  # Kontrollieren, ob branch_expand lang genug, um beta-Beste zu finden
        idx = np.argpartition(score, -beta)[-beta:]  # performance better than with argsort(), returns array with indices
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
                start_branches.append(Seed(int(line[0])))
    elif method == 'examples':
        start_ids = [3622, 5384]
        # 3622 -> 2.38, 5384 -> 4.23
        for ID in start_ids:
            start_branches.append(Seed(ID))
    elif method == 'random':
        start_ids = random.choices(range(10000),k=50)
        for ID in start_ids:
            start_branches.append(Seed(ID))

    return start_branches

