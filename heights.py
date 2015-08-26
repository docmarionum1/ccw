import sys
from os import path
import numpy as np

step1 = 'step1.npy'

hraster = np.load(sys.argv[1])
braster = np.load(sys.argv[2])


# Step 1 - get arrays of heights within the boundries of each bbl
if not path.isfile(step1):
    bblheights = dict()

    for i in range(braster.shape[0]):
        for j in range(braster.shape[1]):
            if braster[i][j] != 0:
                bbl = braster[i][j]
                if bbl not in bblheights:
                    bblheights[bbl] = []
                bblheights[bbl].append(hraster[i][j])

    np.save(step1, bblheights)
else:
    bblheights = np.load(step1).item()

print len(bblheights)
exit()

# Step 2 - calculate the "height" of each bbl
for bbl, heights in bblheights:
    heights = np.array(heights)
    heights = heights[heights>=heights.mean()]
    print bbl, heights.mean()