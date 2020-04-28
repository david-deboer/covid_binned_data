# covid_binned_data
David DeBoer (ddeboer@berkeley.edu)

This derived database is intended to provide up-to-date easily accessible geo-binned data for research purposes from the Johns Hopkins maintained database
https://github.com/CSSEGISandData/COVID-19.git

Updated daily after Johns Hopkins updates.

Uses Basemap from Matplotlib to locate longitude and latitude into Census Bureau shapefiles for all US:
* States
* Counties
* Congressional districts
* Combined statistical areas
* National urban areas
* Native American areas

Additionally, the global data files are binned into Country.  If the county data are listed in provinces,
the provinces supplied are listed.

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
Bin_Confirmed_Urban.csv    | Confirmed cases binned into National Urban Areas
Bin_Deaths_Urban.csv       | Deaths binned into National Urban areas
Bin_Confirmed_Native.csv   | Confirmed cases binned into Native American areas
Bin_Deaths_Native.csv      | Deaths binned into Native American areas
Bin_Confirmed_Country.csv  | Confirmed cases binned into Countries
Bin_Deaths_Country.csv     | Deaths binned into Countries

The first three columns vary by geographical bin as follows (the first column is a unique key):

Geo      | Column 1 |Column 2   | Column 3   | Key comprises
---------|----------|-----------|------------|---------------
County   | Key      | Name      | (blank)    | STate-COUNTYFP
Congress | Key      | State     | District   | STate-District
State    | Key      | State     | (blank)    | STate
CSA      | Key      | Name      | States     | CSAFP
Urban    | Key      | Name      | States     | UACE10
Native   | Key      | NAME      | NAMELSAD   | GEOID
Country  | Key      | Provinces | (blank)    | Country

The following columns contain data:

Col | All
----|------
4   | Longitude:  longitude of the weighted centroid on the last day of the file
5   | Latitude:  latitude of the weighted centroid on the last day of the file
6   | Count on date
.......


Run*.txt files have run meta-information

## Viewing software
A very simple reader is provided called 'quickcsv' to provide an initial glimpse.

E.g. at your command prompt (in the directory where you installed) type './quickcsv.py'

More sophisticated plots may be made by installing binc19 and using the methods there.  These files
are in-process research-grade modules to view time series of data.

## Generating software
![US States with centroid of cases over time](https://astro.berkeley.edu/~ddeboer/Confirmed_States_200426_time_centroid.png)
CAPTION State totals of confirmed cases, with the centroid of where deaths occurred over time.

As mentioned above, the generating mapping software use matplotlib Basemap and shapefiles from the US Census Bureau.
The two packages written and used are:  mymaps and bgbcovid (Berkeley Geo-Binned Covid).  These aren't currently
distributed as they are even rougher.  In addition to geo-binning, the code draws maps, calculates and displays overlays and contains slightly more data than in this repo (currently only the centroid over time).

Please contact ddeboer@berkeley.edu if interested.

In addition to states shown above, the areas used are:

![US Counties](https://astro.berkeley.edu/~ddeboer/Confirmed_County_042320.png)
CAPTION Confirmed cases by County.
![US Combined Statistical Areas](https://astro.berkeley.edu/~ddeboer/Confirmed_CSA_042320.png)
CAPTION Confirmed cases by Combined Statistical Areas
![US Native American Areas](https://astro.berkeley.edu/~ddeboer/Confirmed_Native_200425.png)
CAPTION Confirmed cases by Native American Areas
![US National Urban Areas](https://astro.berkeley.edu/~ddeboer/Confirmed_Urban_042320.png)
CAPTION Confirmed cases by National Urban Areas
![US National Urban Areas - zoom](https://astro.berkeley.edu/~ddeboer/Confirmed_Urban_close_042320.png)
![CA counties in time](https://astro.berkeley.edu/~ddeboer/CA_County-4_10_20.png)
CAPTION CA counties in time
