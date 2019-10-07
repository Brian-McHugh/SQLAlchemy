import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"<h1>Welcome to the Hawaiian Weather API!</h1><br/>"
        f"<hr>"
        f"<h2>Available Routes:</h2><br/>"
        f"<h3>(1)/api/v1.0/precipitation</h3><br/>"
        f"<h4>All rainfall measurements available</h4><br/>"
        f"<h3>(2)/api/v1.0/stations</h3><br/>"
        f"<h4>Hawaiian weather stations</h4><br/>"
        f"<h3>(3)/api/v1.0/tobs</h3><br/>"
        f"<h4>Latest year of temperature readings available</h4><br/>"
        f"<h3>(4)/api/v1.0/<start></h3><br/>"
        f"<h4>TMIN, TAVG, TMAX for all dates after a given date string in the format yyyy-mm-dd, inclusive</h4><br/>"
        f"<h3>(5)/api/v1.0/<start>/<end></h3><br/>"
        f"<h4>TMIN, TAVG, TMAX for all dates between a start and end date string in the format yyyy-mm-dd, inclusive</h4>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data"""
    # Query all precipitation measurements
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    # Close the connection to the DB
    session.close()

    # Create a list of daily precipitation
    #daily_precip = list(np.ravel(results))
    
    # Convert the query results to a dict with date as the key and prcp as the value
    daily_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        daily_prcp.append(prcp_dict)
        
    return jsonify(daily_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Hawaiian weather stations"""
    # Query all station names
    results = session.query(Station.station).all()
    
    # Close the connection to the DB
    session.close()

    # Create a list of stations
    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of temperature measurements for the last 12 months available"""
    # Query the date of the last available temperature reading
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]
    
    # Calculate the date one year prior to the date of the last available temperature reading
    start_last_12 = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)
    start_last_12 = start_last_12.strftime("%Y-%m-%d")
    
    # Perform a query to retrieve the temperature data
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > start_last_12).\
        order_by(Measurement.date).all()

    # Close the connection to the DB
    session.close()

    # Create a list of temp observations
    tobs = list(np.ravel(results))

    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def temp_stats_after(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """TMIN, TAVG, TMAX for all dates after given date, inclusive"""
    
    # Perform a query to retrieve the temperature stats data
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).\
        filter(Measurement.date >= start_date).all()

    # Close the connection to the DB
    session.close()

    # Create a list of temperature stats
    temp_stats_after = list(np.ravel(results))

    return jsonify(temp_stats_after)


@app.route("/api/v1.0/<start>/<end>")
def temp_stats_btwn(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """TMIN, TAVG, TMAX for all dates between a start and end date, inclusive"""
    
    # Perform a query to retrieve the temperature data
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    results = session.query(*sel).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).all()   

    # Close the connection to the DB
    session.close()

    # Create a list of temperature stats
    temp_stats_btwn = list(np.ravel(results))

    return jsonify(temp_stats_btwn)


if __name__ == '__main__':
    app.run(debug=True)



    
    
    
  






























    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
