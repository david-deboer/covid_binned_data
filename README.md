# covid_binned_data

This derived database is intended to provide up-to-date easily accessible geo-binned data for research purposes from the Johns Hopkins maintained database
https://github.com/CSSEGISandData/COVID-19.git

Updated daily after Johns Hopkins updates.

Uses Basemap from Matplotlib to locate longitude and latitude into Census Bureau shapefiles for states, counties and Congressional districts.

Unbinned data are assigned to "0000" to within that state.

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

The code used to generate draws maps, with overlays and contains slightly more data than in this repo
(currently only the centroid over time).  The software comprises two Python packages, which are very rough
research quality at this point in time.  They use a json format that is intermediate to these csv files and
draw maps with overlays and time series.
Please contact ddeboer@berkeley.edu if interested.


![US Counties with overlay](https://astro.berkeley.edu/~ddeboer/uswithmega.png)
Overlay points for illustrative purposes are the largest 500 mega-churches, taken from wikipedia (https://en.wikipedia.org/wiki/List_of_megachurches_in_the_United_States)
![CA with centroid track over time](https://astro.berkeley.edu/~ddeboer/CA_track.png)
Overlay points track the centroid over time.  The size if proportional to confirmed cases, with the largest the current value.
![CA counties in time](https://astro.berkeley.edu/~ddeboer/CA_County-4_10_20.png)
