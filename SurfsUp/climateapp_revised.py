import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData
from sqlalchemy.pool import StaticPool
from flask import Flask, jsonify
import datetime as dt
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

# Reminder:
# cd to this directory before running this code in vscode.

#################################################
# Database Setup
#################################################
# Web sites use threads, but sqlite is not thread-safe.
# These parameters will let us get around it.
# However, it is recommended you create a new Engine, Base, and Session
#   for each thread (each route call gets its own thread)
engine = (create_engine("sqlite:///Resources/hawaii.sqlite", 
connect_args={'check_same_thread':False},
   poolclass=StaticPool))

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our connection object
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Available Routes:<br/>" +
        "/api/v1.0/precipitation<br/>"+
        "/api/v1.0/stations<br/>"+
        "/api/v1.0/tobs<br/>"+
        "/api/v1.0/<start><br/>"+
        "/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using date as the key and prcp as the value."""
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

    # Create a blank dictionary to house values
    rainfall_dict = {}

    # Assign dates as keys with precip data as values
    for result in results:
        rainfall_dict[result[0]] = result[1]
    """Return the JSON representation of your dictionary."""
    return jsonify(rainfall_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(Measurement.station).\
    group_by(Measurement.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))
    
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point."""
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    # Create a blank dictionary to house values
    tobs_dict = {}

    # Assign dates as keys with temp data as values
    for result in results:
        tobs_dict[result[0]] = result[1]
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    return jsonify(tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""
    start_dt= (dt.datetime.strptime(start, '%Y-%m-%d'))-dt.timedelta(days=365)
    results = (session.query(
                        func.min(Measurement.tobs),
                        func.avg(Measurement.tobs),
                        func.max(Measurement.tobs))
           .filter(Measurement.date >= start_dt).all())

    # Convert list of tuples into normal list
    trip_stats = list(np.ravel(results))
    
    return jsonify(trip_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""
    start_dt= (dt.datetime.strptime(start, '%Y-%m-%d')-dt.timedelta(days=365))
    end_dt= (dt.datetime.strptime(end, '%Y-%m-%d')-dt.timedelta(days=365))
    results = (session.query(
                    func.min(Measurement.tobs),
                    func.avg(Measurement.tobs),
                    func.max(Measurement.tobs))
            .filter(Measurement.date >= start_dt)
            .filter(Measurement.date <= end_dt).all())

    # Convert list of tuples into normal list
    trip_stats = list(np.ravel(results))
    
    return jsonify(trip_stats)

if __name__ == '__main__':
    app.run(debug=True)

"""sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file (Background on this error at: http://sqlalche.me/e/e3q8)"""
