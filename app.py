# Dependencies
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

#Data Tables
Base.prepare(autoload_with=engine)

# Reference Tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Bring Flask to create app
app = Flask(__name__)

# Function to recal most recent date
def date_prev_year():
    
    session = Session(engine)

    # Define the most recent date in the Measurement dataset
    # Then use the most recent date to calculate the date one year from the last date
    most_recent_date_str = session.query(func.max(Measurement.date)).first()[0]
    first_date = dt.date.fromisoformat(most_recent_date_str) -dt.timedelta(days=365) 
    # Close the session                   
    session.close()

    # Return the date
    return(first_date)

# Define what to do when the user hits the homepage
@app.route("/")
def homepage():
    return """ <h1>Section 2: Climate API </u></h1>
    <img src="Resources/Hawaii2.jpg" alt="Hawaii Image" width="500" height="400">
    <h3> Available Routes </h3>
    <ul>
    <li><a href = "/api/v1.0/precipitation"> Precipitation</a>: <strong>/api/v1.0/precipitation</strong> </li>
    <li><a href = "/api/v1.0/stations"> Stations </a>: <strong>/api/v1.0/stations</strong></li>
    <li><a href = "/api/v1.0/tobs"> Temperature observations for the past 12 months </a>: <strong>/api/v1.0/tobs</strong></li>
    <br/>
    <li><strong>For Specific Date Searches, uses extensions below following (YYY-MM-DD):</strong></li>
    <br/>
    <li>To retrieve the Temperature Summary (Min/ Max and Average Temp) for a Specific Date, use <strong>/api/v1.0/&ltStart_Date&gt</strong></li>
    <li>To retrieve the Temperature Summary (Min/ Max and Average Temp) for a Date Range, use <strong>/api/v1.0/&ltStart_Date&gt/&ltEnd_Date&gt</strong> </li>
    </ul>
    """

# Define what to do when the user hits the precipitation URL
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session
    session = Session(engine)

    # Query precipitation data from last 12 months from the most recent date from Measurement table
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_prev_year()).all()
    # Close the session                   
    session.close()

    # Create a dictionary from the row data and append to a list of prcp_list
    prcp_list = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    # Return a list of jsonified precipitation data for the previous 12 months 
    return jsonify(prcp_list)

# Define what to do when the user hits the station URL
@app.route("/api/v1.0/stations")
def stations():
    # Create the session
    session = Session(engine)

    # Query station data from the Station dataset
    station_data = session.query(Station.station).all()

    # Close the session                   
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_data))

    # Return a list of jsonified station data
    return jsonify(station_list)

# Define what to do when the user hits the URL
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session
    session = Session(engine)

    # Query tobs data from last 12 months from the most recent date from Measurement table
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
                        filter(Measurement.date >= date_prev_year()).all()

    # Close the session                   
    session.close()

    # Create a dictionary from the row data and append to a list of tobs_list
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    #Return
    return jsonify(tobs_list)

# Define what to do when the user hits the URL with a specific start date or start-end range
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def cal_temp(start=None, end=None):
    # Create the session
    session = Session(engine)
    
    # Make a list to query (the minimum, average and maximum temperature)
    sel=[
        func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)]
    
    # Check if there is an end date then do the task accordingly
    if end == None: 
        # Query the data from start date to the most recent date
        start_data = session.query(*sel).filter(Measurement.date >= start).all()
        start_list = list(np.ravel(start_data))
        return jsonify(start_list)
    else:
        # Query the data from start date to the end date
        start_end_data = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        # Convert list of tuples into normal list
        start_end_list = list(np.ravel(start_end_data))

        # Return a list of jsonified minimum, average and maximum temperatures for a specific start-end date range
        return jsonify(start_end_list)

    # Close the session                   
    session.close()
    
# Define main branch 
if __name__ == "__main__":
    app.run(debug = True)