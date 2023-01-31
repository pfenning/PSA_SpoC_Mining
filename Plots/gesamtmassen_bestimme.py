from SpoC_Constants import data, dict_asteroids, MU_TRAPPIST
import numpy as np

mass_v = [0, 0, 0, 0]
material_count = [0,0,0,0]
for _,mass,mat in dict_asteroids.values():
    mass_v[mat] += mass
    material_count[mat] += 1

print(mass_v)
print(material_count)