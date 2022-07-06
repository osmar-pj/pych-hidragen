import pandas as pd
from flask import Flask, jsonify, Request
from flask_cors import CORS
from datetime import datetime, timedelta

from getTripsTest import getTripsTest
from getUnit import getUnits


app = Flask(__name__)
cors = CORS(app)

units = getUnits()


@app.route('/api/v1/getTripsByGeofences', methods=['GET'])
def getTripsByGeofences():
    # leer archivo csv con pandas
    df1 = pd.read_csv('df1.csv')
    df2 = pd.read_csv('df2.csv')
    # convertir a json
    df1_json = df1.to_dict(orient='records')
    df2_json = df2.to_dict(orient='records')
    return jsonify({'df1': df1_json, 'df2': df2_json})


@app.route('/api/v1/updateTripsByGeofences', methods=['GET'])
def updateTripsByGeofences():
    w = 1
    # start 20 de junio

    arrRutaPCh = []
    arrRutaPoints = []
    for u in units['items']:
        unit = u['id']
        dfRutaPCh, dfRutaPoints = getTripsTest(unit)
        dfRutaPCh['nm'] = u['nm']
        dfRutaPoints['nm'] = u['nm']
        arrRutaPCh.extend(dfRutaPCh.to_dict(orient='records'))
        arrRutaPoints.extend(dfRutaPoints.to_dict(orient='records'))
    dfRutaPCh = pd.DataFrame(arrRutaPCh)
    dfRutaPoints = pd.DataFrame(arrRutaPoints)
    df1 = dfRutaPCh.query(
        'tripFrom == "REFERENCE_PALA"').query('consumed < 50')
    df2 = dfRutaPoints.query('tripFrom == "POINT_A"').query('consumed > 8')

    df1.to_csv('df1.csv', index=False)
    df2.to_csv('df2.csv', index=False)
    df1_json = df1.to_dict(orient='records')
    df2_json = df2.to_dict(orient='records')
    return jsonify({'df1': df1_json, 'df2': df2_json})


if (__name__ == "__main__"):
    app.run(debug=True)
