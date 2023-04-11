#########1#########2#########3#########4#########5#########6#########7#########8
# function image2hist()
#
# This module (file) contains one function named image2hist().
# This function takes a geographic raster image and generates a 2-dimensional
# frequency histogram and returns a raster layer.
#
# This function was designed to be called by two different ArcGIS Python
# script tools that are executed from within ArcGIS Pro. These tools are
# part of the Histogram2D Toolbox.
#
# Arguments:
#   geoimg [Raster Dataset] = multiband image raster to be used to make 
#                             2-dimensional histogram
#   histlyrx [Layer File] = layer file to symbolize the histogram raster
#   xband [Long] = band number to appear on x-axis of histogram. The default
#                  is band 4 which is commonly the near IR band.
#   yband [Long] = band number to appear on y-axis of histogram. The default
#                  is band 3 which is commonly the blue band.
#
# March 2023
########1#########2#########3#########4#########5#########6#########7#########8

import arcpy
import numpy as np
import pandas as pd

def image2hist(geoimg, xband, yband):
    
    arcpy.AddMessage("Creating histogram...\n")

    # convert raster to NumPy array
    arr = arcpy.RasterToNumPyArray(geoimg)

    # combine the brightness values from the two bands with place shift (1000) to
    # retain individual band info, ie brightness values 129 and 253 become 129253.
    z = arr[yband-1].astype('uint32') + (1000*arr[xband-1].astype('uint32'))

    # from z, a 2D array, to 1D vector
    zvect = np.concatenate(z)
    # vector to dict
    zdict = {"2bandcode": zvect}
    # dict to pandas dataframe
    zdf = pd.DataFrame(zdict)

    # group by 2bandcode and summarize groups by count
    codetbl = zdf.groupby("2bandcode")['2bandcode'].count().reset_index(name="count")

    # decompose 2bandcode into the two brightness values
    codetbl['b1bv'] = (codetbl['2bandcode']/1000).astype(int)
    codetbl['b2bv'] = (codetbl['2bandcode'] - 1000*codetbl['b1bv']).astype(int)
    codetbl.drop('2bandcode', axis=1, inplace=True)

    # convert back to NumPy array
    codetbl_arr = codetbl.to_numpy()

    # initialize array to hold 2D histogram values
    hist2D_arr = np.zeros((256,256), dtype='uint32')
    # replace array values from records in codetbl
    rows = codetbl_arr[:,2]
    cols = codetbl_arr[:,1]
    values = codetbl_arr[:,0]
    hist2D_arr[rows, cols] = values

    # NumPyArrayToRaster()
    outRaster = arcpy.NumPyArrayToRaster(hist2D_arr, value_to_nodata=0)
  
    # return histogram raster
    return outRaster
