#!/usr/bin/env python

#
# This file is part of CEP.
#
# CEP is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CEP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Leser General Public License
# along with CEP.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2016 Daniel Janke
#

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
initialEncodingTimes = []
coverCreationTimes = []
finalEncodingTimes = []
nHopReplicationTimes = []
statisticCollectionTimes = []
containmentAdjustmentTimes = []
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
    initialEncodingTimes.append(long(row[2])/1000/3600)
    coverCreationTimes.append(long(row[3])/1000/3600)
    finalEncodingTimes.append(long(row[4])/1000/3600)
    nHopReplicationTimes.append(long(row[5])/1000/3600)
    statisticCollectionTimes.append(long(row[6])/1000/3600)
    containmentAdjustmentTimes.append(long(row[7])/1000/3600)
    transferTimes.append(long(row[8])/1000/3600)
    indexingTimes.append(long(row[9])/1000/3600)

coverNames = np.array(coverNames)
initialEncodingTimes = np.array(initialEncodingTimes)
coverCreationTimes = np.array(coverCreationTimes)
finalEncodingTimes = np.array(finalEncodingTimes)
nHopReplicationTimes = np.array(nHopReplicationTimes)
statisticCollectionTimes = np.array(statisticCollectionTimes)
containmentAdjustmentTimes = np.array(containmentAdjustmentTimes)
transferTimes = np.array(transferTimes)
indexingTimes = np.array(indexingTimes)

N = len(coverNames)
ind = np.arange(N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, initialEncodingTimes, width, color='#cccccc')
p2 = plt.bar(ind, coverCreationTimes, width, color='#222222', bottom=initialEncodingTimes)
p3 = plt.bar(ind, finalEncodingTimes, width, color='#888888', bottom=coverCreationTimes+initialEncodingTimes)
p4 = plt.bar(ind, nHopReplicationTimes, width, color='#666666', bottom=finalEncodingTimes+coverCreationTimes+initialEncodingTimes)
p5 = plt.bar(ind, statisticCollectionTimes, width, color='#444444', bottom=nHopReplicationTimes+finalEncodingTimes+coverCreationTimes+initialEncodingTimes)
p6 = plt.bar(ind, containmentAdjustmentTimes, width, color='#aaaaaa', bottom=statisticCollectionTimes+nHopReplicationTimes+finalEncodingTimes+coverCreationTimes+initialEncodingTimes)
p7 = plt.bar(ind, transferTimes, width, color='#000000', bottom=containmentAdjustmentTimes+statisticCollectionTimes+nHopReplicationTimes+finalEncodingTimes+coverCreationTimes+initialEncodingTimes)
p8 = plt.bar(ind, indexingTimes, width, color='#ffffff', bottom=transferTimes+containmentAdjustmentTimes+statisticCollectionTimes+nHopReplicationTimes+finalEncodingTimes+coverCreationTimes+initialEncodingTimes)

plt.ylabel('Time (in h)')
plt.xticks(ind + width/2., coverNames)
plt.yticks(np.arange(0, 300, 10))
plt.legend((p8[0], p7[0], p6[0], p5[0], p4[0], p3[0], p2[0], p1[0]), ('indexing time', 'transfer time', 'containment adjustment time', 'statistics collection time', 'n-hop replication time', 'final encoding time', 'cover creation time', 'initial encoding time'), bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

plt.savefig(outputDir+'/loadingTimes.'+imageType, bbox_inches='tight')
