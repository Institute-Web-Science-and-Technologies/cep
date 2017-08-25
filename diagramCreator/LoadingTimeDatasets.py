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
import latexPlot as latex
from operator import itemgetter

if len(sys.argv) != 4:
  print("You must have the following arguments: <loadingTime.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

#matplotlib.rcParams.update({'font.size': 20})

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
  rows = list();
  for row in reader:
    if int(row[1])!=20:
      continue;
    row[2]=long(row[2])
    rows.append(row);
  rows = sorted(rows,key=itemgetter(0,2));
  for row in rows:
    dataset = long(row[2])
    coverName = ""
    if int(row[3]) != 0:
      coverName += row[3] + "HOP\\_"
    coverName = "\\parbox{60pt}{\centering " + coverName + row[0].replace("HIERARCHICAL","HIER").replace('MIN_EDGE_CUT','MEC') + '\\\\' + (str(dataset/1000000000)+'G' if dataset/1000000000>0 else str(dataset/1000000)+'M') + ' triples' + '}'
    coverNames.append(coverName)
    initialEncodingTimes.append(long(row[4])/1000/3600)
    coverCreationTimes.append(long(row[5])/1000/3600)
    finalEncodingTimes.append(long(row[6])/1000/3600)
    nHopReplicationTimes.append(long(row[7])/1000/3600)
    statisticCollectionTimes.append(long(row[8])/1000/3600)
    containmentAdjustmentTimes.append(long(row[9])/1000/3600)
    transferTimes.append(long(row[10])/1000/3600)
    indexingTimes.append(long(row[11])/1000/3600)

coverNames = np.array(coverNames)
initialEncodingTimes = np.array(initialEncodingTimes)
coverCreationTimes = np.array(coverCreationTimes)
finalEncodingTimes = np.array(finalEncodingTimes)
nHopReplicationTimes = np.array(nHopReplicationTimes)
statisticCollectionTimes = np.array(statisticCollectionTimes)
containmentAdjustmentTimes = np.array(containmentAdjustmentTimes)
transferTimes = np.array(transferTimes)
indexingTimes = np.array(indexingTimes)

if imageType=="latex":
  latex.latexify(fig_height=10.1181104192)

N = len(coverNames)
fig, ax = plt.subplots()
#fig = plt.figure(figsize=(fig.get_figwidth()*3.2,fig.get_figheight()*3))
ind = np.arange(N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence


colormap = plt.cm.gist_ncar
colors = [colormap(i) for i in np.linspace(0, 0.9, 8)]

p1 = plt.bar(ind, initialEncodingTimes, width, color=colors[0], linewidth=0.5)
p2 = plt.bar(ind, coverCreationTimes, width, color=colors[1], bottom=initialEncodingTimes, linewidth=0.5)
p3 = plt.bar(ind, finalEncodingTimes, width, color=colors[2], bottom=coverCreationTimes+initialEncodingTimes, linewidth=0.5)
p4 = plt.bar(ind, nHopReplicationTimes, width, color=colors[3], bottom=finalEncodingTimes+coverCreationTimes+initialEncodingTimes, linewidth=0.5)
p5 = plt.bar(ind, statisticCollectionTimes, width, color=colors[4], bottom=nHopReplicationTimes+finalEncodingTimes+coverCreationTimes+initialEncodingTimes, linewidth=0.5)
p6 = plt.bar(ind, containmentAdjustmentTimes, width, color=colors[5], bottom=statisticCollectionTimes+nHopReplicationTimes+finalEncodingTimes+coverCreationTimes+initialEncodingTimes, linewidth=0.5)
p7 = plt.bar(ind, transferTimes, width, color=colors[6], bottom=containmentAdjustmentTimes+statisticCollectionTimes+nHopReplicationTimes+finalEncodingTimes+coverCreationTimes+initialEncodingTimes, linewidth=0.5)
p8 = plt.bar(ind, indexingTimes, width, color=colors[7], bottom=transferTimes+containmentAdjustmentTimes+statisticCollectionTimes+nHopReplicationTimes+finalEncodingTimes+coverCreationTimes+initialEncodingTimes, linewidth=0.5)

plt.ylabel('Time (in h)')
plt.xticks(ind + width/2., coverNames)
plt.yticks(np.arange(0, 2000, 24))
plt.legend((p8[0], p7[0], p6[0], p5[0], p3[0], p2[0], p1[0]), ('local index creation', 'transfer to slaves', 'join resp. adjustment', 'statistics collection', 'final dictionary encoding', 'cover creation', 'initial dictionary encoding'), bbox_to_anchor=(0, 1.002, 0.4, .102), loc=3, ncol=1, mode="expand", borderaxespad=0., borderpad=0.2, labelspacing=0.1)
plt.axis('tight')
if imageType=="latex":

  fig.tight_layout(rect=(-0.02,-0.015,1.025,0.91))

if imageType=="latex":
  latex.savefig(outputDir,'loadingTimesDatasets')
else:
  plt.savefig(outputDir+'/loadingTimesDatasets.'+imageType, bbox_inches='tight')
