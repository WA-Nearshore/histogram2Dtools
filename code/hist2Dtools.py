#########1#########2#########3#########4#########5#########6#########7#########8
#
#  Main script to call 2d histogram tools from Python environment. The intent
#  is that this will be replaced by ArcGIS Toolbox tools that call the Python
#  modules (files) that are called here.
#
#  Manages calls to three tools contained in three separate modules (.py files).
#  (1) img2hist tool.  Takes a multi-band raster image in geographic space and
#      creates a 2d histgram of pixel frequencies (a raster in 'histogram' space).
#  (2) poly2hist tool. Takes a polygon drawn over area of image in geographic
#      space and transforms the associated pixels to a mask in histogram
#      space to overlay on the 2d histogram.
#  (3) poly2img tool. Takes a polygon drawn over area of 2d histogram and
#      transforms the associated pixels to a mask in geographic space to
#      overlay over the geographic image.
#
#  The input aerial image is assumed to be in a file geodatabase. 
#  In typical usage, this image will be 4 band image (R-G-B-NIR), that has
#  been masked to the desired subset to be used in kelp classification.
#
#  February 2023
#
#########1#########2#########3#########4#########5#########6#########7#########8

import sys    # needed just for running in ArcGIS Pro Python window so import
              # can file the modules.
sys.path.append(r"C:/Users/pete/OneDrive/Work-current/kelp/2022_imagery/code")

import i2h_module


########## set path to a multi-band aerial photo digital image #########
# define a list of image names to select from (just for development) 
img_names = ["extract_0086","extract_0223","extract_0548",
             "extract_0519", "extract_070", 
             "poly_extract_0086_test_low"]
# select image to process by list index integer 
img_sel_idx = 0

# set paths to gdb and layer file for histogram symbology
gdb_path = r'F:/imagery_tif_2022/MyProject.gdb'
hist_lyrx = r'F:/imagery_tif_2022/hist_symbology.lyrx'
# set path to histogram layout file (applies grid) 
hist_layout_path = "F:/imagery_tif_2022/Histogram_layout.pagx"

inImagePath = gdb_path + r'/' + img_names[img_sel_idx] 
outImagePath = gdb_path + r'/' + img_names[img_sel_idx] + '_hist'

######################### call img2hist tool ######################### 
xBand = 4   # near-IR band
yBand = 3   # blue band
returnObj = i2h_module.img2hist(inImagePath,outImagePath,hist_lyrx,
                                hist_layout_path, xBand,yBand)

print("Complete.")


