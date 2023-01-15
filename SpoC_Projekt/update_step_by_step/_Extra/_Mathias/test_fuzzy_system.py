import numpy as np

from fuzzy_system import FuzzySystem, _fit_to_resolution, _item_count, _transform, _get_index
import unittest
import random

class TestFuzzy(unittest.TestCase):

    def test_fit_to_resolution(self):
        test_list = random.choices(np.linspace(0,1,74), k=50)
        for ele in test_list:
            self.assertAlmostEqual(round(ele,2), _fit_to_resolution(ele, 0.01))

    def test_item_count(self):
        self.assertEqual(4, _item_count(0.33))
        self.assertEqual(5, _item_count(0.25))
        self.assertEqual(101, _item_count(0.01))

    def test_transform(self):
        pass

    def test_get_index(self):
        vector = np.linspace(0,1,101)
        array = enumerate(vector)
        for i, a in array:
            self.assertEqual(i, _get_index(a,vector))

    def test_calculate_by_map(self):
        my_system = FuzzySystem(0.03, 0.4, resolution=0.01,load_map=True)
        t_n_list = random.choices(np.linspace(0,1,74), k=50)
        delt_v_list = random.choices(np.linspace(0, 1, 74), k=50)
        bes_list = random.choices(np.linspace(0, 1, 74), k=50)
        verf_list = random.choices(np.linspace(0.03, 0.4, 74), k=50)
        mas_list = random.choices(np.linspace(0, 1, 74), k=50)

        print(f"Sprit:{my_system.out_sub_1_map.min()} bis {my_system.out_sub_1_map.max()}")
        print(f"Material:{my_system.out_sub_2_map.min()} bis {my_system.out_sub_2_map.max()}")

        for t_n, delt_v, bes, verf, mas in zip(t_n_list, delt_v_list, bes_list, verf_list, mas_list):
            self.assertTrue(
                my_system.calculate_score_by_map(t_n, delt_v, bes, verf, mas) -
                my_system.calculate_score(t_n, delt_v, bes, verf, mas) <0.04,
                f"Expected:{my_system.calculate_score_by_map(t_n, delt_v, bes, verf, mas)},"
                f"Got:{my_system.calculate_score(t_n, delt_v, bes, verf, mas)}"
            )
