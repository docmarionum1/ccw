#python floorh.py /scratch/share/pvarsh/lidar/rasters/empire_state_5000/raster.npy /scratch/share/pvarsh/lidar/rasters/empire_state_bbl_5000/raster.npy bbl.json output.csv
import sys, json
from os import path
import numpy as np
import Image
from matplotlib import cm

step1 = 'step1.npy'
step2 = 'step2.npy'

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
                if not np.isnan(hraster[i][j]):
                    bblheights[bbl].append(hraster[i][j])

    np.save(step1, bblheights)
else:
    print "loading", step1
    bblheights = np.load(step1).item()

if not path.isfile(step2):
    with open(sys.argv[3]) as f:
        bbls = json.load(f)
        
    # Step 2 - calculate the "height" of each bbl
    with open(sys.argv[4], 'w') as f:
        for bbl in bblheights:
            heights = bblheights[bbl]
            heights = np.array(heights)
            heights = heights[heights>=heights.mean()]
            if str(bbl) in bbls:
                block, lot, floors = bbls[str(bbl)]
                h = np.percentile(heights, 75)
                bbls[str(bbl)].append(h)
                bbls[str(bbl)].append(h/floors if floors > 0 else 0)
                #f.write(',',join([block, lot, np.percentile(heights, 75)]) + '\n')
                
    np.save(step2, bbls)
else:
    print "loading", step2
    bbls = np.load(step2).item()

print bbls["389752"]

fraster = np.zeros((5000,5000))
for i in range(fraster.shape[0]):
    for j in range(fraster.shape[1]):
        if str(braster[i][j]) in bbls:
            bbl = str(braster[i][j])
            if not np.isnan(bbls[bbl][4]):
                fraster[i][j] = bbls[bbl][4]
print np.max(fraster)
fraster[fraster>np.percentile(fraster, 95)] = np.max(fraster)       
fraster /= np.max(fraster)
fraster *= 255
fraster = np.uint8(fraster)



im = Image.fromarray(np.uint8(cm.gist_earth(fraster)*255))
im.save('floorheights.jpg')