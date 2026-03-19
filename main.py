# Imports a CVS from a Columbus P-10 Pro GPS-Logger, calculates a height profile showing it with matplotlib.
# Example files in the map "CSV"

import csv
import math
import numpy
import matplotlib.pyplot as plt
import matplotlib.ticker

# To draw plane coordinates
from shapely.geometry import LineString
import geopandas as gpd


# For raw data
rows = []

# For calculation
dandh = []

# Average Earth radius in meters
R = 6371000.0

# Load a CSV file
with open("CSV/13153001.CSV", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        rows.append(row)

# for row in rows[:5]: print(row) # for control

# Remove trailing chars
for row in rows[1:]:
    row[4] = row[4][:-1]
    row[5] = row[5][:-1]

# for row in rows[:5]: print(row) # for control

# Compute length between points
for index in range(len(rows[:-2])):
    if index == 0:
        dandh.append([0.0, float(rows[index + 1][6])])
    else:
        dla = math.radians(float(rows[index + 2][4]) - float(rows[index + 1][4]))
        dlo = math.radians(float(rows[index + 2][5]) - float(rows[index + 1][5]))

        a = (math.sin(dla/2)**2 +
             math.cos(float(rows[index + 1][4])) *
             math.cos(float(rows[index + 2][4])) *
             math.sin(dlo/2)**2)



        b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * b
        # Filter out length of zero and append data
        if distance > 0.0:
            dandh.append([distance, float(rows[index + 1][6])])

# Just print the data
for row in dandh[:5]:print(row)
print('----')

# Calculate length from first point on path
for index in range(1, len(dandh)):
        dandh[index][0] = dandh[index][0] + dandh[index - 1][0]

# Just print the data
for row in dandh[:5]:print(row)

# Package it for numpy
distance = numpy.array([value[0] for value in dandh])
elevation = numpy.array([value[1] for value in dandh])

# Make subplot
fig, (ax1, ax2) = plt.subplots(1, 2
                               , layout='constrained')

fig.suptitle('Height profile and path')

# Visualise the data
ax1.plot(distance, elevation)

# Draw plane
coords = [(float(row[5]), float(row[4])) for row in rows[1:]]
gdf = gpd.GeoDataFrame(geometry=[LineString(coords)], crs="EPSG:4326")
gdf.plot(ax=ax2)


ax2.relim()
ax2.autoscale_view()

plt.show()