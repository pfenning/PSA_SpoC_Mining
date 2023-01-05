#BEAM SEARCH
from numpy import array
def beam_search(distances, beta):
    # dummy  structure represented by
    # visited vertices and the path length (so far),
    # traversed along each path.
    paths_so_far = [[list(), 0]]
    
    # Propagates through the neighbouring vertices tier by tier
    # (row by row). A vertex position is indicated by its
    # index in each row (dists).
    for idx, tier in enumerate(distances):
        if idx > 0:
            print(f'Paths kept after tier {idx-1}:')
            print(*paths_so_far, sep='\n')
        paths_at_tier = list()
        
        # Follows each path.
        for i in range(len(paths_so_far)):
            # Reads the current path and its length (sum of distances).
            path, distance = paths_so_far[i]
            
            # Extends the path for every possible neighboring vertex
            # at the current tier.
            for j in range(len(tier)):
                path_extended = [path + [j], distance + tier[j]]
                paths_at_tier.append(path_extended)
                
        # Sorts the newly generated paths by their length.
        # sorted - sorts iterable (paths) with a key distances/güte
        paths_ordered = sorted(paths_at_tier, key=lambda element: element[1])
        
        # The best 'beta' paths are preserved.
        paths_so_far = paths_ordered[:beta]
        print(f'\nPaths pruned/removed after tier {idx}: ')
        print(*paths_ordered[beta:], sep='\n')
        
    return paths_so_far


#TEST
#distances from each knoten starting on root
dists = [[0.3, 0.1, 0.2, 0.1, 0.6],
         [0.2, 0.4, 0.6, 0.8, 0.1],
         [0.7, 0.6, 0.5, 0.4, 0.7],
         [0.1, 0.8, 0.2, 0.7, 0.3]]
dists = array(dists)
# Calculates the best paths by applying a beam of width 'beta'.
best_beta_paths = beam_search(dists, 3)
# Prints the best 'beta' paths.
print('\nThe best \'beta\' paths:')
for beta_path in best_beta_paths:
    print(beta_path)