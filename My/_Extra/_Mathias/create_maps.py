from fuzzy_system import FuzzySystem


my_system = FuzzySystem(0.03, 0.4, resolution=0.01, load_map=False)
my_system.creat_score_map()