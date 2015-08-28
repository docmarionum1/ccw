#python census.py /scratch/share/pvarsh/lidar/rasters/empire_state_bbl_5000 bblh.json census.csv jobs.jpg home.jpg
import sys, json, csv
from os import path
import shapefile
import numpy as np
import Image
from matplotlib import cm

raster = np.load(path.join(sys.argv[1], 'raster.npy'))
#with open(path.join(sys.argv[1], 'registration.txt')) as f:
#    coords = f.read()
#    reg = {'x': float(coords.split(',')[1]), 'y': float(coords.split(',')[0])}
    
with open(sys.argv[2]) as f:
    bblmap = json.load(f)
    
census = {}

with open(sys.argv[3], 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[2] != '' and row[3] != '':
            census[row[0]] = [float(row[2]), float(row[3])]
            
jraster = np.zeros((5000,5000))
hraster = np.zeros((5000,5000))
for i in range(raster.shape[0]):
    for j in range(raster.shape[1]):
        id = raster[i][j]
        if str(id) not in bblmap:
            continue
        b, l, h = bblmap[str(id)]
        bbl = '1' + str(b).zfill(5) + str(l).zfill(4)
        if bbl in census:
            jraster[i][j] = census[bbl][0]
            hraster[i][j] = census[bbl][1]
            
print jraster.max(), jraster.min()
print hraster.max(), hraster.min()

np.save('jraster.npy', jraster)
np.save('hraster.npy', hraster)
        
def createImage(raster, name):
    raster[raster>np.percentile(raster, 95)] = np.percentile(raster, 95)
    raster /= raster.max()
    im = Image.fromarray(np.uint8(cm.gist_earth(raster)*255))
    im.save(name)
    
createImage(jraster, sys.argv[4])
createImage(hraster, sys.argv[5])