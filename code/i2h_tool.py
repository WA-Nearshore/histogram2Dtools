########1#########2#########3#########4#########5#########6#########7#########8
# ArcGIS Toolbox scrip tool:  Image to Histogram 
#
# Takes an image raster (geographic spatial dimensions) and converts to
# a 2D histogram with pixel frequencies in 2 specified bands (mathematical
# spatial dimensions - row/col brightness values).
#
# Common bands in input image: 1(red), 2(green), 3(blue), 4(near IR).
#
# This code is written to be called from an ArcGIS Toolbox, not to be used as
# a stand alone script. The actual histogram creation is done in a
# function that is called image2hist() and imported from a separate module. 
#
# Script tool parameters (set in ArcGIS tool user interface): 
#  geoimg [raster] = the input image, typically a multiband aerial photo.
#  histimg [raster] = the output histogram raster.
#  histlyrx [layer] = layer file with histogram raster symbology.
#  xband [int] = the band number to appear on x-axis of histogram (default 4).
#  yband [int] = the band number to appear on y=axis of histogram (default 3). 
#
# In addition there is a derived parameter that is specified with the script
# tool parameters so that the applied symbology is seen. See the ArcGIS Pro
# documentation page for ApplySymbologyFromLayer.
#
# March 2023
#########1#########2#########3#########4#########5#########6#########7#########8

import arcpy
import image2hist

arcpy.AddMessage("Image to Histogram tool")

# get the parameter values from the tool user interface
geoimg = arcpy.GetParameterAsText(0)
histlyrx = arcpy.GetParameter(1)
xband = int(arcpy.GetParameterAsText(2))
yband = int(arcpy.GetParameterAsText(3))

arcpy.AddMessage("Calling image2hist ...\n")

# image2hist() returns an ArcGIS raster object
histRaster = image2hist.image2hist(geoimg, xband, yband) 

# write to gdb, same name as input image with '_hist' suffix
histRasterName = geoimg + '_hist' 
histRaster.save(histRasterName)

# Confirm if map named 'Histogram' is present in the current project
currProject = arcpy.mp.ArcGISProject("CURRENT")
histMapList = currProject.listMaps("Histogram")
if histMapList:
    arcpy.AddMessage("Histogram map is present.\n")
    histMap = histMapList[0]
    # add histogram raster to the map 'Histogram'
    histlyr = histMap.addDataFromPath(histRasterName)
    currProject.save()
    # symbolize the raster layer from layer file; catch typical first failure
    # during testing with try. Could not eliminate failures. This at least notifies. 
    try:
        histlyr = arcpy.management.ApplySymbologyFromLayer(histlyr, histlyrx)
        arcpy.AddMessage("New layer:  {0}".format(histlyr))
    except:
        arcpy.AddWarning("Could not successfully apply symbology to output.")
else:
    arcpy.AddError("No map named Histogram found.\n")
    histlyr = []

# Use SetParameter to associate the derived layer required by
# ApplySymbologyFromlayer to the 5th item in the parameter list
arcpy.SetParameter(4,histlyr)

arcpy.AddMessage("Completed.\n")

