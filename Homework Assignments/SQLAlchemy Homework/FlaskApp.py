
import datetime as dt
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

start_date_string = "2017-08-31" 
start_date = dt.datetime.strptime(start_date_string, '%Y-%m-%d')

date_prev_year = start_date - relativedelta(years=1)
print("Date 1 year prior to the current date")

app = Flask (__name__)

#### FLASK ROUTES
###
#

@app.route("/")
def welcome(): 
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end <br/>"
    )

### PRECIPITATION API REQUEST 
##
#

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    precip_data = session.query(Measurement.date,Measurement.prcp).\
              filter(Measurement.date > date_prev_year).all()
    
    date_list= []
    prcp_list=[]
    count=0

    for row in precip_data:
        count+=1
        date_list.append(row.date)
        prcp_list.append(row.prcp)
        if count % 500 == 0:
            print(row.date, row.prcp)

    return jsonify (precip_data)

### STATIONS API REQUEST 
##
#

@app.route("/api/v1.0/stations")
def stations():
    ## Query results for stations 
    station_list = session.query(Measurement.station).all()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    ## Query results for temp observations
    results = session.query(Measurement.tobs).\
              filter(Measurement.date > date_prev_year).\
              all()
    return jsonify(results)

@app.route("/api/v1.0/startdate")
def temp_start(start):
    
    #Try except for start date.
   
    try:
        ent_start_date = dt.datetime.strptime(start_input, '%Y-%m-%d')
    except:
        print(" Invalid entry. Try the correct format = YYYY-MM-DD.")
        print(" Using default (2017-08-23)")
        print(" Start Date You Entered: " + start_input)
        print(" ")
        start_input = '2017-08-23'
        ent_start_date = dt.datetime.strptime(start_input, '%Y-%m-%d')
    
        
    print(ent_start_date)
    
    measured_temp_entry = session.query(func.min(Measurement.tobs),
                                        func.avg(Measurement.tobs),
                                        func.max(Measurement.tobs)).\
                          filter(Measurement.date >= ent_start_date).\
                          all()
    return jsonify(measured_temp_entry)

@app.route("/api/v1.0/startdateenddate")
def temp_start_end (start,end):
    start_input = input("Provide a start date (YYYY-MM-DD)")
    end_input = input("Provide an end date (YYYY-MM-DD)")
    
    try: 
        ent_start_date = dt.datetime.strptime(start_input, '%Y-%m-%d')
    except:
        print(" Invalid entry. Try the correct format = YYYY-MM-DD.")
        print(" Using default (2017-08-23)")
        print(" Start Date You Entered: " + start_input)
        print(" ")
        start_input = '2017-08-23'
        ent_start_date = dt.datetime.strptime(start_input, '%Y-%m-%d')
    
    try: 
        ent_end_date = dt.datetime.strptime(end_input, '%Y-%m-%d')
    except: 
        print(" Invalid entry. Try the correct format = YYYY-MM-DD.")
        print(" Using default current date ")
        print(" End Date You Entered: " + end_input)
        print(" ")
        end_input = '2017-08-23'
        ent_end_date = dt.datetime.today().strftime(end_input, '%Y-%m-%d')
    
    print(ent_start_date, ent_end_date)
    
####Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
####for a given start or start-end range.

####When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` 
####for all dates greater than and equal to the start date.

####When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
####for dates between the start and end date inclusive.
    
    measured_temp_entry = session.query(func.min(Measurement.tobs),
                                        func.avg(Measurement.tobs),
                                        func.max(Measurement.tobs)).\
                          filter(Measurement.date >= ent_start_date).\
                          filter(Measurement.date <= ent_end_date)
    return jsonify (measured_temp_entry)

if __name__ == '__main__':
    app.run(debug=True)