import numpy as np
import pykep as pk
from SpoC_Constants import T_DAUER, dict_asteroids, verf
import SpoC_Constants as SpoC
import copy
import unittest


class TestFunctions(unittest.TestCase):
    def test_dict_asteroids(self):
        # Variablen laden
        i = 0
        for asteroid_id, values in zip(dict_asteroids.keys(), dict_asteroids.values()):
            print(f"Asteroid ID:{asteroid_id}, Masse:{values[1]}, Material:{values[2]}")
            i += 1
            if i > 10:
                break

    def test_verf(self):
        print(verf)

    def test_get_dv(self):
        # Test, ob Spritverbrauch richtig berechnet wird
        pass

    def test_time_optimize(self):
        asteroid1_id = 8836
        asteroid2_id = 3774
        asteroid1, asteroid1_mas, asteroid1_mat = dict_asteroids[asteroid1_id]
        asteroid2 = dict_asteroids[asteroid2_id][0]
        t_m_min_dv, t_flug_min_dv, dv_min \
            = psa.time_optimize(asteroid1, asteroid1_mas, asteroid1_mat,
                                asteroid2,
                                t_arr=0.0, t_opt=asteroid1_mas*TestFunctions.TIME_TO_MINE_FULLY, propellant=1.0)
        print(f"Verweilzeit:{t_m_min_dv}, Flugzeit: {t_flug_min_dv}, DV:{dv_min}")

    def test_verfuegbarkeit(self):
        verf, norm_material = psa.verfuegbarkeit(data=TestFunctions.data)
        # Für den späteren Einsatz: (mass=Branch.dict_asteroids[-2], material=Branch.dict_asteroids[-1])
        print(f"Verfügbarkeit: {verf}")
        print(f"Maximales Gütemaß:{norm_material}")
        for expect, got in zip(verf, [0.42020501, 0.02968144, 0.45186633, 0.09824722]):
            self.assertAlmostEqual(expect,got,5)

