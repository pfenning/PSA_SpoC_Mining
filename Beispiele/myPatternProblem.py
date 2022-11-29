from pymoo.algorithms.soo.nonconvex.pattern import PatternSearch
from pymoo.core.problem import ElementwiseProblem
from pymoo.problems.single import Himmelblau
from pymoo.optimize import minimize
import numpy as np

class MyPatternProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=2,
                         n_obj=1,
                         n_ieq_constr=0,
                         xl=np.array([-2,-2]),
                         xu=np.array([2,2]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = 100 * (x[0]**2 + x[1]**2)

        out["F"] = [f1]

# problem = Himmelblau()
problem = MyPatternProblem()

algorithm = PatternSearch()

res = minimize(problem,
               algorithm,
               verbose=False,
               seed=1)

print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))