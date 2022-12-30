import numpy as np
import numpy as np
import pykep as pk
import PSA_functions_v3 as psa
from branch_class import Branch
import copy
import unittest


class TestFunctions(unittest.TestCase):
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

    def test_get_dv(self):
        # Test, ob Spritverbrauch richtig berechnet wird
        pass

    def test_time_optimize(self):
        asteroid1_id = 8816
        asteroid2_id = 9090
        asteroid1, asteroid1_mas, asteroid1_mat = TestFunctions.dict_asteroids[asteroid1_id]
        asteroid2 = TestFunctions.dict_asteroids[asteroid2_id][0]
        t_m_min_dv, t_flug_min_dv, dv_min \
            = psa.time_optimize(asteroid1, asteroid1_mas, asteroid1_mat,
                                asteroid2,
                                t_arr=0.0, t_opt=asteroid1_mas*TestFunctions.TIME_TO_MINE_FULLY, propellant=1.0)
        print(f"Verweilzeit:{t_m_min_dv}, Flugzeit: {t_flug_min_dv}, DV:{dv_min}")

