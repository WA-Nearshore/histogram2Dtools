# README Histogram2D Tools

This repository contains four ArcGIS Pro script tools.  

The purpose of these script tools is to enable interactive exploration of the spectral properties of multi-band imagery. The user can create a 2-dimensional spectral frequency histogram from two specified bands of an image. The user can also delineate polygon AOIs within the image and locate the associated pixels on the histogram. Likewise, polygon AOIs within the histogram can be associated with pixels in the image.

The tools and their usage are described in the User Manual (pdf) that is included in the repository. Consider this a beta release of these script tools as there are significant known issues as described below.
<br>
| Tool Name            | Tool Function                           |
|----------------------|-----------------------------------------|
| Import Layout        | Imports a layout and map into the current ArcGIS Pro project |
| Image to Histogram   | Creates a 2-dimensional spectral frequency histogram from a specified image |
| Polygon to Histogram | Creates a histogram mask indicating histogram cells that are associated with image pixels within a polygon AOI |
| Polygon to Image     | Creates an image mask indicating image pixels that are associated with histogram cells within a polygon AOI |



<br>
Nearshore Habitat Program<br>
Aquatic Resources Division<br>
Washington State Department of Natural Resources<br>
nearshore@dnr.wa.gov<br>
April 2023
<br>
<br>

--------

## Known Issues
When a 2-dimensional histogram is created from an image with the ‘Image to Histogram’ tool, the symbology is not consistently applied from the specified layer file.  Static (hist_sumbology.lyrx) and dynamic (hist_symbology_nbj.lyrx) symbology layer files are included in the repository for this purpose. The problem commonly occurs on the first usage of the tool within a Pro session, but symbology is correctly applied for subsequent uses.

The script tools currently only handle 8-bit image bands with brightness values that vary from 0 to 255.

For the two tools that operate on polygon AOIs, there is an option to interactively create polygons in a new layer created from within the tool interface.  In testing, we found that these layers are automatically saved as a feature class to the project geodatabase, but with the extent not properly set.  As a consequence, if that feature class is used for AOI definition in subsequent uses of the tools, Error 010568: Invalid extent is raised. The ‘Recalculate Feature Class Extent’ system tool in the Data Management Tools in the Feature Class Toolset can be used to correct the extent.

