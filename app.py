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
    df3 = pd.read_csv('df3.csv')
    df4 = pd.read_csv('df4.csv')
    # convertir a json
    df1_json = df1.to_dict(orient='records')
    df2_json = df2.to_dict(orient='records')
    df3_json = df3.to_dict(orient='records')
    df4_json = df4.to_dict(orient='records')
    return jsonify({'df1': df1_json, 'df2': df2_json, 'df3': df3_json, 'df4': df4_json})


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
    df = pd.DataFrame(arrRutaPCh)
    df1 = df.query('trip == "REFERENCE_PALA - STK2"').query('consumed < 60')
    df2 = df.query(
        'trip == "REFERENCE_PALA - CHANCADO I"').query('consumed < 55')
    df3 = df.query('trip == "REFERENCE_PALA - STK7"').query('consumed < 100')
    df4 = df.query('trip == "992 - WASTE1"').query('consumed > 24')

    df1.to_csv('df1.csv', index=False)
    df2.to_csv('df2.csv', index=False)
    df3.to_csv('df3.csv', index=False)
    df4.to_csv('df4.csv', index=False)

    df1_json = df1.to_dict(orient='records')
    df2_json = df2.to_dict(orient='records')
    df3_json = df3.to_dict(orient='records')
    df4_json = df4.to_dict(orient='records')
    return jsonify({'df1': df1_json, 'df2': df2_json, 'df3': df3_json, 'df4': df4_json})


if (__name__ == "__main__"):
    app.run(debug=True)
