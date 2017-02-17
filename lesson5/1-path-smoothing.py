# Define a function smooth that takes a path as its input
# (with optional parameters for weight_data, weight_smooth,
# and tolerance) and returns a smooth path. The first and 
# last points should remain unchanged.
#
# Smoothing should be implemented by iteratively updating
# each entry in newpath until some desired level of accuracy
# is reached. The update should be done according to the
# gradient descent equations.
# -----------

from copy import deepcopy

def printpaths(path,newpath):
    for old,new in zip(path,newpath):
        print '['+ ', '.join('%.3f'%x for x in old) + \
               '] -> ['+ ', '.join('%.3f'%x for x in new) +']'

path = [[0, 0],
        [0, 1],
        [0, 2],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
        [4, 3],
        [4, 4]]

def smooth(path, weight_data = 0.5, weight_smooth = 0.1, tolerance = 0.000001):

    # Make a deep copy of path into newpath
    newpath = deepcopy(path)

    change = tolerance

    while change >= tolerance:
        change = 0
        for i in range(1, len(path) - 1):
            for j in range(len(path[0])):
                d1 = weight_data*(path[i][j] - newpath[i][j])
                d2 = weight_smooth*(newpath[i-1][j] + newpath[i+1][j] - 2*newpath[i][j])
                change += abs(d1 + d2)
                newpath[i][j] += d1 + d2
                
    
    return newpath 

printpaths(path,smooth(path))
