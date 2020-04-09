# covid_binned_data

Geographically bins US COVID-19 data from https://github.com/CSSEGISandData/COVID-19.git

Uses Basemap from Matplotlib to locate longitude and latitude into shapefiles for congressional districts and counties.

Unbinned data are assigned to State, Unassigned

Numbers are US Census Bureau FIP.
    State are two digit numbers
    County are three digit numbers
    Congressional district are two digit numbers

Current files:
* Bin_Confirmed_Congress_District.csv
* Bin_Deaths_Congress_District.csv
* Bin_Confirmed_County.csv
* Bin_Deaths_County.csv
