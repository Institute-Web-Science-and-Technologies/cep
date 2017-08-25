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

coverNames = []
coverCreationTimes = []

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    coverName = ""
    if int(row[2]) != 0:
      coverName += row[2] + "HOP\\_"
    coverName = "\\parbox{50pt}{\centering " + coverName + row[0].replace("HIERARCHICAL","HIER").replace('MIN_EDGE_CUT','MEC') + '\\\\' + row[1] + ' slaves}'
    coverNames.append(coverName)
    coverCreationTimes.append(long(row[4])/1000./3600.)

coverNames = np.array(coverNames)
coverCreationTimes = np.array(coverCreationTimes)

if imageType=="latex":
  latex.latexify(fig_height=3,scale=0.85)

N = len(coverNames)
fig, ax = plt.subplots()
#fig = plt.figure(figsize=(fig.get_figwidth()*3.2,fig.get_figheight()*3))
ind = np.arange(N)    # the x locations for the groups
width = 0.5       # the width of the bars: can also be len(x) sequence


colormap = plt.cm.gist_ncar
colors = [colormap(i) for i in np.linspace(0, 0.9, 8)]

p2 = plt.bar(ind, coverCreationTimes, width, color=colors[1], linewidth=0.5, label='cover creation', align="center")

plt.ylabel('Time (in h)')
plt.xticks(ind, coverNames)
plt.xlim([min(ind)-0.5,max(ind)+0.5,])
#plt.yticks(np.arange(0, 936, 24))
#plt.legend(bbox_to_anchor=(0, 1.01, 0.4, .102), loc=3, ncol=1, mode="expand", borderaxespad=0.)
#plt.axis('tight')
if imageType=="latex":
  fig.tight_layout(rect=(-0.025,-0.045,1.026,1.045))

if imageType=="latex":
  latex.savefig(outputDir,'coverCreationTime')
else:
  plt.savefig(outputDir+'/coverCreationTime.'+imageType, bbox_inches='tight')
