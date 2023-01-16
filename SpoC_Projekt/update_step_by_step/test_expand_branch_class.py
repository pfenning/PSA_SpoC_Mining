import numpy as np
import unittest
from expand_branch_class import Seed, ExpandBranch, find_idx_start
from SpoC_Constants import T_DAUER, dict_asteroids, data, DV_per_propellant


class TestBranchClass(unittest.TestCase):
    def test_sort_material_types(self):
        branch = Seed(asteroid_id=0)
        # Teste Fall 1
        branch.bestand = [1, 2, 3, 0.2]
        sort = branch._sort_material_types()
        self.assertEqual(([0,1,2], [1,2,3]), branch._sort_material_types())
        # Teste Fall 2
        branch.bestand = [4, 1, 13, 1]
        self.assertEqual(([1, 0, 2], [1, 4, 13]), branch._sort_material_types())
        # Teste Fall 3
        branch.bestand = [12, 1, 5, 1]
        sort = branch._sort_material_types()
        self.assertEqual(([1, 2, 0], [1, 5, 12]), branch._sort_material_types())
        # Teste Fall 4
        branch.bestand = [13, 12, 1, 1]
        sort = branch._sort_material_types()
        self.assertEqual(([2, 1, 0], [1, 12, 13]), branch._sort_material_types())
        # Teste Fall 5
        branch.bestand = [1, 1, 1, 1]
        sort = branch._sort_material_types()
        self.assertEqual(([0, 1, 2], [1, 1, 1]), branch._sort_material_types())

    def test_get_cluster_case(self):
        # Mission fast beendet
        self._test_iteration(expected_iteration=[[1], [0, 2, 3]],
                             bestand=[1, 0, 2, 0.3],
                             t_arr=T_DAUER - 80,
                             sprit_bei_start=0.1)
        # Sprit fast leer
        self._test_iteration(expected_iteration=[[3]],
                             bestand=[1, 1, 1, 0.3],
                             t_arr=200,
                             sprit_bei_start=0.1)
        # ein Rohstoff wenig, Rest viel
        self._test_iteration(expected_iteration=[[1], [0, 2, 3]],
                             bestand=[3, 0.5, 3, 0.5],
                             t_arr=200,
                             sprit_bei_start=0.5)
    def _test_iteration(self, expected_iteration, bestand, t_arr, sprit_bei_start):
        branch = Seed(asteroid_id=0)
        branch.bestand = bestand
        branch.t_arr = t_arr
        cluster_iteration = branch._get_cluster_case(sprit_bei_start)
        for expected, got in zip(expected_iteration, cluster_iteration):
            self.assertEqual(expected, got)

    def test_is_visited(self):
        pass

    def test_calc_candidate_ids(self):
        pass

    def test_get_cluster_by_material(self):
        branch = Seed(asteroid_id=0)
        neighbour_ids = branch._get_cluster_by_material([3])
        materials = [dict_asteroids[asteroid_id][-1] for asteroid_id in neighbour_ids]
        self.assertTrue(len(materials) is not 0)
        self.assertTrue((3 in materials) and ((0 not in materials) or (1 not in materials) or (2 not in materials)))

        # Noch testen: Ob auch wirklich alle enthalten?
        # ToDo: Test, dass keine visited dabei

    def test_get_next_possible_steps(self):
        branch = Branch(i_start=0)
        branch.bestand[3] = 0.3

        possible_steps = branch.get_next_possible_steps()
        neighbour_mat = [dict_asteroids[step['step']['id']][-1] for step in possible_steps]
        self.assertTrue(0 not in neighbour_mat and 1 not in neighbour_mat and 2 not in neighbour_mat)

    def test_branch_creation(self):
        branch_v = find_idx_start(data=data,
                                  method='examples')
        expanded = []
        score = []
        branch = branch_v[0]
        for i in range(50):
            try:
                possible_steps = branch.get_next_possible_steps()
            except StopIteration:
                break
            else:
                if len(possible_steps) == 0:
                    print("Keine weiteren Schritte gefunden")
                    break
                for step in possible_steps:
                    expanded.append((ExpandBranch(origin_branch=branch,
                                                  last_t_m=step['last_t_m'],
                                                  dv=step['dv'],
                                                  asteroid_id=step['asteroid_2_id'],
                                                  t_arr=step['t_arr'],
                                                  step_score=step['step_score'])))
                    score.append(expanded[-1].get_score())
                branch = expanded[np.argmin(score)]
                # print(new_step.get_step_count())
        print(branch)

    def test_get_result(self):
        branch = []
        branch.append(Seed(0))
        my_fantasy_trip = [
            [60, 3000, 1, 200, 0.0],
            [60, 3000, 2, T_DAUER-41, 0.0]
        ]
        for last_t_m, dv, ID, t_arr, score in my_fantasy_trip:
            branch.append(ExpandBranch(branch[-1], last_t_m, dv, ID, t_arr, score))
        print(branch[-1])
        print(branch[-1].get_result())



    def test_find_idx_start(self):
        branch_v = find_idx_start(data=data,
                       method='examples')
        print(f"Länge:{len(branch_v)}")
        for branch in branch_v:
            print(f"Element:{print(branch)}")


    def test_find_best(self):
        # Einfacher Test, ob bester Branch ausgewählt wird
        # ToDo: Scheint aber beim richtigen Durchlauf nicht immer der Fall zu sein
        branch = []
        branch.append(Seed(0))
        my_fantasy_trip = [
            [60, 3000, 1, 200, 0.0],
            [60, 3000, 2, T_DAUER - 41, 0.0]
        ]
        for last_t_m, dv, ID, t_arr, score in my_fantasy_trip:
            branch.append(ExpandBranch(branch[-1], last_t_m, dv, ID, t_arr, score))

        beendete_branches= [branch[-1]] * 10
        guete_array = [1, 0, 3, 5, 10, 8, 9, 6, 4]
        for guete, my_branch in zip(guete_array, beendete_branches):
            my_branch.bestand[:3] = [guete]*3
        final_branch = beendete_branches[np.argmin([branch.get_guetemass() for branch in beendete_branches])]
        self.assertEqual(beendete_branches[4], final_branch)

