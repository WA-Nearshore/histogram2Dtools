#########1#########2#########3#########4#########5#########6#########7#########8
# ArcGIS Toolbox scrip tool:  Polygon to Histgram 
#
# This script tool takes pixels from a polygon AOI within a 8-bit multiband 
# image and converts the pixels in the AOI to a 2-dimensional frequency 
# histogram. 
#
# If a map named 'Histogram' is present in the current ArcGIS Pro project,
# the new histogram raster is added to the map and symbolized as a mask.
# This mask is designed to overly on the histogram of the entire image 
# raster (not just the polygon AOI subset).
#
# Script tool parameters (set in ArcGIS tool user interface): 
#  geoimg [raster] = the input image, typically a multiband aerial photo.
#  polyAOI [polygon] = the polygon feature class or layer defining the AOI. This
#                      can be created on the fly by drawing polygons. 
#  masklyrx [layer] = layer file used for histogram mask 
#  xband [int] = the band number to appear on x-axis of histogram (default 4).
#  yband [int] = the band number to appear on y=axis of histogram (default 3). 
#
# March 2023
#########1#########2#########3#########4#########5#########6#########7#########8

import arcpy
from arcpy.sa import *
import image2hist

arcpy.AddMessage("Polygon to Histogram tool")

# get the parameter values from the tool user interface
geoimg = arcpy.GetParameterAsText(0)
polyAOI = arcpy.GetParameter(1)
xband = arcpy.GetParameter(2)
yband = arcpy.GetParameter(3)
masklyr = arcpy.GetParameter(4)

# extract the AOI pixels from the source image
arcpy.AddMessage("Extracting AOI from image...")
imgExtract = ExtractByMask(in_raster = geoimg, in_mask_data = polyAOI)

# create the 2-dimensional histogram as a raster layer
arcpy.AddMessage("Calling image2hist...")
AOIHistRaster = image2hist.image2hist(imgExtract, xband, yband) 

# write to gdb, same name as input image with '_hist' suffix
histRasterName = geoimg + '_AOI_hist' 
AOIHistRaster.save(histRasterName)

# Confirm if map named 'Histogram' is present in the current project
currProject = arcpy.mp.ArcGISProject("CURRENT")
histMapList = currProject.listMaps("Histogram")
if histMapList:
    arcpy.AddMessage("Histogram map is present.\n")
    histMap = histMapList[0]
    # add histogram raster to the map 'Histogram'
    histlyr = histMap.addDataFromPath(histRasterName)
    currProject.save()
    arcpy.AddMessage("New layer:  {0}".format(histlyr))
else:
    arcpy.AddError("No map named Histogram found.\n")
    histlyr = []

arcpy.AddMessage("Completed.\n")