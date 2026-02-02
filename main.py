# Imports a CVS from a Columbus P-10 Pro GPS-Logger, calculates a hight profile showing it with matplotlib.
# Example files in the map "CSV"

import csv
import math
import numpy
import matplotlib.pyplot
import matplotlib.ticker

rows = []
dandh = []
R = 6371000.0 # meters

with open("CSV/13141948.CSV", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        rows.append(row)

# for row in rows[:5]: print(row) # control

for row in rows[1:]:
    row[4] = row[4][:-1]
    row[5] = row[5][:-1]

# for row in rows[:5]: print(row) # control

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

        if distance > 0.0: #dont add lengths of zero
            dandh.append([distance, float(rows[index + 1][6])])

for row in dandh[:5]:print(row)
print('----')

for index in range(1, len(dandh)):
        dandh[index][0] = dandh[index][0] + dandh[index - 1][0]

for row in dandh[:5]:print(row)

distance = numpy.array([value[0] for value in dandh])
elevation = numpy.array([value[1] for value in dandh])

matplotlib.pyplot.plot(distance, elevation)
matplotlib.pyplot.show()

