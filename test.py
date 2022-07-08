import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from getUnit import getUnits
from datetime import datetime, timedelta
from getTripsTest import getTripsTest
import json

units = getUnits()


# GEOFENCES RUTA COMBUSTIBLE PARA HIDROGEN
arrRutaPCh = []
for u in units['items']:
    unit = u['id']
    dfRutaPCh, dfRutaPoints = getTripsTest(unit)
    dfRutaPCh['nm'] = u['nm']
    arrRutaPCh.extend(dfRutaPCh.to_dict(orient='records'))
df = pd.DataFrame(arrRutaPCh)

# df1 RUTA REFERENCE_PALA - STK2
df1 = df.query('trip == "REFERENCE_PALA - STK2"').query('consumed < 60')
df2 = df.query('trip == "REFERENCE_PALA - CHANCADO I"').query('consumed < 55')
df3 = df.query('trip == "REFERENCE_PALA - STK7"').query('consumed < 100')
df4 = df.query('trip == "992 - WASTE1"').query('consumed > 24')

sns.scatterplot(data=df1, x='datetimeEnd', y='consumed', hue='nm')
sns.scatterplot(data=df2, x='datetimeEnd', y='consumed', hue='nm')
sns.scatterplot(data=df3, x='datetimeEnd', y='consumed', hue='nm')
sns.scatterplot(data=df4, x='datetimeEnd', y='consumed', hue='nm')

df1.to_csv('df1.csv', index=False)
df2.to_csv('df2.csv', index=False)
df3.to_csv('df3.csv', index=False)
df4.to_csv('df4.csv', index=False)

pd.set_option('display.max_rows', None)

# RESUMEN
