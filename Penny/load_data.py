import os
import numpy as np

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'data/SpoC_Datensatz.txt')

data = np.loadtxt(filename)