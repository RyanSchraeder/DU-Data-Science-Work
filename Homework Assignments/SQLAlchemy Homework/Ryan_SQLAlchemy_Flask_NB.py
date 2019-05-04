#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Dependencies (ORM, Numpy, Pandas, Matplotlib, Seaborn)
#get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

from collections import defaultdict
from dateutil.relativedelta import relativedelta


# In[2]:


import numpy as np
import pandas as pd


# In[3]:


import datetime as dt


# # Reflect Tables into SQLAlchemy ORM

# In[4]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
from sqlalchemy.inspection import inspect


# In[5]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[6]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[7]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[8]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[9]:


# Create our session (link) from Python to the DB
session = Session(engine)


# # Exploratory Climate Analysis
# 

# In[10]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results
start_date =  "2017-08-23"
start_date_int = dt.datetime.strptime(start_date, '%Y-%m-%d')


# Calculate the date 1 year ago from the last data point in the database
date_prev_year = start_date_int - relativedelta(years=1)

# Perform a query to retrieve the data and precipitation scores
precip_data = session.query(Measurement.date,Measurement.prcp).              filter(Measurement.date > date_prev_year).all()
date_list= []
prcp_list=[]
count=0

for row in precip_data:
    count+=1
    date_list.append(row.date)
    prcp_list.append(row.prcp)
    if count % 500 == 0:
        print(row.date, row.prcp)
    
precip_data_dict = {
                "Date":date_list,
                "Precipitation":prcp_list
                }

# Save the query results as a Pandas DataFrame and set the index to the date column
precip_df = pd.DataFrame(precip_data_dict)

# Sort the dataframe by date
precip_df_sorted = precip_df.sort_values('Date', ascending=True)
precip_df_sorted = precip_df_sorted.dropna(how="any")
precip_df_sorted

# Use Pandas Plotting with Matplotlib to plot the data
y_axis = precip_df_sorted['Precipitation']
x_axis = precip_df_sorted['Date']
plt.ylim = (0, y_axis)
plt.xlabel("date")

plt.plot(x_axis, y_axis)
plt.legend()

plt.savefig("./Ryan's Images/Precipitation Last Year in HI.png")
plt.show()


# In[11]:


# Use Pandas to print the summary statistics for the precipitation data
precip_df_sorted.describe()


# ### Station Analysis
# 
# * Design a query to calculate the total number of stations.
# 
# * Design a query to find the most active stations.
# 
#   * List the stations and observation counts in descending order.
# 
#   * Which station has the highest number of observations?
# 
#   * Hint: You may need to use functions such as `func.min`, `func.max`, `func.avg`, and `func.count` in your queries.
# 
# * Design a query to retrieve the last 12 months of temperature observation data (tobs).
# 
#   * Filter by the station with the highest number of observations.
# 
#   * Plot the results as a histogram with `bins=12`.
# 
# ![station-histogram](Images/station-histogram.png)
# 

# In[12]:


# Count of stations

stations_count = session.query(Station.station).count()
stations_count


# In[13]:


# Query for most active stations
# use desc 
# 
most_active_stations = session.query(Measurement.station,
                                    func.count(Measurement.station).label("count")).\
                                    group_by(Measurement.station).\
                                    order_by(desc("count")).\
                                    all()
most_active_stations


# In[14]:


# Which station has the highest number of observations? 

(station_max , count_max) = most_active_stations[0]

obs_station_max = session.query(func.max(Measurement.tobs),
                             func.min(Measurement.tobs),
                             func.avg(Measurement.tobs)).\
                filter(Measurement.station == station_max).\
                all()
obs_station_max


# In[15]:


# Incorporate date_prev_year to run this query to account for 12 months of data

temps = session.query(Measurement.tobs).        filter(Measurement.date > date_prev_year).        filter(Measurement.station == station_max).        all()
temps

#loop through rows to store temps as ints without commas

temp_list=[]
frequency=[]
count=0
for row in temps:
    count+=1
    temp, = row
    temp_list.append(temp)

print(str(len(temp_list)))

temps_dict = pd.DataFrame({
            "tobs": temp_list,
})

temps_dict.head()


# In[16]:


temps_dict.plot.hist(bins=12)
plt.savefig("./Ryan's Images/Temperature-vs-Frequency.png")
plt.show()


# ## Step 2 - Climate App
# 
# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.
# 
# * Use FLASK to create your routes.
# 

# ### Routes
# 
# * `/`
# 
#   * Home page.
# 
#   * List all routes that are available.
# 
# * `/api/v1.0/precipitation`
# 
#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# 
#   * Return the JSON representation of your dictionary.
# 
# * `/api/v1.0/stations`
# 
#   * Return a JSON list of stations from the dataset.
# 
# * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.
# 
# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
# 
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# 
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# 
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
# 

# ## Hints
# 
# * You will need to join the station and measurement tables for some of the analysis queries.
# 
# * Use Flask `jsonify` to convert your API data into a valid JSON response object.

# ## Integrated Flask App to Jupyter 

# In[1]:


from flask import Flask, jsonify

app = Flask (__name__)

#### FLASK ROUTES
@app.route("/")
def welcome(): 
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd <br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    ## Query results for date & prcp as a dict
    print(start_date)
    
    ##Query upon 12 months prior 
    print(date_prev_year)
    
    return jsonify (precip_df_sorted)

@app.route("/api/v1.0/stations")
def stations():
    ## Query results for stations 
    station_list = session.query(Measurement.station).distinct().all()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    ## Query results for temp observations
    results = session.query({
        'Date': date.name.all(),
        'Tobs': temps_dict['tobs']
    })
    return jsonify(results)

@app.route("/api/v1.0/<start>")
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

@app.route("/api/v1.0/<start>/<end>")
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
    


# ## Raw Flask Code for FlaskApp.py 
#  * Used in FlaskApp.py located in SQLAlchemy Homework folder
#  * CURRENTLY RETURNING DB CONNECTION ERROR - - https://docs.sqlalchemy.org/en/13/errors.html#error-e3q8)

# In[2]:


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
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd <br/>"
        f"/api/v1.0/yyyy-mm-dd <br/>"
    )

### PRECIPITATION API REQUEST 
##
#

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    ## Query results for date & prcp as a dict
    print(start_date)
    
    ##Query upon 12 months prior 
    print(date_prev_year)
    
    precip_data = session.query(Measurement.date,Measurement.prcp).              filter(Measurement.date > date_prev_year).all()
    
    date_list= []
    prcp_list=[]
    count=0

    for row in precip_data:
        count+=1
        date_list.append(row.date)
        prcp_list.append(row.prcp)
        if count % 500 == 0:
            print(row.date, row.prcp)
        
    precip_data_dict = {
                "Date":date_list,
                "Precipitation":prcp_list
                }
    return jsonify (precip_data_dict)

### STATIONS API REQUEST 
##
#

@app.route("/api/v1.0/stations")
def stations():
    ## Query results for stations 
    station_list = session.query(Measurement.station).distinct().all()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    ## Query results for temp observations
    results = session.query(Measurement.tobs).              filter(Measurement.date > date_prev_year).              all()
    return jsonify(results)

@app.route("/api/v1.0/<start>")
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

@app.route("/api/v1.0/<start>/<end>")
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


# In[ ]:




