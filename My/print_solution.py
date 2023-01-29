import numpy as np

solution = np.array([...])

# Solution.txt erstellen
with open("Solution.txt", "w") as output:
    output.write("[")
    for ele in solution:
        output.write(f"{ele}, ")
    output.write("]")
