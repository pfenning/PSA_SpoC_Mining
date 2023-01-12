import numpy as np
import numpy as np
import pykep as pk
import PSA_functions_v3 as psa
from branch_class import Branch
import copy
import unittest


class TestBranchClass(unittest.TestCase):
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
    dict_asteroids = dict()  # "Beispiel Dictionary für neue Objekte"

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

    def test_sort_material_types(self):
        branch = Branch(i_start=0)
        # Teste Fall 1
        branch.bestand = [1, 1, 1, 0.3]
        sort = branch._sort_material_types()
        assert sort in [[0, 1, 2], [1, 0, 2]]
        # "Actual: " + str(sort) + "\n Expected: [0, 1, 2] or [1, 0, 2]"
        # Teste Fall 2
        branch.bestand = [4, 1, 13, 1]
        self.assertEqual([1, 0, 2], branch._sort_material_types())
        # Teste Fall 3
        branch.bestand = [13, 1, 13, 1]
        sort = branch._sort_material_types()
        assert sort in [[1, 0, 2], [1, 2, 0]]
            # "Actual: " + str(sort) + "\n Expected: [1, 0, 2] or [1, 2, 0]"
        # Teste Fall 4
        branch.bestand = [1, 1, 13, 1]
        sort = branch._sort_material_types()
        assert sort in [[0, 1, 2], [1, 0, 2]]
            # "Actual: " + str(sort) + "\n Expected: [0, 1, 2] or [1, 0, 2]"
        # Teste Fall 5
        branch.bestand = [1, 1, 1, 1]
        sort = branch._sort_material_types()
        assert sort in [[0, 1, 2], [1, 0, 2], [2, 0, 1], [2, 1, 0]]
            # "Actual: " + str(sort) + "\n Expected: [0, 1, 2] or [1, 0, 2] or [2, 0, 1] or [2, 1, 0]"

    def test_get_cluster_case(self):
        branch = Branch(i_start=0)
        # Teste Fall 1
        branch.bestand = [1, 1, 1, 0.3]
        branch.visited[-1]['t_arr'] = 200
        expected_iteration = [3]
        cluster_iteration = branch._get_cluster_case()
        self.assertEqual(expected_iteration, cluster_iteration)

        branch.visited[-1]['t_arr'] = 1750
        expected_iteration = range(4)
        cluster_iteration = branch._get_cluster_case()
        self.assertEqual(expected_iteration, cluster_iteration)

        # Teste Fall 2
        branch.bestand = [4, 1, 13, 1]
        expected_iteration = [1, 0, [2, 3]]
        cluster_iteration = branch._get_cluster_case()
        self.assertEqual(expected_iteration, cluster_iteration)
        # Teste Fall 3
        branch.bestand = [13, 1, 13, 1]
        expected_iteration = [1, [0, 2, 3]]
        cluster_iteration = branch._get_cluster_case()
        self.assertEqual(expected_iteration, cluster_iteration)
        # Teste Fall 4
        branch.bestand = [1, 1, 13, 1]
        expected_iteration = [[0, 1], [2, 3]]
        cluster_iteration = branch._get_cluster_case()
        self.assertEqual(expected_iteration, cluster_iteration)
        # Teste Fall 5
        branch.bestand = [1, 1, 1, 1]
        expected_iteration = range(4)
        cluster_iteration = branch._get_cluster_case()
        self.assertEqual(expected_iteration, cluster_iteration)

    def test_get_cluster_by_material(self):
        branch = Branch(i_start=0)
        neighbour_ids = branch._get_cluster_by_material(3)
        materials = [TestBranchClass.dict_asteroids[asteroid_id][-1] for asteroid_id in neighbour_ids]
        self.assertTrue(len(materials) is not 0)
        self.assertTrue((3 in materials) and ((0 not in materials) or (1 not in materials) or (2 not in materials)))

        # Noch testen: Ob auch wirklich alle enthalten?

    def test_get_next_possible_steps(self):
        branch = Branch(i_start=0)
        branch.bestand[3] = 0.3

        possible_steps = branch.get_next_possible_steps()
        neighbour_mat = [TestBranchClass.dict_asteroids[step['step']['id']][-1] for step in possible_steps]
        self.assertTrue(0 not in neighbour_mat and 1 not in neighbour_mat and 2 not in neighbour_mat)


