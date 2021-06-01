
#-------------
# Module import
#-------------

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#---------------
# Database Setup
#---------------

engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)

# Store class tables in obj
Station = Base.classes.station
Measurement = Base.classes.measurement

# Initialize Flask app
app = Flask(__name__)

#---------------
# Flask Routes
#---------------


@app.route('/')
def home() :
    """List all available api routes"""
    return (
        f'Available Routes:<br/><br/>'
        f'Rainfall Data:<br/> /api/v1.0/precipitation<br/><br/>'
        f'Station Information:<br/> /api/v1.0/stations<br/><br/>'
        f'Temperature Observed from start date:<br/> /api/v1.0/YYYY-mm-dd<br/><br/>'
        f'Temperature Observed from date range:<br/> /api/v1.0/YYYY-mm-dd/YYYY-mm-dd<br/><br/>'
    )


@app.route('/api/v1.0/precipitation')
def prcp() :
    try :
        #connect to engine
        session = Session(engine)

        #query session for data
        dates = session.query(Measurement.date).all()
        prcp = session.query(Measurement.prcp).all()

        #disconnect
        session.close()
    except :
        return jsonify({'Session / Query Error',})

    try :
        #restructure the response to fit into a dictionary
        dateList = list(np.ravel(dates))
        prcpList = list(np.ravel(prcp))
        prcpDict = dict(zip(dateList,prcpList))

        #generate response from dictionary obj
        return jsonify(prcpDict)
    except :
        return jsonify({'Data Transform error'},)
        

@app.route('/api/v1.0/stations')
def station() :
    try :  
        #connect to engine
        session = Session(engine)

        #query session for data
        stations = session.query(Station.name).all()

        #disconnect
        session.close()
    except : 
        return jsonify({'Session / Query Error',})

    return jsonify(list(np.ravel(stations)))
    
@app.route('/api/v1.0/tobs')
def tobs() :
    try : 
        #connect to engine
        session = Session(engine)

        #Queries

        # Most Recent day in data set
        dateRecent = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

        # Date one year ago from most recent date in data set
        query_date = dt.date(int(dateRecent[0:4]), int(dateRecent[5:7]), int(dateRecent[8:10])) - dt.timedelta(days=365)

        # Most active station in frequency of reporting of percipitation
        activeStation = session.query(Measurement.station)\
                        .group_by(Measurement.station)\
                        .order_by(func.count(Measurement.prcp).desc())\
                        .first()
        # Observed temp at most active station
        stationTOBS = session.query(Measurement.tobs)\
                        .filter(Measurement.date >= query_date)\
                        .filter(Measurement.station == activeStation[0])\
                        .all()

        #disconnect
        session.close()
        
    except : 
        return jsonify({'Session / Query Error'})
    
    #return the temp obs for the station
    return jsonify(list(np.ravel(stationTOBS)))
    
@app.route(f'/api/v1.0/<start>')
def tempStart(start) :
    try :
        #Connect to engine
        session = Session(engine)
        
        # Most active station in frequency of reporting of percipitation
        activeStation = session.query(Measurement.station)\
                        .group_by(Measurement.station)\
                        .order_by(func.count(Measurement.prcp).desc())\
                        .first()
            
        #Query session for temp data
        tempMin, tempMax, tempAvg = session.query(func.min(Measurement.tobs),
                                                 func.max(Measurement.tobs),
                                                 func.avg(Measurement.tobs))\
                                                    .filter(Measurement.date >= start)\
                                                    .filter(Measurement.station == activeStation[0])\
                                                    .all()[0]
        session.close()
        
    except : 
        return jsonify({'Session / Query Error',})
    
    return {'Minimum Tobs':tempMin,'Maximum Tobs':tempMax,'Average Tobs':tempAvg}
    
    
@app.route(f'/api/v1.0/<start>/<end>')
def tempRange(start,end) :
    try :
        #Connect to engine
        session = Session(engine)
        
        # Most active station in frequency of reporting of percipitation
        activeStation = session.query(Measurement.station)\
                        .group_by(Measurement.station)\
                        .order_by(func.count(Measurement.prcp).desc())\
                        .first()
            
        #Query session for temp data
        tempMin, tempMax, tempAvg = session.query(func.min(Measurement.tobs),
                                                 func.max(Measurement.tobs),
                                                 func.avg(Measurement.tobs))\
                                                    .filter(Measurement.date >= start)\
                                                    .filter(Measurement.date <= end)\
                                                    .filter(Measurement.station == activeStation[0])\
                                                    .all()[0]
        session.close()
        
    except : 
        return jsonify({'Session / Query Error',})
    
    return {'Minimum Tobs':tempMin,'Maximum Tobs':tempMax,'Average Tobs':tempAvg}
    
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)