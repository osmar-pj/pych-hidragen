import pandas as pd
from main import login
from datetime import datetime, timedelta
from getUnit import getUnits
from getResource import getResources
import locale
locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

start = datetime(2022, 7, 1)
end = datetime.now()

# def getResumenByDia(start, end):
sdk = login()
units = getUnits()
resources = getResources()
parameterSetLocale = {
    'tzOffset': -18000,
    "language": "en"
}
sdk.render_set_locale(parameterSetLocale)
# end = (datetime.now() - timedelta(days=1)).timestamp()
# unit = 9919  # CAM 121
resumen = []
unit = 25642778
# for unit in units['items']:
paramsExecReport = {
    'reportResourceId': resources['items'][0]['id'],
    'reportTemplateId': 3,
    'reportObjectId': unit,
    'reportObjectSecId': 0,
    'reportObjectIdList': 0,
    'interval': {
        'from': int(start.timestamp()),
        'to': int(end.timestamp()),
        'flags': 0
    }
}
reports = sdk.report_exec_report(paramsExecReport)
paramsSummary = {
    'tableIndex': 0,
    'indexFrom': 0,
    'indexTo': reports['reportResult']['tables'][0]['rows']
}
rows = sdk.report_get_result_rows(paramsSummary)
dataSummary = [r['c'] for r in rows]
dfSummary = pd.DataFrame(dataSummary)

dfSummary.rename(columns={0: 'group', 1: 'ratio', 2: 'parkingHours', 3: 'engineHours',
                 4: 'utilizacionEfec', 5: 'mileage', 6: 'avgSpeed', 7: 'maxSpeed', 8: 'moveTime', 9: 'engineTime', 10: 'parking', 11: 'consumed', 12: 'avgConsumed'}, inplace=True)
dfSummary['datetime'] = pd.to_datetime(dfSummary['group'])
dfSummary['ratio'] = dfSummary['ratio'].apply(
    lambda x: x.split(' ')[0]).astype(float)
dfSummary['parkingHours'] = dfSummary['parkingHours'].apply(
    lambda x: x.split(' ')[0]).astype(float)
dfSummary['engineHours'] = dfSummary['engineHours'].apply(
    lambda x: x.split(' ')[0]).astype(float)
dfSummary['utilizacionEfec'] = dfSummary['utilizacionEfec'].apply(
    lambda x: x.split(' ')[0]).astype(float)
dfSummary['mileage'] = dfSummary['mileage'].apply(
    lambda x: x.split(' ')[0]).astype(float)
dfSummary['avgSpeed'] = dfSummary['avgSpeed'].apply(
    lambda x: x.split(' ')[0]).astype(float)
dfSummary['maxSpeed'] = dfSummary['maxSpeed'].apply(
    lambda x: x['t'].split(' ')[0] if x != '0 km/h' else 0).astype(float)
dfSummary['consumed'] = dfSummary['consumed'].apply(
    lambda x: x.split(' ')[0]).astype(float)
dfSummary['avgConsumed'] = dfSummary['avgConsumed'].apply(
    lambda x: x.split(' ')[0]).astype(float)

paramsGeofences = {
    'tableIndex': 1,
    'indexFrom': 0,
    'indexTo': reports['reportResult']['tables'][1]['rows']
}
rowsGeofences = sdk.report_get_result_rows(paramsGeofences)
dataGeofences = [r['c'] for r in rowsGeofences]
dfGeofences = pd.DataFrame(dataGeofences)

# return dfSummary, dfGeofences
# sdk.logout()
