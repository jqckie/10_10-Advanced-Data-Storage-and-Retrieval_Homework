# SQLAlchemy Weather Reports and FLASK app

## Instructions
* Run [climate_analysis.ipynb](SurfsUp/climate_analysis.ipynb) to analyze [hawaii.sqlite](Resources/hawaii.sqlite)
* Run [climateapp.py](SurfsUp/climateapp.py) to launch a flask app that returns weather analysis data

## Background

Using SQLAlchemy ORM queries, Pandas, Matplotlib, Python, and SQLAlchemy to do basic climate analysis and data exploration of climate database for a date range.

## Details 

* Using SQLAlchemy `create_engine` to connect to sqlite database.

* Using SQLAlchemy `automap_base()` to reflect tables into classes, saving a reference to those classes called `Station` and `Measurement`.

* Querying for the last 12 months of precipitation data.

* Selecting only the `date` and `prcp` values.

* Loading the query results into a Pandas DataFrame and setting the index to the date column.

* Sorting the DataFrame values by `date`.

* Plotting the results using the DataFrame `plot` method.

* Using Pandas to print summary statistics for the precipitation data.

* Querying for the total number of weather stations.

* Querying for the most active weather stations.

  * Listing the stations and observation counts in descending order.

* Retrieving the last 12 months of temperature observation data (tobs).

  * Filtering by the station with the highest number of observations.

  * Plotting the results as a histogram with `bins=12`.

* Using the `calc_temps` function to calculate the min, avg, and max temperatures for a date range using the matching dates from the previous year.

* Plotting the min, avg, and max temperature from the previous query as a bar chart.

* Calculating the rainfall per weather station using the previous year's matching dates.

* Designing a Flask API based on the weather analysis queries above.

* Creating the following FLASK routes:

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * query for the dates and temperature observations from a year from the last data point.
  * Return a JSON list of Temperature Observations (tobs) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
