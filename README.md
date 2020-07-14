# covid_binned_data
7/14/20
Since much better options exist, I am deprecating parts of this repo.  Primary Urban and Native Title areas, since the geolocation of the data is not sufficient to adequately represent the data.  I am also removing quickcsv.py and some functions within the installed code.  This is in an effort to make it simpler to maintain.

David DeBoer (ddeboer@berkeley.edu)

This derived database is intended to provide up-to-date easily accessible geo-binned data for research purposes from the Johns Hopkins maintained database
https://github.com/CSSEGISandData/COVID-19.git

Updated daily after Johns Hopkins updates.

Uses Basemap from Matplotlib to locate longitude and latitude into Census Bureau shapefiles for all US:
* Counties
* Congressional districts
* Combined statistical areas

Additionally, US data files are binned by state and the global data files are binned into Country.
If the country data are listed in provinces, the provinces supplied are listed.

Unbinned data are assigned to "9999" to within that state/area.

## Current data files:

Name                       | Description
---------------------------|----------------------
Bin_Confirmed_County.csv   | Confirmed cases binned into Counties
Bin_Deaths_County.csv      | Deaths binned into Counties
Bin_Confirmed_State.csv    | Confirmed cases binned into States
Bin_Deaths_State.csv       | Deaths binned into States
Bin_Confirmed_Congress.csv | Confirmed cases binned into Congressional Districts
Bin_Deaths_Congress.csv    | Deaths binned into Congressional Districts
Bin_Confirmed_CSA.csv      | Confirmed cases binned into Combined Statistical Areas
Bin_Deaths_CSA.csv         | Deaths binned into Combined Statistical Areas
Bin_Confirmed_Country.csv  | Confirmed cases binned into Countries
Bin_Deaths_Country.csv     | Deaths binned into Countries

The first three columns vary by geographical bin as follows (the first column is a unique key):

Geo      | Column 1 |Column 2   | Column 3   | Key comprises
---------|----------|-----------|------------|---------------
County   | Key      | Name      | STate      | STate-COUNTYFP
Congress | Key      | STate     | District   | STate-District
State    | Key      | State     | STate      | STate
CSA      | Key      | Name      | STates     | CSAFP
Country  | Key      | Provinces | STate      | Country

The following columns contain data:

Col | All
----|------
4   | Longitude:  longitude of the weighted centroid on the last day of the file
5   | Latitude:  latitude of the weighted centroid on the last day of the file
6   | Count on date
.......


Run*.txt files have run meta-information
