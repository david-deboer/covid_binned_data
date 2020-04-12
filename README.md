# covid_binned_data

Geographically binned US COVID-19 data from the Johns Hopkins online database at https://github.com/CSSEGISandData/COVID-19.git

Updated daily after Johns Hopkins updates.

Uses Basemap from Matplotlib to locate longitude and latitude into Census Bureau shapefiles for counties and Congressional districts.

Unbinned data are assigned to "State-0000"

Current data files:

Name                                | Description
------------------------------------|----------------------
Bin_Confirmed_County.csv            | Confirmed cases binned into counties
Bin_Deaths_County.csv               | Deaths binned into counties
Bin_Confirmed_State.csv             | Confirmed cases binned into states
Bin_Deaths_State.csv                | Deaths binned into states
Bin_Confirmed_Congress_District.csv | Confirmed cases binned into Congressional Districts
Bin_Deaths_Congress_District.csv    | Deaths binned into Congressional Districts

Files have columns:

Col | District/County                           | State
----|-------------------------------------------|-------------
1   | FIP number state-geo                      | FIP number state
2   | State                                     | State
3   | County name/Congressional District Number | State name


Col | All
----|------
4   | Longitude:  longitude of the weighted centroid on the last day of the file
5   | Latitude:  latitude of the weighted centroid on the last day of the file
6   | Count on date
.......


Run*.txt files have run meta-information

A simple reader is provided called 'quickcsv'.

E.g. at your command prompt type './quickcsv.py'

<html>
<p>
<a href=https://astro.berkeley.edu/~ddeboer/uswithmega.png>US counties with overlay</a>
</p>
<p>
<a href=https://astro.berkeley.edu/~ddeboer/CA_track.png>California counties with overlay</a>
</p>
<p>
<a href=https://astro.berkeley.edu/~ddeboer/CA_County-4_10_20.png>California counties in time</a>
</p>
</html>
