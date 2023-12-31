# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB

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
    return (
        f"Thank you for visiting my API! Please enjoy :)<br/>"
        f"<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"Daily precipitation data capture off the coast of Hawai'i: /api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Individual station data: /api/v1.0/stations<br/>"
        f"<br/>"
        f"Daily temperature observed at station USC00519281: /api/v1.0/tobs<br/>"
        f"<br/>"
        f"Min, Max, and Average temperature for individual days: /api/v1.0/start_date/yyyy-mm-dd<br/>"
        f"<br/>"
        f"Min, Max, and Average temperature for date ranges: /api/v1.0/start_and_end/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )

#---------------------------------------
#Created the route for the precipitation data

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    precip_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.date <= '2017-08-23').\
        order_by(measurement.date).all()

    session.close()


    all_rain = []
    for date, prcp in precip_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_rain.append(prcp_dict)

    return jsonify(all_rain)

#---------------------------------------
#Created the route for each individual station to see which station is the most active

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    active_stations = session.query(measurement.station).\
        group_by(measurement.station).all()

    session.close()

	#Here I was getting an error about an incorrect data type. Stack overflow helped big time with this one
	#This function converts a list of touples into a regular list
    station_list = list(np.ravel(active_stations))
    return jsonify(station_list)



#---------------------------------------
#Created the route for the tobs data at station USC00519281 since it's the busiest station 

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    tobs_results = session.query(measurement.date, measurement.tobs, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.station == 'USC00519281').all()

    session.close()

    tobs_total = []
    for date, tobs, prcp in tobs_results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_dict['prcp'] = prcp

        tobs_total.append(tobs_dict)

    return jsonify(tobs_total)


#---------------------------------------
#Created a route where users can manually enter a date to retrieve data from specific days in hawai'i from across all stations
#Includes the min, max, and average of all stations 

@app.route("/api/v1.0/start_date/<start_date>")
def Start_date(start_date, end_date='2017-08-23'):

    session = Session(engine)

    function_results = session.query(func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

    session.close()

    rain_stats = []
    for min_temp, max_temp, avg_temp in function_results:
        rain_stats_dict = {}
        rain_stats_dict['min_temp'] = min_temp
        rain_stats_dict['max_temp']= max_temp
        rain_stats_dict['avg_temp'] = avg_temp
        rain_stats.append(rain_stats_dict)

    if rain_stats_dict['min_temp']: 
        return jsonify(rain_stats)
    else:
        return jsonify({"error": f"Date(s) not found, invalid, or not formatted as YYYY-MM-DD."}), 404

#---------------------------------------
#This code is similar to the one above, however this one returns data from a range of dates rather than just one specific date.
#Again, includes the min, max, and average of the stations. 

@app.route("/api/v1.0/start_and_end/<start_date>/<end_date>")
def start_and_end(start_date, end_date='2017-08-23'):

    session = Session(engine)

    function_results = session.query(func.min(measurement.tobs),
        func.max(measurement.tobs),
        func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

    session.close()

    range_stats = []
    for min_temp, max_temp, avg_temp in function_results:
        range_stats_dict = {}
        range_stats_dict['min_temp'] = min_temp
        range_stats_dict['max_temp']= max_temp
        range_stats_dict['avg_temp'] = avg_temp
        range_stats.append(range_stats_dict)

    if range_stats_dict['min_temp']: 
        return jsonify(range_stats)
    else:
        return jsonify({"error": f"Date(s) not found, invalid, or not formatted as YYYY-MM-DD."}), 404


if __name__ == '__main__':
    app.run(debug=True)

#---------------------------------------


