#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import csv

if len(sys.argv) != 4:
  print("You must have the following arguments: <loadingTime.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

coverNames = []
coverCreationTimes = []
encodingTimes = []
transferTimes = []
indexingTimes = []

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    coverName = ""
    if int(row[1]) != 0:
      coverName += row[1] + "HOP_"
    coverName += row[0]
    coverNames.append(coverName)
    coverCreationTimes.append(long(row[2])/1000)
    encodingTimes.append(long(row[3])/1000)
    transferTimes.append(long(row[4])/1000)
    indexingTimes.append(long(row[5])/1000)

coverNames = np.array(coverNames)
coverCreationTimes = np.array(coverCreationTimes)
encodingTimes = np.array(encodingTimes)
transferTimes = np.array(transferTimes)
indexingTimes = np.array(indexingTimes)

N = len(coverNames)
ind = np.arange(N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, coverCreationTimes, width, color='#222222')
p2 = plt.bar(ind, encodingTimes, width, color='#aaaaaa', bottom=coverCreationTimes)
p3 = plt.bar(ind, transferTimes, width, color='#666666', bottom=encodingTimes+coverCreationTimes)
p4 = plt.bar(ind, indexingTimes, width, color='#ffffff', bottom=transferTimes+encodingTimes+coverCreationTimes)

plt.ylabel('Time (in sec)')
plt.xticks(ind + width/2., coverNames)
plt.yticks(np.arange(0, 5000, 500))
plt.legend((p4[0], p3[0], p2[0], p1[0]), ('indexing time', 'transfer time', 'encoding time', 'cover creation time'))

plt.savefig(outputDir+'/loadingTimes.'+imageType, bbox_inches='tight')
