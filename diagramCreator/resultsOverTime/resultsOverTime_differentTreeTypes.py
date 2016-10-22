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
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    treeType = row[2]
    query = ("ss" if row[4]=='SUBJECT_SUBJECT_JOIN' else "so") + " #j=" + row[5] + " #ds=" + row[6] + " sel=" + row[7]
    row2 = reader.next();
    row = row[8:len(row)]
    row_time = []
    row_time.append(0)
    for time in row:
      row_time.append((long(time)-1)/1000)
      row_time.append(long(time)/1000)
    row2 = row2[8:len(row2)]
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
    queries[query][cover][treeType] = { 'time':row_time, 'percent':row_percent}

lines = ["-","--","-.",":"]

for query in sorted(queries.keys()):
  for cover in sorted(queries[query].keys()):
    # create diagram
    fig, ax = plt.subplots()
    treeTypeSet = sorted(queries[query][cover].keys())
    colorBase = 1 / float(len(treeTypeSet)+1)
    linecycler = cycle(lines)
    for i, treeType in enumerate(treeTypeSet):
      colorValue = "{:f}".format(colorBase*(i+0.5))
      plt.plot(queries[query][cover][treeType]['time'], queries[query][cover][treeType]['percent'], label=treeType, color=colorValue, linestyle=next(linecycler))
    plt.title(query + ' for ' + cover + ' cover')
    plt.xlabel("Time (in sec)")
    plt.ylabel("Percentage of returned results")
    plt.axis('tight')
    plt.legend(loc='upper left', ncol=len(sorted(queries[query][cover].keys())), bbox_to_anchor=(0., -0.2, 1., .102))
    plt.savefig(outputDir+'/resultsOverTime_'+query + '_cover-'+ cover +'.'+imageType, bbox_inches='tight')
    plt.close(fig)

