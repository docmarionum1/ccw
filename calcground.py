#python calcground.py /scratch/share/pvarsh/lidar/rasters/empire_state_5000/raster.npy /scratch/share/pvarsh/lidar/rasters/empire_state_bbl_5000/raster.npy
import numpy as np
import sys

hraster = np.load(sys.argv[1])
braster = np.load(sys.argv[2])

braster[braster == 0] = 1
braster[braster > 1] = 0

graster = hraster * braster
graster = graster[graster != 0]
graster = graster[~np.isnan(graster)]
print graster.mean()