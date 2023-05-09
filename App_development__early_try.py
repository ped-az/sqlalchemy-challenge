#Import Dependencies
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import Session


#engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Base
Base = automap_base()
Base.prepare(autoload_with = engine)

#Referencing Tabels for both Station and Measurement
Station = Base.classes.station
Measurement = Base.classes.measurement

#Flask App
app = Flask(__name__)


@app.route('/')
def welcome():
    content = (
        "Welcome, these are all the available routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/stats/&lt;start_date&gt;<br/>"
        "/api/v1.0/stats/&lt;start_date&gt/&lt;end_date&gt<br/>"
    )
    return content






@app.route("/api/v1.0/stats/<start_date>")
@app.route("/api/v1.0/stats/<start_date>/<end_date>")
def stats(start_date, end_date=None):
    session = Session(engine)
    results = most_recent_date_str = session.query(func.max(Measurement.date)).first()[0]
    session.close()
    return f"{results}: {start_date} ;{end_date}"


if __name__ == '__main__':
    app.run(debug=True)



