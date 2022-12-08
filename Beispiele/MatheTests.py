import numpy as np
# resF = np.array([[1,2, 3],[4, 5, 6]])
# weights = np.array([0.2, 0.4, 0.4])
#
# rank = sum(weights*resF[0])
#
# print(rank)

A = [1, 2, 3]
B = [4, 5, 6]
results = []
for i in range(0, len(A)):
    results.append([A[i], B[i]])

print(results)
