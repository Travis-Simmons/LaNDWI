# LaNDWI

LaNDWI is a containerized Landsat 8 processing tool for timeseries NDWI analysis.

## Inputs

A directory containing compressed Landsat 8 data, and corner cordinates for your region of interest.


## Outputs

The origional Landast 8 data cropped to your region of interest and sorted by cloudcover as well as the results of the NDWI analysis for each non-cloudy day.

## Arguments and Flags
* **Positional Arguments:**
    * **Directory containing compressed Landsat 8 data:** 'indir'
* **Required Arguments:**
    * **Corner cordinates of GPS bounding box for your region of intrest:** '-b', '--bounding_box'
* **Optional Arguments:**
    * **Strictness of cloud detection:** '-c', '--how_strict', default = 0.7 (the lower the value the more strict)

## Workflow for finding GPS bounding cordinates.

1. Download the Earth Explorer Bulk Download Application 
    * https://dds.cr.usgs.gov/bulk
2. Use the Bulk Download Application and the Earth Eplorer Website in order to bulk download compressed Lansat-8 data in your region of intrest
    * add in screenshots of workflow
