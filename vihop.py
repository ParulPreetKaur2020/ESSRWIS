import numpy as np
import pandas as pd
import fisanalysis as fis
import matplotlib.pyplot as plt
import matplotlib as mpl
from database_connection import cursor, connection
import time

df = pd.read_csv('rwis2019.csv')

SURFACE_COND_NO = pd.Series([], dtype=pd.StringDtype())

for i, row in df.iterrows():
    if (df['SURFACE_CONDITION'][i] == "Dry") & (df['SURFACE_TEMP'][i] >= 60):
        SURFACE_COND_NO[i] = np.random.uniform(9.2, 10)
    elif (df['SURFACE_CONDITION'][i] == "Dry") & (df['SURFACE_TEMP'][i] < 60):
        SURFACE_COND_NO[i] = np.random.uniform(8.4, 9.1)
    elif (df['SURFACE_CONDITION'][i] == "Trace Moisture") & (df['SURFACE_TEMP'][i] >= 60):
        SURFACE_COND_NO[i] = np.random.uniform(7.5, 8.3)
    elif (df['SURFACE_CONDITION'][i] == "Trace Moisture") & (df['SURFACE_TEMP'][i] < 60):
        SURFACE_COND_NO[i] = np.random.uniform(6.7, 7.4)
    elif (df['SURFACE_CONDITION'][i] == "Wet") & (df['SURFACE_TEMP'][i] >= 60):
        SURFACE_COND_NO[i] = np.random.uniform(5.8, 6.6)
    elif (df['SURFACE_CONDITION'][i] == "Wet") & (df['SURFACE_TEMP'][i] < 60):
        SURFACE_COND_NO[i] = np.random.uniform(5, 5.7)
    elif (df['SURFACE_CONDITION'][i] == "Chemically Wet") & (df['SURFACE_TEMP'][i] >= 15):
        SURFACE_COND_NO[i] = np.random.uniform(4.1, 4.9)
    elif (df['SURFACE_CONDITION'][i] == "Chemically Wet") & (df['SURFACE_TEMP'][i] < 15):
        SURFACE_COND_NO[i] = np.random.uniform(3.3, 4)
    elif (df['SURFACE_CONDITION'][i] == "Ice Watch") & (df['SURFACE_TEMP'][i] >= 15):
        SURFACE_COND_NO[i] = np.random.uniform(2.4, 3.2)
    elif (df['SURFACE_CONDITION'][i] == "Ice Watch") & (df['SURFACE_TEMP'][i] < 15):
        SURFACE_COND_NO[i] = np.random.uniform(1.6, 2.3)
    elif (df['SURFACE_CONDITION'][i] == "Ice Warning") & (df['SURFACE_TEMP'][i] >= 15):
        SURFACE_COND_NO[i] = np.random.uniform(0.75, 1.5)
    elif (df['SURFACE_CONDITION'][i] == "Ice Warning") & (df['SURFACE_TEMP'][i] < 15):
        SURFACE_COND_NO[i] = np.random.uniform(0, 0.74)
    else:
        SURFACE_COND_NO[i] = 'NaN'

print(df)
df.insert(4, "SURFACE_COND_NO", round(SURFACE_COND_NO, 3))

dft = df.loc[:, ['SURFACE_CONDITION', 'SURFACE_TEMP', 'SURFACE_COND_NO']]

#print(dft)


road_cond = []

for i, row in df.iterrows():
    sc = df['SURFACE_COND_NO']
    st = df['SURFACE_TEMP']
    rcd = fis.road_condition(sc[i], st[i])
    mpl.rc('figure', max_open_warning=0)
    road_cond.append(rcd)
    coefficient = round(road_cond[i], 2)
    if (coefficient < 0.3):
        postgreSQL_insert_RC = 'UPDATE public."RoadConditions" SET "µ(slipperycoefficient)"=%s where "Road_Condition"=%s'
        cursor.execute(postgreSQL_insert_RC, (coefficient, "Very Slippery"))
    elif (0.3 <= coefficient < 0.5):
        postgreSQL_insert_RC = 'UPDATE public."RoadConditions" SET "µ(slipperycoefficient)"=%s where "Road_Condition"=%s'
        cursor.execute(postgreSQL_insert_RC, (coefficient, "Slippery"))
    elif (coefficient >= 0.5):
        postgreSQL_insert_RC = 'UPDATE public."RoadConditions" SET "µ(slipperycoefficient)"=%s where "Road_Condition"=%s'
        cursor.execute(postgreSQL_insert_RC, (coefficient, "Normal"))
    connection.commit()
    time.sleep(5)
    #print(sc[i], st[i], round(road_cond[i], 2))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(sc, st, road_cond, c='r', marker='o')
ax.set_xlabel('Surface condition')
ax.set_ylabel('Surface temp')
ax.set_zlabel('Slipperiness')

plt.show()
