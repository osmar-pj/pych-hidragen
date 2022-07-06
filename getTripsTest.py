import pandas as pd
from main import login
from getResource import getResources
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

"""
 [{'nm': 'CAM-101', 'cls': 2, 'id': 9925, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'CAM-115', 'cls': 2, 'id': 9931, 'mu': 3, 'uacl': 19327369763},
  {'nm': 'CAM-121', 'cls': 2, 'id': 9919, 'mu': 3, 'uacl': 19327369763}]
"""

resources = getResources()

# start = datetime(2022, 5, 22)
# end = datetime.now()
# unit = 10293


def getTripsTest(unit):
    end = datetime.now()
    start = datetime(2022, 6, 20)
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 8,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 0
        }
    }
    reports = sdk.report_exec_report(paramsExecReport)

    # TRIPS
    # 6 TripsMine2Lima
    paramsRutaPCh = {
        'tableIndex': 0,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][0]['rows']
    }
    paramsRutaPoints = {
        'tableIndex': 1,
        'indexFrom': 0,
        'indexTo': reports['reportResult']['tables'][1]['rows']
    }

    rowsRutaPCh = sdk.report_get_result_rows(paramsRutaPCh)
    dataRutaPCh = [r['c'] for r in rowsRutaPCh]
    dfRutaPCh = pd.DataFrame(dataRutaPCh)

    rowsRutaPoints = sdk.report_get_result_rows(paramsRutaPoints)
    dataRutaPoints = [r['c'] for r in rowsRutaPoints]
    dfRutaPoints = pd.DataFrame(dataRutaPoints)

    dfRutaPCh.rename(columns={0: 'parkingDuration', 1: 'tripDuration', 2: 'ratio', 3: 'trip', 4: 'tripFrom', 5: 'tripTo', 6: 'datetimeBegin', 7: 'datetimeEnd',
                              8: 'mileage', 9: 'tripDurationTime', 10: 'parkingDurationTime', 11: 'avgSpeed', 12: 'maxSpeed', 13: 'consumed', 14: 'avgConsumed'}, inplace=True)
    dfRutaPCh['parkingDuration'] = pd.to_numeric(
        dfRutaPCh['parkingDuration'], errors='coerce')
    dfRutaPCh['tripDuration'] = pd.to_numeric(
        dfRutaPCh['tripDuration'], errors='coerce')
    dfRutaPCh['ratio'] = dfRutaPCh['ratio'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPCh['mileage'] = dfRutaPCh['mileage'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPCh['avgSpeed'] = dfRutaPCh['avgSpeed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPCh['maxSpeed'] = dfRutaPCh['maxSpeed'].apply(
        lambda x: x['t'].split(' ')[0]).astype(int)
    dfRutaPCh['consumed'] = dfRutaPCh['consumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPCh['avgConsumed'] = dfRutaPCh['avgConsumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPCh['timestampBegin'] = dfRutaPCh['datetimeBegin'].apply(
        lambda x: x['v'])
    dfRutaPCh['datetimeBegin'] = pd.to_datetime(
        dfRutaPCh['datetimeBegin'].apply(lambda x: x['t']))
    dfRutaPCh['timestampEnd'] = dfRutaPCh['datetimeEnd'].apply(
        lambda x: x['v'])
    dfRutaPCh['datetimeEnd'] = pd.to_datetime(
        dfRutaPCh['datetimeEnd'].apply(lambda x: x['t']))

    dfRutaPoints.rename(columns={0: 'parkingDuration', 1: 'tripDuration', 2: 'ratio', 3: 'trip', 4: 'tripFrom', 5: 'tripTo', 6: 'datetimeBegin', 7: 'datetimeEnd',
                                 8: 'mileage', 9: 'tripDurationTime', 10: 'parkingDurationTime', 11: 'avgSpeed', 12: 'maxSpeed', 13: 'consumed', 14: 'avgConsumed'}, inplace=True)
    dfRutaPoints['parkingDuration'] = pd.to_numeric(
        dfRutaPoints['parkingDuration'], errors='coerce')
    dfRutaPoints['tripDuration'] = pd.to_numeric(
        dfRutaPoints['tripDuration'], errors='coerce')
    dfRutaPoints['ratio'] = dfRutaPoints['ratio'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPoints['mileage'] = dfRutaPoints['mileage'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPoints['avgSpeed'] = dfRutaPoints['avgSpeed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPoints['maxSpeed'] = dfRutaPoints['maxSpeed'].apply(
        lambda x: x['t'].split(' ')[0]).astype(int)
    dfRutaPoints['consumed'] = dfRutaPoints['consumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPoints['avgConsumed'] = dfRutaPoints['avgConsumed'].apply(
        lambda x: x.split(' ')[0]).astype(float)
    dfRutaPoints['timestampBegin'] = dfRutaPoints['datetimeBegin'].apply(
        lambda x: x['v'])
    dfRutaPoints['datetimeBegin'] = pd.to_datetime(
        dfRutaPoints['datetimeBegin'].apply(lambda x: x['t']))
    dfRutaPoints['timestampEnd'] = dfRutaPoints['datetimeEnd'].apply(
        lambda x: x['v'])
    dfRutaPoints['datetimeEnd'] = pd.to_datetime(
        dfRutaPoints['datetimeEnd'].apply(lambda x: x['t']))

    return dfRutaPCh, dfRutaPoints

# pd.set_option('display.max_rows', None)
