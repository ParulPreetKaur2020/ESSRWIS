from queringsql_tables import get_surfacedata
import random
import fisanalysis as fis
import matplotlib.pyplot as plt
import matplotlib as mpl

Surfacedata=get_surfacedata()
SurfaceC=Surfacedata[0][0]
SurfaceCond=SurfaceC.replace(" ", "")
SurfaceTemp=Surfacedata[0][1]

if (SurfaceCond== "Dry") & (SurfaceTemp >= "60"):
     SurfaceCondnumber = random.uniform(9.2, 10)
elif (SurfaceCond == "Dry") & (SurfaceTemp < "60"):
    SurfaceCondnumber = random.uniform(8.4, 9.1)
elif (SurfaceCond == "Trace Moisture") & (SurfaceTemp >= "60"):
    SurfaceCondnumber = random.uniform(7.5, 8.3)
elif (SurfaceCond == "Trace Moisture") & (SurfaceTemp < "60"):
    SurfaceCondnumber = random.uniform(6.7, 7.4)
elif (SurfaceCond == "Wet") & (SurfaceTemp >= "60"):
    SurfaceCondnumber = random.uniform(5.8, 6.6)
elif (SurfaceCond == "Wet") & (SurfaceTemp < "60"):
    SurfaceCondnumber = random.uniform(5, 5.7)
elif (SurfaceCond == "Chemically Wet") & (SurfaceTemp >= "15"):
    SurfaceCondnumber = random.uniform(4.1, 4.9)
elif (SurfaceCond == "Chemically Wet") & (SurfaceTemp < "15"):
    SurfaceCondnumber = random.uniform(3.3, 4)
elif (SurfaceCond == "Ice Watch") & (SurfaceTemp >= "15"):
    SurfaceCondnumber = random.uniform(2.4, 3.2)
elif (SurfaceCond == "Ice Watch") & (SurfaceTemp < "15"):
    SurfaceCondnumber = random.uniform(1.6, 2.3)
elif (SurfaceCond == "Ice Warning") & (SurfaceTemp >= "15"):
    SurfaceCondnumber = random.uniform(0.75, 1.5)
elif (SurfaceCond == "Ice Warning") & (SurfaceTemp < "15"):
    SurfaceCondnumber = random.uniform(0, 0.74)
else:
    SurfaceCondnumber = 'NaN'

rcd=fis.road_condition(SurfaceCondnumber,SurfaceTemp)
print(rcd)
mpl.rc('figure', max_open_warning=0)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(SurfaceCondnumber, SurfaceTemp, rcd, c='r', marker='o')
ax.set_xlabel('Surface condition')
ax.set_ylabel('Surface temp')
ax.set_zlabel('Slipperiness')

plt.show()