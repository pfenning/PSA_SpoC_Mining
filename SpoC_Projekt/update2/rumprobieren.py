import numpy as np

a = [10,1,2,3]
b1 = [4,5,6]
b2 = [7,8,9]
b3 = [10,11,12]

c=[]
i = 0
while i < len(a):
    if i == 0: b=b1
    elif i==1: b=b2
    elif i==2: b=b3
    help = [a[i], b]

    c.append([a[i], b])
    i+=1

for line in a:
    print(line)
#     if line==1: b=b1
#     elif line==2: b=b2
#     elif line==3: b=b3

#     for line2 in b:
#         c.append()



# print(c[1][1][1])