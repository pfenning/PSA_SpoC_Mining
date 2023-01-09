import numpy as np
import pykep as pk
from pykep import phasing
import PSA_functions_v3 as psa
# import branch_class as branch

data = np.loadtxt("SpoC_Datensatz.txt")

semimajor = data[:,1]
mitte = np.mean(semimajor)
intervall = 0.01 * mitte
print(mitte, min(semimajor), max(semimajor), (mitte-intervall))

i_start = []
for line in data:
    if (line[-1] == 3) and ((mitte-intervall) <= line[1] < (mitte+intervall)):
        i_start.append(line[0])
    
print(len(i_start))

# for idx in i_start:
#     pass