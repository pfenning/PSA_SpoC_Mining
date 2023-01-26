import random
import numpy as np
from pykep import phasing
import pykep as pk
import copy

import SpoC_Constants as SpoC
from SpoC_Constants import dict_asteroids, DV_per_propellant, T_DAUER, T_START, verf, material_most_needed

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
    ##############################
    # Methoden und Objektattribute
    ##############################
    def __init__(self, asteroid_id, fuzzy=True):
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
        self.fuzzy=fuzzy

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
    def _sort_material_types(self, vector=None):
        if vector is None:
            vector = self.bestand[:3]
        sort_items = enumerate(vector)
        sorted_material = sorted(sort_items, key=lambda item: item[1])
        sorted_material_types = []
        sorted_materials = []
        for i, x in sorted_material:
            sorted_material_types.append(i)
            sorted_materials.append(x)
        return sorted_material_types, sorted_materials

    def _get_cluster_case(self, bestand_bei_start=None, bevorzugen=1.7, sprit_save=None):
        """
        Bestimmt den Cluster-Case
        :param bestand_bei_start:   (minimaler) Bestand bei Start
        :param sprit_save:          Wahl der Grenzen fürs Tanken
        :return: Array von Material-Typ-Arrays für Clusterbildung
        """
        if sprit_save is None:
            sprit_save = [0.2, 0.4]
        if bestand_bei_start is None:
            bestand_bei_start = self.bestand

        # Materialtypen nach Bestand sortieren (ohne Sprit)
        sorted_material_types, sorted_materials = self._sort_material_types(vector=bestand_bei_start[:3])
        sprit_bei_start = bestand_bei_start[3]

        # Fallunterscheidung
        if self.t_arr > T_DAUER-45:   # letzer Asteroid
            cluster_iteration = [[sorted_material_types[0]], [sorted_material_types[1], sorted_material_types[2], 3]]
        elif self.t_arr > T_DAUER-100 and sprit_bei_start > 0.4: # Vorletzter Asteroid
            cluster_iteration = [[sorted_material_types[0], sorted_material_types[1]], [sorted_material_types[2]], [3]]
        else:
            if sprit_bei_start < sprit_save[0]:       # Tanken fast leer
                cluster_iteration = [[3]]
            elif sprit_bei_start < sprit_save[1]:     # Tank halbvoll
                if bevorzugen * sorted_materials[0] < sorted_materials[1] \
                        and bevorzugen * sorted_materials[1] < sorted_materials[2]:
                    # geringste Verfügbarkeit, mittlere, häufigstes oder Sprit
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1]],
                                         [sorted_material_types[2], 3]]
                elif bevorzugen * sorted_materials[0] < sorted_materials[1]:
                    # geringste Verfügbarkeit, ansonsten Rest
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1], sorted_material_types[2], 3]]
                elif bevorzugen * sorted_materials[1] < sorted_materials[2]:
                    # beiden geringsten, ansonsten Rest
                    cluster_iteration = [sorted_material_types[:2],
                                         [sorted_material_types[2], 3]]
                elif bevorzugen * sorted_materials[0] < sorted_materials[2]:
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1], sorted_material_types[2], 3]]
                else:
                    cluster_iteration = [range(3), [3]]
            else:                           # Tank noch voll
                # if sorted_material_types[0] == material_most_needed:    # Sprit vorhanden → seltenstes Material suchen
                #     cluster_iteration = [[material_most_needed],
                #                          sorted_material_types[1:],
                #                          [3]]
                if bevorzugen * sorted_materials[0] < sorted_materials[1] \
                        and bevorzugen * sorted_materials[1] < sorted_materials[2]:
                    # geringste Verfügbarkeit, mittlere, häufigstes oder Sprit
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1]],
                                         [sorted_material_types[2]],
                                         [3]]
                elif bevorzugen * sorted_materials[0] < sorted_materials[1]:
                    # geringste Verfügbarkeit, ansonsten Rest
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1], sorted_material_types[2]],
                                         [3]]
                elif bevorzugen * sorted_materials[1] < sorted_materials[2]:
                    # beiden geringsten, ansonsten Rest
                    cluster_iteration = [sorted_material_types[:2],
                                         [sorted_material_types[2]],
                                         [3]]
                elif bevorzugen * sorted_materials[0] < sorted_materials[2]:
                    cluster_iteration = [[sorted_material_types[0]],
                                         [sorted_material_types[1], sorted_material_types[2]],
                                         [3]]
                else:
                    cluster_iteration = [range(3), [3]]

        return cluster_iteration

    def _get_cluster_by_material(self, materials, t_flug=15, knn_type=False, radius=3000, k=50):
        """
        Erstellt Cluster für aktuellen Asteroiden aus allen Asteroiden, die übergebene Materialien besitzen
        :param materials: int oder list of ints - Liste von Materialien, die geclustert werden sollen
        :param radius: Cluster-Radius
        :param t_flug: mittlere Flugzeit für Clusterbildung
        :return: Asteroid-IDs der Nachbarasteroiden
        """
        candidates_id = calc_candidate_ids(self, materials)
        candidates = [SpoC.get_asteroid(asteroid_id) for asteroid_id in candidates_id]

        if not candidates:
            # print(f"Keine Asteroiden mit den Materialien {materials} mehr vorhanden.")
            return []
        knn = phasing.knn(candidates, pk.epoch(T_START.mjd2000 + self.t_arr + self.t_opt), 'orbital', T=t_flug)
        if knn_type:
            _, neighb_idx, _ = knn.find_neighbours(SpoC.get_asteroid(self.asteroid_id), query_type='knn', k=k)
        else:
            _, neighb_idx, _ = knn.find_neighbours(SpoC.get_asteroid(self.asteroid_id), query_type='ball', r=radius)

        return [candidates_id[index] for index in list(neighb_idx) if candidates_id[index] != self.asteroid_id]

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

    def _current_material_is_needed(self):
        current_material = SpoC.get_asteroid_material(self.asteroid_id)
        # Sprit Asteroid
        if current_material == 3:
            return False # Wird in Time-Optimize gelöst
        # Material Asteroid
        rar_material = self._sort_material_types(verf)[0][0]
        return current_material == rar_material \
            or (1.5*self.bestand[current_material] < max(self.bestand[:3])) \
            or current_material == material_most_needed

    def get_next_possible_steps(self, fast=False, knn_type = False):
        """
        Bestimmt die Menge von Asteroiden, die für Expand-Schritt verwendet werden sollen.
        - Cluster gewinnen
        - Durch Cluster iterieren: siehe Vorversion (Zeitoptimierung, Score, SCORE PFAD)
        - Prüfen, ob leere Menge, wenn ja Kandidaten erweitern und neu anfangen (Rekursion mit Hilfsfunktion?)
        :return: Liste von Dictionaries mit der Form {'last_t_m', 'dv', 'asteroid_2_id', 't_arr', 'step_score'}
        """
        # Prüfen, ob noch ein Schritt notwendig
        if T_DAUER-45 < self.t_arr:
            # print("Letzter Asteroid")
            # self.visited[-1]['t_m'] = Branch.T_DAUER-self.visited[-1]['t_arr']
            raise StopIteration
        # Prüfen, ob Material des aktuellen Asteroiden wichtig ist
        needed = self._current_material_is_needed()
        # Modus für Entwicklung neuer Blatt-Knoten
        if fast:
            cluster_case = [0.25, 0.5]
            time_divider = 34
        else:
            cluster_case = [0.2, 0.4]
            time_divider = 45
        # Speicher für mögliche Schritte
        possible_steps = []
        masses = []
        # Sprit bei Start approximieren/nach oben abschätzen
        # sprit_bei_start = self._calc_sprit_bei_start()  # ToDo Ausweiten auf gesamten Bestand
        bestand_bei_start = self.bestand[:]
        SpoC.abbau(bestand_bei_start,  # Kopie der Liste Bestand
                   SpoC.get_asteroid_mass(self.asteroid_id),
                   SpoC.get_asteroid_material(self.asteroid_id),
                   0.7 * self.t_opt)
        # Cluster-Fall bestimmen
        cluster_iteration = self._get_cluster_case(bestand_bei_start, sprit_save=cluster_case)
        # Durch Fälle iterieren, bis possible_steps nicht leer & Massen > 0.5, oder Cluster_Iteration fertig
        for materials in cluster_iteration:
            if fast:
                if len(materials) == 1:
                    t_flug = 20
                    radius = 5000   # Wird gar nicht benötigt
                else:
                    t_flug = 10
                    radius = 5000   # Wird gar nicht benötigt
            else:
                if len(materials)==1:
                    t_flug = 20
                    radius = 5000
                else:
                    t_flug = 15
                    radius = 3000
            # Cluster bilden für die Materialien aus materials
            neighbour_ids = self._get_cluster_by_material(materials, t_flug=t_flug, radius=radius, knn_type=knn_type)
            # Iteration durch Nachbar. Hinzufügen zu Menge, wenn erreichbar
            for asteroid_2_id in neighbour_ids:
                t_m_opt_, t_flug_min_dv_, dv_min_ = SpoC.time_optimize(SpoC.get_asteroid(self.asteroid_id),
                                                                       SpoC.get_asteroid_mass(self.asteroid_id),
                                                                       SpoC.get_asteroid_material(self.asteroid_id),
                                                                       SpoC.get_asteroid(asteroid_2_id),
                                                                       t_arr=self.t_arr,
                                                                       t_opt=self.t_opt,
                                                                       limit=bestand_bei_start[3],
                                                                       needed=needed,
                                                                       time_divider=time_divider)
                # Bewertung nur durchführen, wenn Asteroid auch erreichbar
                if (dv_min_ / DV_per_propellant) < bestand_bei_start[3]:
                    if self.fuzzy:
                        # Bewertung des Asteroids und des Wechsels
                        score = SpoC.my_system.calculate_score(  # ToDo: Über Normierung des delta_v sprechen
                            # Tank nach Flug → dv muss normiert werden
                            t_n=(bestand_bei_start[3] - (dv_min_/DV_per_propellant)),
                            delta_v=(dv_min_/3000),  # Diese Normierung in Ordnung? - Dachte ganz sinnvoll
                            bes=SpoC.norm_bestand(self.bestand, SpoC.get_asteroid_material(asteroid_2_id)), # , Branch.norm_material
                            verf=SpoC.verf[SpoC.get_asteroid_material(asteroid_2_id)],
                            mas=SpoC.get_asteroid_mass(asteroid_2_id))
                    else:
                        score = 0.0
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
                # else:
                    # print(f"Für Materialien {materials} wurden nicht ausreichend Lösungen gefunden. Es wird weitergesucht.")
        return possible_steps




# Nachdem entschieden wurde, dass ein Branch-Objekt weitergeführt wird, muss das t_m des letzten angepasst werden
#   PROBLEM: Das t_m kann für verschiedene Ausführungen unterschiedlich sein!!!
#   => Es muss im aktuellen Branch das t_m vom letzten Asteroiden gespeichert werden
#   → Erstellen des finalen Branches: t_m des letzten Asteroiden wird nach dessen Ankunftszeit gewählt.
#       Keine Optimierung notwendig
# Wird der Bestand, da als Referenz übergeben, auch bei den anderen Verändert? Wäre schlecht -> Deepcopy
class ExpandBranch(Seed):
    def __init__(self, origin_branch, last_t_m, dv, asteroid_id, t_arr, step_score, fuzzy=True):
        """
        Objekt, zum Speichern des Expand-Schrittes im Beam-Search-Algorithmus.
        Speichert nur eine Referenz des zu erweiternden Branches, sowie den möglichen Expand-Schritt.
        :param origin_branch: Ursprungs-Pfad
        :param asteroid_id: Asteroid-Id des Ziel-Asteroiden vom neuen Schritt
        :param t_arr: Ankunftszeit auf Ziel-Asteroiden
        :param step_score: Bewertung des Schritts zum Ziel-Asteroiden
        :return: Objekt, dass Schritt zu Ziel-Asteroiden beschreibt
        """
        super().__init__(asteroid_id, fuzzy)
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
        if fuzzy:
            self.step_score = step_score
        else:
            self.step_score = self.calc_score(dv)

        # Abbauzeit und Branch-Score bestimmen
        self.t_opt = SpoC.get_t_opt(self.asteroid_id,
                                    prop_needed=(1.0 - self.bestand[3] if SpoC.get_asteroid_material(asteroid_id)==3
                                                 else None))
        self.branch_score_yet = self.calc_branch_score()

    def fh(self):
        return min(SpoC.get_asteroid_mass(self.asteroid_id), 1.0-self.bestand[-1])

    def calc_score(self, dv):
        # print("Ich wurde verwendet :D!")
        tof = self.t_arr - (self.last_t_m + self.origin_branch.t_arr)
        if SpoC.get_asteroid_material(self.asteroid_id) == 3:
            return -(tof + 30*self.fh())/(self.fh()-dv)
        else:
            return -(tof + self.t_opt + 80*dv)/SpoC.get_asteroid_mass(self.asteroid_id)


    def __str__(self):
        print(self.origin_branch)
        return f"Abbauzeit auf Asteroiden {self.last_t_m:.0f}, \n" \
               f"Flugzeit:{self.t_arr-self.origin_branch.t_arr-self.last_t_m}, \n" \
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
        return -min(bestand[:3])

    def get_score_by_branch_and_guete(self, norm_guete=8):
        return self.get_branch_score() - self.get_guetemass()/norm_guete


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
        res_t_m.append(T_DAUER - res_t_arr[-1] if T_DAUER - res_t_arr[-1] > 0 else 2.0)

        assert res_t_m[-1] > 0, "Letzte Abbauzeit wurde kleiner 0 gewählt!"

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
              f"Flugzeit:{self.t_arr-self.origin_branch.t_arr-self.last_t_m}, \n" 
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
              f"Gütemaß:{self.get_guetemass()},\n"
              f"Bestand:{self.bestand}")

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
def beam_search(branch_v, beta, analysis="step", fuzzy=True, fast=False, knn_type = False):
    """
    Übergeben wird ein Vektor, der die beta-Besten Branches beinhaltet aus dem vorherigen Iterationsschritt.
    Führt ausgehend davon die neuen möglichen Schritte aus und gibt davon die beta besten zurück.

    :param knn_type:    Ob Cluster mit knn gebildet werden (ansonsten Ball)
    :param fast:        Ob möglichst schnell geflogen werden soll
    :param fuzzy:       Ob Fuzzy als Bewertungsmethode verwendet wird
    :param branch_v:    Vektor mit bisherigen Branches
    :param beta:
    :param analysis:    Gibt die Art der Score-Bewertung an:
                            step: nur den Score des aktuellen steps
                            branch: Mittelwert des entstandenen Pfades
    :param method:      gibt die Methode an, mit welcher die Branches ausgewertet & -gewählt  werden
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
            next_possible_steps = branch.get_next_possible_steps(fast, knn_type)
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
                                                   step_score=step['step_score'], fuzzy=fuzzy))
                # ToDo: Methodenauswahl für Score-Berechnung:
                #  hier soll übergeben werden, welche Methode ausgewählt wird
                if analysis == 'branch':
                    score.append(branch_expand_[-1].get_branch_score())
                elif analysis == 'branch and guete':
                    score.append(branch_expand_[-1].get_score_by_branch_and_guete())
                else:
                    score.append(branch_expand_[-1].step_score)

        branch_expand = np.concatenate((branch_expand, branch_expand_), axis=0)
        # score = np.concatenate((score, score_), axis=0)

    # print("branch_expand length: ", len(branch_expand))

    # Beste Branches auswählen
    top_beta = []
    # Nach Score sortierte Index-Reihenfolge erstellen
    if beta < len(branch_expand):  # Kontrollieren, ob branch_expand lang genug, um beta-Beste zu finden
        idx = np.argpartition(score, -beta)[-beta:]  # performance better than with argsort(), returns array with indices
        for line in idx:
            top_beta.append(branch_expand[line])
    else:
        top_beta = branch_expand

    # print("beam search done, top-beta length: ", len(top_beta))

    return v_done, top_beta

def find_idx_start(data, intervall=0.01, method='mean semimajor', fuzzy=True, k=15, alpha=50):
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
                start_branches.append(Seed(int(line[0]), fuzzy=fuzzy))
    elif method == 'examples':
        start_ids = [2447] # [1446, 3622, 5384, 2257, 925, 2447]
        # 3622 -> 2.38, 5384 -> 4.23, 2257 -> 4.4, 1446 -> 7.99, 2447 -> 8.37
        for ID in start_ids:
            start_branches.append(Seed(ID))
    elif method == 'random':
        start_ids = random.choices(range(10000),k=k)
        for ID in start_ids:
            start_branches.append(Seed(ID,fuzzy=fuzzy))
    elif method == 'all':
        start_branches = np.reshape([Seed(asteroid_id) for asteroid_id in range(10000)],(int(10000/50),50))
    elif method == 'alles_clustern':
        asteroids = [dict_asteroids[line][0] for line in dict_asteroids]
        ##########################################################################
        # ITERATION VON CLUSTERN ALLER ASTEROIDEN FÜR VERSCHIEDENE STARTZEITEN
        ##########################################################################
        laenge_start_cl = []
        knn = phasing.knn(asteroids, SpoC.T_START, 'orbital', T=30)  # .mjd2000 + i
        for ast_id in dict_asteroids.keys():
            if SpoC.get_asteroid_material(ast_id) != 1 and SpoC.get_asteroid_material(ast_id) != 3:
                _, neighb_idx, _ = knn.find_neighbours(ast_id, query_type='ball', r=5000)
                neighb_idx = list(neighb_idx)
                hilfe = []
                for mat in neighb_idx:
                    if SpoC.get_asteroid_material(mat) == 1: hilfe.append(mat)
                laenge_start_cl.append(len(hilfe))  # [len(neighb_idx), ]
            else:
                laenge_start_cl.append(0)  # [len(neighb_idx), ]

        # print(laenge_start_cl)
        top_starts = np.argpartition(laenge_start_cl, -alpha)[-alpha:]
        start_branches = []
        for ID in top_starts:
            start_branches.append(Seed(ID))

    return start_branches

def find_min_material(data):
    """
    Berechnet die ursprüngliche Verfügbarkeit der Materialien
    """
    material = data[:,-1]
    mass = data[:,-2]
    verf = [0, 0, 0, 0]
    for i in range(0,len(material)):
        if material[i] == 0:
            verf[0] += mass[i]
        elif material[i] == 1:
            verf[1] += mass[i]
        elif material[i] == 2:
            verf[2] += mass[i]
        elif material[i] == 3:
            verf[3] += mass[i]
    min_mat = np.argmin(verf)
    return min_mat
