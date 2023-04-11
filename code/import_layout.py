#########1#########2#########3#########4#########5#########6#########7#########8
# import_layout() - ArcGIS script tool to import layout into current project 
#
# This scrip tool performs a setup function for the subsequent use of the
# other tools bundled in the Histogram toolbox. These are tools to work with
# 2-dimentional histograms derived from two bands of an image. 
#
# This script tool is included for convenience, but the function is identical
# to the 'Import layout' tool available in the ArcGIS Pro ribbon. It is found 
# in the Insert menu in the Project group. It is used by selecting the
# 'Import layout file...' option in the menu that is presented by the tool.
# 
# When this script tool is used with the layout file distributed with the tool
# (Histogram_layout.pagx), a new layout named 'HistogramLayout' is created in 
# the current project. This layout contains a single map frame that is loaded 
# with a map named 'Histogram'. This map is also created at the time of the 
# layout import.
#
# If a layout named 'HistogramLayout' already exists in the current project,
# a message is written out and the import is not executed.
#
# This code is written to be called from an ArcGIS Toolbox, not to be used as
# a stand alone script. 
#
# Script tool parameters (set in ArcGIS tool user interface): 
#  histlayout = the layout file to be imported. This parameter has a data type
#               of Layout. 
#
# March 2023
#########1#########2#########3#########4#########5#########6#########7#########8

import arcpy

# get the layout file from the tool user interface
histlayout = arcpy.GetParameter(0)

# if layout named 'HistogramLayout' does not exist in the current project, 
# create it by import. This also creates the map 'Histogram' which appears
# in a map frame in the layout. 
# If map 'Histogram' already exists, the new map is named 'Histogram1'
currProject = arcpy.mp.ArcGISProject("CURRENT")
layoutList = currProject.listLayouts("HistogramLayout")
if not(layoutList):
    arcpy.AddMessage("Importing layout...\n")
    currProject.importDocument(histlayout)
    currProject.save()
    arcpy.AddMessage("Completed.\n")
else:
    arcpy.AddError("Layout named Histogram already exists.\n")
