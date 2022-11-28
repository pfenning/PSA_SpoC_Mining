import numpy as np


STORAGE= [10,2,4,6]


def calc_minimum():
    return(
        STORAGE.index(np.min(STORAGE))
    )

print(calc_minimum())