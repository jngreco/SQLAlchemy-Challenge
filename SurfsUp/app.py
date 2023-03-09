import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement 
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

session = Session(engine)

###############################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of rain fall for prior year"""

    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    pre_scores= session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > one_year).\
        order_by(measurement.date).all()
    
    rain_totals = []
    for result in pre_scores:
        row = {}
        row["date"] = pre_scores[0]
        row["prcp"] = pre_scores[1]
        rain_totals.append(row)

    return jsonify(rain_totals)

@app.route("/api/v1.0/stations")

def stations():
    results = session.query(station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def temp_monthly():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(measurement.tobs).\
      filter(measurement.station == 'USC00519281').\
      filter(measurement.date >= one_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)




