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
from itertools import cycle

if len(sys.argv) != 4:
  print("You must have the following arguments: <computationalEffort.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

queries = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[2]) != 0:
      cover += row[2] + "HOP_"
    cover += row[0]
    scale = row[1]
    treeType = row[3]
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " #tp=" + str(int(row[6])+1) + " #ds=" + row[7] + " sel=" + row[8]
    row2 = reader.next();
    row = row[9:len(row)]
    row_time = []
    row_time.append(0)
    for time in row:
      row_time.append((long(time)-1)/float(1000))
      row_time.append(long(time)/float(1000))
    row2 = row2[9:len(row2)]
    row_percent = []
    row_percent.append(0)
    previous = 0
    for percent in row2:
      row_percent.append(previous)
      previous = float(percent)
      row_percent.append(previous)
    if not query in queries.keys():
      queries[query] = {}
    if not cover in queries[query].keys():
      queries[query][cover] = {}
    if not treeType in queries[query][cover].keys():
      queries[query][cover][treeType] = {}
    queries[query][cover][treeType][scale] = { 'time':row_time, 'percent':row_percent}

for query in sorted(queries.keys()):
  for cover in sorted(queries[query].keys()):
    for treeType in sorted(queries[query][cover].keys()):
      # create diagram
      fig, ax = plt.subplots()
      scaleSet = sorted(queries[query][cover][treeType].keys())
      colormap = plt.cm.gist_ncar
      colors = [colormap(i) for i in np.linspace(0, 0.9, len(scaleSet)+1)]
      for i, scale in enumerate(scaleSet):
        colorValue = colors[i+1]
        plt.plot(queries[query][cover][treeType][scale]['time'], queries[query][cover][treeType][scale]['percent'], label=scale+' chunks', color=colorValue, linewidth=5)
      plt.title(query + ' for ' + treeType + ' trees and '+cover+' cover',y=1.02)
      plt.xlabel("Time (in sec)")
      plt.ylabel("Percentage of returned results")
      plt.axis('tight')
      plt.legend(loc='upper left', ncol=len(sorted(queries[query][cover][treeType].keys())), bbox_to_anchor=(0., -0.2, 1., .102))
      plt.savefig(outputDir+'/resultsOverTime_'+query + '_cover-'+ cover + '_'+treeType +'.'+imageType, bbox_inches='tight')
      plt.close(fig)

