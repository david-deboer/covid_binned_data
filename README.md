# covid_binned_data


This derived database is intended to provide up-to-date easily accessible geo-binned data for research purposes from the Johns Hopkins maintained database
https://github.com/CSSEGISandData/COVID-19.git

Updated daily after Johns Hopkins updates.

Uses Basemap from Matplotlib to locate longitude and latitude into Census Bureau shapefiles for all US:
* States
* Counties
* Congressional districts
* Combined statistical areas
* National urban areas

Additionally, the global data files are binned into Country.  If the county data are listed in provinces,
the provinces supplied are listed.

Unbinned data are assigned to "9999" to within that state.

Current data files:

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
Bin_Confirmed_Urban.csv    | Confirmed cases binned into National Urban Areas
Bin_Deaths_Urban.csv       | Deaths binned into National Urban areas
Bin_Confirmed_Country.csv  | Confirmed cases binned into Countries
Bin_Deaths_Country.csv     | Deaths binned into Countries

The first three columns vary of geographical bin as follows (the first column is a unique key):

Geo      | Column 1 |Column 2   | Column 3
---------|----------|-----------|---------
County   | Key      | State     | Name
Congress | Key      | State     | District
State    | Key      | State     | State
CSA      | Key      | CSAFP     | NAME
Urban    | Key      | State     | Name
Country  | Key      | Provinces | (blank)

The following columns contain data:

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


![US States](https://astro.berkeley.edu/~ddeboer/Confirmed_States_042320.png)
![US Counties](https://astro.berkeley.edu/~ddeboer/Confirmed_County_042320.png)
![US Combined Statistical Areas](https://astro.berkeley.edu/~ddeboer/Confirmed_CSA_042320.png)
![US National Urban Areas](https://astro.berkeley.edu/~ddeboer/Confirmed_Urban_042320.png)
![US National Urban Areas - zoom](https://astro.berkeley.edu/~ddeboer/Confirmed_Urban_close_042320.png)
![CA counties in time](https://astro.berkeley.edu/~ddeboer/CA_County-4_10_20.png)
