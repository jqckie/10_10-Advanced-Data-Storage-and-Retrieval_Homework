import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, MetaData
from sqlalchemy.pool import StaticPool
from flask import Flask, jsonify
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
        "/api/v1.0/stations"
    )


@app.route("/api/v1.0/precipitation")
def rainfall():
    """Return rainfall totals"""
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    rainfall_details = list(np.ravel(results))
    # Create a dictionary from the row data and append to a list of all_passengers
    rainfall_details = []
    for result in results:
        rainfall_dict = {}
        rainfall_dict["key"] = result.date
        rainfall_dict["value"] = result.prcp
        rainfall_details.append(rainfall_dict)

    return jsonify(rainfall_details)
""" 
@app.route("/api/v1.0/stations")
def stations():

    # Query for stations
    results = session.query(Measurement.station).\
    group_by(Measurement.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temps():

    # Query for temps
    results = (session.query(
    Measurement.tobs)
.filter(Measurement.date >= '2016-08-23').all())

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

@app.route("/api/v1.0/2017-04-01")
def temps():

    # Query for temps
    results = (session.query(
    Measurement.tobs)
.filter(Measurement.date >= '2016-08-23').all())

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(results))

    return jsonify(temp_list)

@app.route("/api/v1.0/tobs")
def temps():
 
    # Query for temps
    results = (session.query(
    Measurement.tobs)
.filter(Measurement.date >= '2016-08-23').all())

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(results))

    return jsonify(temp_list)


##############################################
@app.route("/api/v1.0/stations")
def liststations():

    # Query stations
    results = session.query(Measurement.station).\
    group_by(Measurement.station).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for passenger in results:
        passenger_dict = {}
        passenger_dict["name"] = passenger.name
        passenger_dict["age"] = passenger.age
        passenger_dict["sex"] = passenger.sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)

 """
if __name__ == '__main__':
    app.run(debug=True)

"""sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) unable to open database file (Background on this error at: http://sqlalche.me/e/e3q8)"""
