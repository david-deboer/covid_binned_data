# covid_binned_data

Geographically binned US COVID-19 data from the Johns Hopkins online database at https://github.com/CSSEGISandData/COVID-19.git

Updated daily after Johns Hopkins updates.

Uses Basemap from Matplotlib to locate longitude and latitude into shapefiles for counties and Congressional districts.

Unbinned data are assigned to "State FIP-0000"

Numbers are US Census Bureau FIP.
    State are two digit numbers
    County are three digit numbers
    Congressional district are two digit numbers
    Unassigned are 0000

Current data files:
* Bin_Confirmed_County.csv
* Bin_Deaths_County.csv
* Bin_Confirmed_Congress_District.csv
* Bin_Deaths_Congress_District.csv

Columns are:
* 1 - FIP number state-geo
* 2 - State name
* 3 - County name/Congressional District Number
* 4 - Longitude:  longitude of the weighted centroid on the last day of the file
* 5 - Latitude:  latitude of the weighted centroid on the last day of the file
* 6 - Count on date
.......

.txt files have run meta-information

A simple reader is provided called 'quickcsv'.

E.g. at your command prompt type './quickcsv.py'
