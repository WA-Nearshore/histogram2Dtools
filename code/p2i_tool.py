#########1#########2#########3#########4#########5#########6#########7#########8
# ArcGIS Toolbox scrip tool:  Polygon to Image 
#
# This script tool takes pixels from a polygon AOI within a 2-dimensional
# histogram raster and converts the pixels in the histogram AOI to the
# associated pixels in the original image. 
#
# The original image is asssumed to be 8 bit.
#
# Script tool parameters (set in ArcGIS tool user interface): 
#  hist2D [raster] = the 2-dimensional histogram previously made based on geoimg
#  polyAOI [polygon] = the polygon feature class or layer defining the AOI. This
#                      can be created on the fly by drawing polygons. 
#  geoimg [raster] = the input image, typically a multiband aerial photo.
#  xband [int] = the band number to appear on x-axis of histogram (default 4).
#  yband [int] = the band number to appear on y=axis of histogram (default 3). 
#
# April 2023
#########1#########2#########3#########4#########5#########6#########7#########8

import arcpy
from arcpy.sa import *
import numpy as np

arcpy.AddMessage("Polygon to Image tool")

# get the parameter values from the tool user interface
hist2D = arcpy.GetParameterAsText(0)
polyAOI = arcpy.GetParameter(1)
geoimg = arcpy.GetParameterAsText(2)
xband = arcpy.GetParameter(3)
yband = arcpy.GetParameter(4)

# extract the AOI pixels from the source histogram 
arcpy.AddMessage("Extracting AOI from histogram ...")
histAOIExtract = ExtractByMask(in_raster = hist2D, in_mask_data = polyAOI)

# create 256x256 rasters; one with row values and one with col values
arcpy.AddMessage("Creating row and col rasters...")
row_arr = np.indices((256,256))[0]
col_arr = np.indices((256,256))[1]
rowRast = arcpy.NumPyArrayToRaster(row_arr, value_to_nodata=0)
colRast = arcpy.NumPyArrayToRaster(col_arr, value_to_nodata=0)

# Use histogram AOI extract as mask to extract those pixels from row & col
# rasters. 
arcpy.AddMessage("Extracting from row and col rasters...")
rowAOIExtract = ExtractByMask(in_raster = rowRast, in_mask_data = histAOIExtract)
colAOIExtract = ExtractByMask(in_raster = colRast, in_mask_data = histAOIExtract)
# consolidate the two layers, displacing col values by x1000
rowColAOIExtract = colAOIExtract + 1000*rowAOIExtract

# convert to NumPy array, and then to 1D array of target brightness value codes
arcpy.AddMessage("Reduce extract pixels to 1D array...")
rowColAOIarr = arcpy.RasterToNumPyArray(in_raster = rowColAOIExtract)
bv_pair_vals = np.concatenate(rowColAOIarr)

# construct paths to the two selected bands of the original image
geoimage = Raster(geoimg,True)
imgPath = geoimage.catalogPath
xbandpath = f"{imgPath}\Band_{xband}"
ybandpath = f"{imgPath}\Band_{yband}"

arcpy.AddMessage("x: {0}".format(xbandpath))
arcpy.AddMessage("y: {0}".format(ybandpath))

# consolidate the two image bands into one raster layer with x values x1000
imgCodes = ybandpath + 1000*xbandpath

# Find pixels in original image where codes match those from histogram AOI
imgMask = ExtractByAttributes(in_raster = imgCodes,
                              where_clause = "Value IN bv_pair_vals")   

# copy (?) result to lowest practical bit depth; recode to 0/1




