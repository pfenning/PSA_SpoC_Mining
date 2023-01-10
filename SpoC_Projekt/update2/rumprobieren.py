import numpy as np
import copy

# a = [10,1,2,3]
# b1 = [4,5,6]
# b2 = [7,8,9]
# b3 = [10,11,12]

# c=[]
# i = 0
# while i < len(a):
#     if i == 0: b=b1
#     elif i==1: b=b2
#     elif i==2: b=b3
#     help = [a[i], b]

#     c.append([a[i], b])
#     i+=1


beta = 5
v_done = []

a = ['a','b','c','d','e','f','g']
next_possible_steps = np.array([0.5, 0.2])#,0.2,0.8] # next possible steps
branch_expand = np.array([0.5,0.2,0.4,0.1,0.5, 0.2])#,0.2,0.8] # branch expand schon nach auffüllen

branch_expand = np.concatenate((branch_expand, next_possible_steps), axis=0)

print(branch_expand)

# nr_poss_steps = len(next_possible_steps)
# idx_start = len(branch_expand) - len(next_possible_steps)

# branch = 0.5

# last_added_branches = branch_expand[-nr_poss_steps:]
# for check in last_added_branches : # die zuletzt hinzugefügten branchens
#     print(check)
#     idx = np.where(branch_expand==check)
#     print(idx[0])
#     branch_expand.pop(idx[0])
    # if check == branch:
    #     v_done.append(check)
    #     branch_expand.pop(check)
    #     idx_start = len(branch_expand) - nr_poss_steps
    #     idx = np.where(branch_expand==check)

# print(idx_start)


# if len(a) > beta:
#     idx = np.argpartition(b, -beta)[-beta:]       # performance is better than with argsort(), returns an array with indices    
#     top_beta = []
#     for line in idx:
#         top_beta.append(a[line])
# else:
#     beta_new = len(a)
#     idx = np.argpartition(b, -beta_new)[-beta_new:]       # performance is better than with argsort(), returns an array with indices    
#     top_beta = []
#     for line in idx:
#         top_beta.append(a[line])


# print(top_beta)






# Ausgesonderte Probe, ob Branch beendet!
        # # Probe, ob Pfad beendet:   Wenn ja, dann aus branch_expand und aus score rauslöschen!! (Index benutzen)
        # for check in branch_expand_ : # die zuletzt hinzugefügten branchens
        #     if check == branch:
        #         v_done.append(check)
        #         branch_expand_.pop(check)
        #         idx = np.where(branch_expand_==check)
        #         score_.pop()