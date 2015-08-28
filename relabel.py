# python relabel /scratch/share/pvarsh/lidar/rasters/empire_state_bbl_5000 scratch/share/pvarsh/lidar/mappluto/Manhattan/MNMapPLUTO out.json
import sys, json
from os import path
import shapefile
import numpy as np

X = 72
Y = 73
BOROUGH = 0
BLOCK = 1
LOT = 2
FLOORS = 42
FPM = .3048

boroughs = ['MN']

#BBL Raster
raster = np.load(path.join(sys.argv[1], 'raster.npy'))
with open(path.join(sys.argv[1], 'registration.txt')) as f:
    coords = f.read()
    reg = {'x': float(coords.split(',')[1]), 'y': float(coords.split(',')[0])}

#MapPLUTO Shapefile
sf = shapefile.Reader(sys.argv[2])
records = sf.records()

#output
bbls = {}

for record in records:
    if record[BOROUGH] in boroughs:
        x = int(record[X])
        y = int(record[Y])
        i = int((x - reg['x']) * FPM)
        j = int((reg['y'] - y) * FPM)
        if j >= 0 and j < raster.shape[0] and i >= 0 and i < raster.shape[1]:
            id = raster[j][i]
            if id > 0:
                if str(id) in bbls:
                    print "Warning, multiple hits on", id
                else:
                    bbls[str(id)] = [int(record[BLOCK]), int(record[LOT]), int(float(record[FLOORS]))]
            else:
                print "Warning, x/y missed for", record[BLOCK], record[LOT]

with open(sys.argv[3], 'w') as outfile:
    json.dump(bbls, outfile)