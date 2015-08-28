import numpy as np
import Image
from matplotlib import cm
import sys

raster = np.load(sys.argv[1])
        

raster[raster>np.percentile(raster, 95)] = np.percentile(raster, 95)
raster /= raster.max()
im = Image.fromarray(np.uint8(cm.jet(raster)*255))
im.save(sys.argv[2])