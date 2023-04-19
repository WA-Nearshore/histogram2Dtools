#########1#########2#########3#########4#########5#########6#########7#########8
# ArcGIS Toolbox scrip tool:  Polygon to Image 
#
# This script tool takes pixels from a polygon AOI within a 2-dimensional
# histogram raster and transforms the pixels in the histogram AOI to the
# associated pixels in the original image. 
#
# The original image is asssumed to be 8 bit.
#
# Script tool parameters (set in ArcGIS tool user interface): 
#  hist2D [raster] = the 2-dimensional histogram previously made based on geoimg
#  polyAOI [polygon] = the polygon feature class or layer defining the AOI. This
#                      can be created on the fly by drawing polygons in an
#                      ArcGIS Pro map. 
#  geoimg [raster] = the input image, typically a multiband aerial photo.
#  xband [int] = the band number to appear on x-axis of histogram (default 4).
#  yband [int] = the band number to appear on y=axis of histogram (default 3). 
#
# The default band numbers were selected for a near-IR and blue histogram when
# using R-G-B-nearIR imagery.
#
# April 2023
#########1#########2#########3#########4#########5#########6#########7#########8

import arcpy
import numpy as np

arcpy.AddMessage("Polygon to Image tool")

# get the parameter values from the tool user interface
hist2D = arcpy.GetParameterAsText(0)
polyAOI = arcpy.GetParameter(1)
geoimg = arcpy.GetParameterAsText(2)
xband = arcpy.GetParameter(3)
yband = arcpy.GetParameter(4)


############################################################################
# working in histogram space - goal is a 1D array of brightness value codes
# of all pixels within the histogram AOI.  Brightness value codes are
# concatenated values of the brightness values from the two bands with the
# x-axis brightness value displaced by 1000 - e.g. 128 and 221 give a code
# of 128221.
############################################################################

# extract the AOI pixels from the source histogram 
arcpy.AddMessage("Extracting AOI from histogram ...")
histAOIExtract = arcpy.sa.ExtractByMask(in_raster = hist2D, 
                                        in_mask_data = polyAOI)

# create 256x256 rasters; one with row values and one with col values
arcpy.AddMessage("Creating row and col rasters...")
row_arr = np.indices((256,256))[0]
col_arr = np.indices((256,256))[1]
rowRast = arcpy.NumPyArrayToRaster(row_arr, value_to_nodata=0)
colRast = arcpy.NumPyArrayToRaster(col_arr, value_to_nodata=0)

# Use histogram AOI extract as mask to extract those pixels from row & col
# rasters. 
arcpy.AddMessage("Extracting from row and col rasters...")
rowAOIExtract = arcpy.sa.ExtractByMask(in_raster = rowRast, 
                                       in_mask_data = histAOIExtract)
colAOIExtract = arcpy.sa.ExtractByMask(in_raster = colRast, 
                                       in_mask_data = histAOIExtract)
# consolidate the two layers, displacing col values by x1000
rowColAOIExtract = rowAOIExtract + 1000*colAOIExtract

# convert to NumPy array, and then to 1D array of target brightness value codes
arcpy.AddMessage("Reduce extract pixels to 1D array...")
rowColAOIarr = arcpy.RasterToNumPyArray(in_raster = rowColAOIExtract)
bv_pair_vals = np.concatenate(rowColAOIarr)
# filter out code values of zero; zero used for NoData for brightness values
bv_pair_vals[bv_pair_vals != 0]


############################################################################
# working in geographic image space - goal is a mask to overlay on the
# original image that indicates each pixel with brightness value pairs that
# match the pairs from the histogram AOI (bv_pair_vals).
############################################################################

# construct paths to the two selected bands of the original image
arcpy.AddMessage("Retrieving image bands...")
geoimage = arcpy.Raster(geoimg, is_multidimensional=True)
# set NoData value to 0 for each layer, for pixels outside extraction mask;
# this assumes ther input image has 4 bands
geoimage.setProperty("noDataValues", (0,0,0,0))
imgPath = geoimage.catalogPath
xbandpath = f"{imgPath}\Band_{xband}"
ybandpath = f"{imgPath}\Band_{yband}"
arcpy.AddMessage("x: {0}".format(xbandpath))
arcpy.AddMessage("y: {0}".format(ybandpath))

# consolidate the two image bands into one raster layer with x-values x1000
arcpy.AddMessage("Create raster of codes ...")
imgCodes = arcpy.Raster(ybandpath) + 1000*arcpy.Raster(xbandpath)

# convert from ArcGIS Raster to NumPy array (32bit integer)
arcpy.AddMessage("Creating image mask...")
imgCodesArr = arcpy.RasterToNumPyArray(in_raster=imgCodes, 
                                       nodata_to_value=0)
# test each array element (pixel) for membership in the set of AOI b.v. pairs,
# convert boolean output from .isin to int
imgMask = np.isin(imgCodesArr, bv_pair_vals).astype(int)


# convert back to ArcGIS Raster object and with extent and spatial ref. 
# matching original image
arcpy.AddMessage("Convert to ArcGIS Raster and save...")
arcpy.env.outputCoordinateSystem = arcpy.Describe(geoimage).spatialReference
LLx = geoimage.extent.XMin
LLy = geoimage.extent.YMin
lower_left_pt = arcpy.Point(LLx,LLy)
xResult = arcpy.management.GetRasterProperties(in_raster=geoimage,
                                               property_type="CELLSIZEX")
yResult = arcpy.management.GetRasterProperties(in_raster=geoimage,
                                               property_type="CELLSIZEY")
xsize = float(xResult.getOutput(0))
ysize = float(yResult.getOutput(0))
arcpy.AddMessage("xysize:  {0} {1}".format(xsize,ysize))
imgMaskRaster = arcpy.NumPyArrayToRaster(in_array=imgMask,
                                         lower_left_corner=lower_left_pt,
                                         x_cell_size=xsize,
                                         y_cell_size=ysize,
                                         value_to_nodata=0)

# write to gdb, same name as original image with '_hist_AOI' suffix
maskRasterName = geoimg + '_hist_AOI2img' 
imgMaskRaster.save(maskRasterName)

arcpy.AddMessage("Completed.")


