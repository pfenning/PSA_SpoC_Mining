import numpy as np
import pykep as pk
from pykep import phasing

from _Extra._Mathias.fuzzy_system import FuzzySystem
import PSA_functions_v2 as psa


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
    data = np.loadtxt("SpoC_Datensatz.txt")
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
    del data

    #########
    # TIME
    #########

    # Startwerte
    t_start = 0

    #########
    # GÜTE
    #########
    verf = np.array([0.03, 0.4, 0.42, 0.15])  # ToDo: Verfügbarkeit berechnen

    my_system = FuzzySystem(verf.min(), verf.max(), resolution=0.02)

    ################
    # Branch Objekt
    ################
    def __init__(self, i_start):
        """
        Erzeugt einen ganz neuen Pfad ausgehend einem übergebenden Startasteroiden
        :param i_start: ID des Startasteroiden
        """
        self.steps = [{'id': i_start, 't_m': 0.0, 't_arr': 0.0, 'score next step': 0.0, 'branch score yet': 0.0}]
        self.not_visited = Branch.dict_asteroids.copy()     # Jedes Branch-Objekt hat eigene Visited-Asteroiden-Liste
        self.bestand = [0.0, 0.0, 0.0, 1.0]
        self.asteroid_1_id = self.steps[0]['id']
        self.asteroid_1_kp, self.asteroid_1_mas, self.asteroid_1_mat = self.not_visited[self.asteroid_1_id]
        self.t_opt = 0.0

    def update_current_asteroid(self):
        """
        Setzt ID, Planet-Objekt, Masse, Material und optimale Abbauzeit auf Werte zuletzt besuchten Asteroids
        :return:
        """
        self.asteroid_1_id = self.steps[-1]['id']
        self.asteroid_1_kp, self.asteroid_1_mas, self.asteroid_1_mat = self.not_visited[self.asteroid_1_id]
        # Abbauzeit für gesamte Masse bestimmen
        if self.asteroid_1_id == self.steps[0]['id']:  # bzw. i == 0
            self.t_opt = 0
        else:
            self.t_opt = 30 * self.asteroid_1_mas

    def creat_cluster_by_material(self, materials, radius=4000):
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

        knn = phasing.knn(candidates, self.steps[-1]['t_arr'] + self.t_opt, 'orbital', T=30)
        # neighb_inds = psa.clustering(knn, Branch.asteroids_kp, self.asteroid_1_id, radius)
        neighb, neighb_inds, neighb_dis = knn.find_neighbours(Branch.asteroids_kp[self.asteroid_1_id],
                                                              query_type='ball', r=radius)
        neighb_inds = list(neighb_inds)
        # ToDo: Eventuell knn anstatt ball?
        return [candidates_id[index] for index in neighb_inds if index is not self.asteroid_1_id]

    def





