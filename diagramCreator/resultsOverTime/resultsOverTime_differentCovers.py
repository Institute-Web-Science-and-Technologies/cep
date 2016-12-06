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
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " tree=" + ("ll" if row[3]=='LEFT_LINEAR' else ("rl" if row[3]=='RIGHT_LINEAR' else "b")) + " #tp=" + str(int(row[6])+1) + " #ds=" + row[7] + " sel=" + row[8]
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
    if not scale in queries[query].keys():
      queries[query][scale] = {}
    queries[query][scale][cover] = { 'time':row_time, 'percent':row_percent}

# create diagram per cover
for query in sorted(queries.keys()):
  for scale in sorted(queries[query].keys()):
    fig, ax = plt.subplots()
    coverSet = sorted(queries[query][scale].keys())
    colormap = plt.cm.gist_ncar
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)+1)]
    for i, cover in enumerate(coverSet):
      colorValue = colors[i+1]
      plt.plot(queries[query][scale][cover]['time'], queries[query][scale][cover]['percent'], label=cover, color=colorValue, linewidth=5)
    plt.title(query + " for " + scale + " chunks")
    plt.xlabel("Time (in sec)")
    plt.ylabel("Percentage of returned results")
    plt.axis('tight')
    plt.legend(loc='upper left', ncol=len(sorted(queries[query].keys())), bbox_to_anchor=(0., -0.2, 1., .102))
    plt.savefig(outputDir+'/resultsOverTime_'+query+'_'+scale+'chunks'+'.'+imageType, bbox_inches='tight')
    plt.close(fig)

