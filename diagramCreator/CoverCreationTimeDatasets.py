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

if len(sys.argv) != 4:
  print("You must have the following arguments: <loadingTime.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

#matplotlib.rcParams.update({'font.size': 20})

coverCreationTimes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    if int(row[1])!=20:
      continue;
    coverName = ""
    if int(row[3]) != 0:
      coverName += row[3] + "HOP\\_"
    coverName = coverName + row[0].replace("_","\\_")
    scale = long(row[2]);
    if not coverName in coverCreationTimes.keys():
      coverCreationTimes[coverName] = {}
    coverCreationTimes[coverName][scale] = long(row[5])/1000./3600.

if imageType=="latex":
  #latex.latexify(fig_height=3,scale=0.85)
  latex.latexify(scale=1)

coverList = sorted(list(coverCreationTimes.keys()))
scaleList = sorted(list(coverCreationTimes[coverList[0]].keys()))

N = len(scaleList)
fig, ax = plt.subplots()
#fig = plt.figure(figsize=(fig.get_figwidth()*3.2,fig.get_figheight()*3))
ind = np.arange(N)    # the x locations for the groups
width = 1/float(1.+len(coverList))       # the width of the bars: can also be len(x) sequence


colormap = plt.cm.gist_ncar
colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverList)+1)]

for i, cover in enumerate(coverList):
  bar = []
  for scale in scaleList:
    bar.append(coverCreationTimes[cover][scale])
  plt.bar(ind+i*width-width, bar, width, color=colors[i+1], linewidth=0.5, label=cover, align="center")

plt.ylabel('Cover Creation Time (in h)')
plt.xlabel('Number of Triples')
ax.yaxis.set_label_coords(-0.1,0.4)
plt.xticks(ind, map(lambda x:str(x/1000000000)+'G' if x/1000000000>0 else str(x/1000000)+'M',scaleList))
plt.xlim([min(ind)-0.5,max(ind)+0.5])
#plt.yticks(np.arange(0, 936, 24))
#plt.legend(bbox_to_anchor=(0, 1.01, 0.4, .102), loc=3, ncol=1, mode="expand", borderaxespad=0.)
#plt.axis('tight')

if imageType=="latex":
  plt.legend(bbox_to_anchor=(-0.14, 1.08, 1.14, .102), loc=3, ncol=3, mode="expand", borderaxespad=0., borderpad=0.2, labelspacing=0.2, handletextpad=0.2, handlelength=1.0)
  fig.tight_layout(rect=(-0.04,-0.08,1.04,0.95))
  latex.savefig(outputDir,'coverCreationTimeDatasets')
else:
  plt.savefig(outputDir+'/coverCreationTimeDatasets.'+imageType, bbox_inches='tight')
