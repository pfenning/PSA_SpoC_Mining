import random

import numpy as np
import pykep as pk
from SpoC_Constants import T_DAUER, dict_asteroids, verf, TIME_TO_MINE_FULLY, data
import SpoC_Constants as SpoC
import copy
import unittest
from pykep import phasing
import time


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
            = SpoC.time_optimize(asteroid1, asteroid1_mas, asteroid1_mat,
                                asteroid2,
                                t_arr=0.0, t_opt=asteroid1_mas*TIME_TO_MINE_FULLY, limit=0.5)
        print(f"Verweilzeit:{t_m_min_dv}, Flugzeit: {t_flug_min_dv}, DV:{dv_min}")

    def test_clustering(self):
        # Cluster auf allen Asteroiden. Später nur die möglichen auswählen
        timer1 = time.perf_counter_ns()
        knn = phasing.knn([asteroid for asteroid, _, _ in dict_asteroids.values()], 0, 'orbital', T=30)
        _, neighb_idx, _ = knn.find_neighbours(SpoC.get_asteroid(2257), query_type='ball', r=5000)
        neighb_idx = list(neighb_idx)
        asteroid_id_list = [asteroid_id for asteroid_id in neighb_idx if SpoC.get_asteroid_material(asteroid_id) in [0, 2]]
        timer2 = time.perf_counter_ns()
        print(f"Zeit bei gesamter Betrachtung:{timer2-timer1}")

        # Cluster mit beschränkter Betrachtung
        timer1 = time.perf_counter_ns()
        candidates = [SpoC.get_asteroid(asteroid_id) for asteroid_id in range(5,9985)]
        knn = phasing.knn(candidates, 0, 'orbital', T=30)
        _, neighb_idx, _ = knn.find_neighbours(SpoC.get_asteroid(self.asteroid_id)
        timer2 = time.perf_counter_ns()
        print(f"Zeit bei gesamter Betrachtung:{timer2 - timer1}")

    def test_verfuegbarkeit(self):
        verf, norm_material = SpoC.verfuegbarkeit()
        # Für den späteren Einsatz: (mass=Branch.dict_asteroids[-2], material=Branch.dict_asteroids[-1])
        print(f"Verfügbarkeit: {verf}")
        print(f"Maximales Gütemaß:{norm_material}")
        for expect, got in zip(verf, [0.42020501, 0.02968144, 0.45186633, 0.09824722]):
            self.assertAlmostEqual(expect,got,5)

