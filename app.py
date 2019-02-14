#                                                           Assignment 10 - Advanced SQL 
# Step 2 - Climate App

''' 
Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

Use FLASK to create your routes.
'''

'''
Routes

/
Home page.
List all routes that are available.

/api/v1.0/precipitation
Convert the query results to a Dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.

/api/v1.0/stations
Return a JSON list of stations from the dataset.

/api/v1.0/tobs
query for the dates and temperature observations from a year from the last data point.
Return a JSON list of Temperature Observations (tobs) for the previous year.

/api/v1.0/<start> and /api/v1.0/<start>/<end>
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
'''

# Dependencies
import numpy as np
import datetime as dt
import time
from flask import Flask, jsonify

# Import SQL Alchemy
import sqlalchemy 
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Import SQL Database into engine
engine = create_engine("sqlite:///./hawaii.sqlite", echo=False)

# Define Base class to map the tables.
Base = automap_base()

Base.prepare(engine, reflect=True)

# Create table classes using Base class
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create connection to the Database
session = Session(engine)

# Flask setup

app = Flask(__name__)

# ############## Flask Routes ###################

# Home page. 
# List all routes that are available.
'''
Routes

/
Home page.
List all routes that are available.
'''

@app.route("/")
def home_page():
    #Return all lists available.
    return (
        f"Welcome to Climate App. Routes avialable: <br/>"
        # list all the routes
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/Start Date (YYYY-MM-DD) <br/>" 
        f"/api/v1.0/Start Date/End Date (YYYY-MM-DD)"
    )

'''
/api/v1.0/precipitation
Convert the query results to a Dictionary using date as the key and prcp as the value.
Return the JSON representation of your dictionary.
'''

# Route to Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # return date and precipitaation from Measurement Table
    record = session.query(Measurement.date, Measurement.prcp).limit(1000).all()
    
    # Define list for storing date and precipitation
    prec_date = []

    # loop the record and store in the list
    for prec in record:
        # Define Dictionary
        prec_dict = {}
        prec_dict['Date'] = prec.date
        prec_dict['Precipitation Value'] = prec.prcp
        prec_date.append(prec_dict)

    # unravel the list
    #perc_data = list(np.ravel(record))
    
    return jsonify(prec_date)

'''
/api/v1.0/stations
Return a JSON list of stations from the dataset.
'''

@app.route("/api/v1.0/stations")
def station_all():
    # Query to retrieve stations
    stations = session.query(Station.station, Station.name).all()
    station_list = []
    # unravel the list
    #station_data = list(np.ravel(stations))
    for sta in stations:
        station_list.append(sta)

    #station_data = list(np.ravel(station_list))
    return jsonify(station_list)

'''
/api/v1.0/tobs
query for the dates and temperature observations from a year from the last data point.
Return a JSON list of Temperature Observations (tobs) for the previous year.
'''

@app.route("/api/v1.0/tobs")
def temp_observ():
    #Get latest date
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    #Split the date into integers
    max_date= max_date.date

    # Split the Year, Date and Month 
    year = max_date.split('-')
    yr=int(year[0])
    mt=int(year[1])
    dy=int(year[2])

    ## Get past year date by subtracting 365 days from the max date 
    last_12_month = dt.date(yr,mt,dy) - dt.timedelta(days=365)

    # Retrieve temperature observations for last 12 months.

    temp_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=last_12_month)\
                    .order_by(Measurement.date).all()
    
    # unravel the list
    temperatures = list(np.ravel(temp_data))

    return jsonify(temperatures)


'''
/api/v1.0/<start> and /api/v1.0/<start>/<end>
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
'''

@app.route("/api/v1.0/<start>")
def avg_temp_start(start):
    #start_date = dt.datetime.strftime(start,"%Y-%m-%d")

    start_date = start
    
    # Query using start date
    temp_result = session.query( func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
           filter(Measurement.date >= start_date).all()

    temp_data = list(np.ravel(temp_result))
    
    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def avg_temp_range(start,end):
    start_date = start
    end_date=end

    # Query using start date and end date
    temp_result_range = session.query( func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
           filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    temp_data1 = list(np.ravel(temp_result_range))

    return jsonify(temp_data1)

'''End Flask'''

if __name__ == "__main__":
    app.run(debug=True)


