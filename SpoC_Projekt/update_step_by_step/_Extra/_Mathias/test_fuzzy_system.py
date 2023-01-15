import numpy as np

from fuzzy_system import FuzzySystem, _fit_to_resolution, _item_count, _transform
import unittest
import random

class TestFuzzy(unittest.TestCase):

    def test_fit_to_resolution(self):
        pass

    def test_item_count(self):
        pass

    def test_transform(self):
        pass

    def test_calculate_by_map(self):
        my_system = FuzzySystem(0.03, 0.4, resolution=0.01,load_map=True)
        t_n_list = random.choices(np.linspace(0,1,74), k=50)
        delt_v_list = random.choices(np.linspace(0, 1, 74), k=50)
        bes_list = random.choices(np.linspace(0, 1, 74), k=50)
        verf_list = random.choices(np.linspace(0.03, 0.4, 74), k=50)
        mas_list = random.choices(np.linspace(0, 1, 74), k=50)

        for t_n, delt_v, bes, verf, mas in zip(t_n_list, delt_v_list, bes_list, verf_list, mas_list):
            self.assertTrue(
                my_system.calculate_score_by_map(t_n, delt_v, bes, verf, mas) -
                my_system.calculate_score(t_n, delt_v, bes, verf, mas) <0.04,
                f"Expected:{my_system.calculate_score_by_map(t_n, delt_v, bes, verf, mas)},"
                f"Got:{my_system.calculate_score(t_n, delt_v, bes, verf, mas)}"
            )
