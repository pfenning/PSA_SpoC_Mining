import numpy as np
import matplotlib.pyplot as plt
import pykep as pk







    
def calc_prepared_material(asteroid_id, t):
    """
    - asteroid:        Aktueller Asteroid
    - t:               Verweildauer auf Asteroid1, bestimmt durch Zeitoptimierung

    """
    if asteroids[asteroid_id[:,-1].astype(int)] == 3:
        STORAGE[asteroids[asteroid_id[:,-1].astype(int)]] = np.minimum(1.0, t * asteroids[asteroid_id[:,-2]] / TIME_TO_MINE_FULLY)
    STORAGE[asteroids[asteroid_id[:,-1].astype(int)]] += t * asteroids[asteroid_id[:,-2]] / TIME_TO_MINE_FULLY       # pro Tag 1/30 abbaubar

    return (STORAGE)
# ==> ACHTUNG: Beim Propellant gibt es auch ein Maximum!! 










print(calc_Delta_V(data[0,0], data[1,0]))
# print(data[0,0])



