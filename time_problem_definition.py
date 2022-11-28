import numpy as np
from pymoo.core.problem import ElementwiseProblem

class TimeOptimizeWithHookeAndJeeves(ElementwiseProblem):

    def __init__(self, xl, xu):
        """ 
        Optimierungsproblem:
        Spritverbrauch soll minimiert werden
        Variablen dabei sind: Flugzeit T, Starttag t_start
        
        Weitere mögliche Ziele:
        Minimierung der Flugzeit,
        Minimierung der Abweichung: absolut(t_start - t_start_opt)


        Parameters:
        xl : np.array, float, int
            Lower bounds for the variables. if integer all lower bounds are equal.

        xu : np.array, float, int
            Upper bounds for the variable. if integer all upper bounds are equal.
         """
        super().__init__(n_var = 2, n_obj = 1, n_ieq_constr = 0, xl = xl, xu = xu)

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = 