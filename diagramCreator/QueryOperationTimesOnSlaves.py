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
  print("You must have the following arguments: <operationTimesPerSlave.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

# required map: cover -> chunk -> value

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
    scale = int(row[1]);
    treeType = row[3]
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " #tp=" + str(int(row[6])+1) + " #ds=" + row[7] + " sel=" + row[8]
    if not query in queries:
      queries[query] = {}
    if not scale in queries[query]:
      queries[query][scale] = {}
    if not treeType in queries[query][scale]:
      queries[query][scale][treeType] = {}
    if not cover in queries[query][scale][treeType]:
      queries[query][scale][treeType][cover] = {}
    for i in range(len(row)-1):
      if i >= 9 and (i-9)%4==0:
        slave = row[i]
        operation = row[i+1]
        start = long(row[i+2])/1000
        time = long(row[i+3])/1000
        if not operation in queries[query][scale][treeType][cover]:
          queries[query][scale][treeType][cover][operation] = {}
        if not slave in queries[query][scale][treeType][cover][operation]:
          queries[query][scale][treeType][cover][operation][slave] = {}
        queries[query][scale][treeType][cover][operation][slave]['start time'] = start
        queries[query][scale][treeType][cover][operation][slave]['execution time'] = time
        queries[query][scale][treeType][cover][operation][slave]['total time'] = long(row[len(row)-1])/1000

for measurementType in ["Execution Time"]:
  querySet = list(sorted(queries.keys()))
  scaleSet = list(sorted(queries[querySet[0]].keys()))
  treeTypeSet = list(sorted(queries[querySet[0]][scaleSet[0]].keys()))
  coverSet = list(sorted(queries[querySet[0]][scaleSet[0]][treeTypeSet[0]].keys()))
  dataRows = {}
  for i, query in enumerate(querySet):
    dataRows[query] = {}
    for j, scale in enumerate(scaleSet):
      dataRows[query][scale] = {}
      for k, treeType in enumerate(treeTypeSet):
        dataRows[query][scale][treeType] = {}
        for l, cover in enumerate(coverSet):
          dataRows[query][scale][treeType][cover] = {}
          for m, operation in enumerate(list(sorted(queries[query][scale][treeType][cover].keys()))):
            dataRows[query][scale][treeType][cover][operation] = {'start time' : [], 'execution time' : [], 'total time' : 0}
            for n, slave in enumerate(queries[query][scale][treeType][cover][operation]):
                dataRows[query][scale][treeType][cover][operation]['start time'].append(queries[query][scale][treeType][cover][operation][slave]['start time']);
                dataRows[query][scale][treeType][cover][operation]['execution time'].append(queries[query][scale][treeType][cover][operation][slave]['execution time']);
                dataRows[query][scale][treeType][cover][operation]['total time'] = queries[query][scale][treeType][cover][operation][slave]['total time'];

  # create diagramms per treeType
  for i, query in enumerate(querySet):
    for j, scale in enumerate(scaleSet):
      for k, treeType in enumerate(treeTypeSet):
        for l, cover in enumerate(coverSet):
          operationSet = list(sorted(queries[query][scale][treeType][cover].keys(),key=queries[query][scale][treeType][cover].__getitem__))
          slaveSet = list(sorted(queries[query][scale][treeType][cover][operationSet[0]].keys()));
          n_groups = scale
          fig, ax = plt.subplots()
          fig2 = plt.figure(figsize=(fig.get_figwidth()*(scale/20.)*(len(operationSet)/4),5))
          index = np.arange(n_groups)
          bar_width = 1/float(len(operationSet)+1)
          colormap = plt.cm.gist_ncar
          colors = [colormap(i) for i in np.linspace(0, 0.9, len(operationSet))]
          plt.gca().set_color_cycle(colors)
          #colorBase = 1 / float(len(operationSet)+1)
          totalTime = 0;
          wasSet = False;
          for n, operation in enumerate(operationSet):
            #colorValue = "{:f}".format(colorBase*(n+0.5))
            #plt.bar(index + n * bar_width + 0.5*bar_width, np.array(dataRows[query][scale][treeType][cover][operation]), bar_width, color=colorValue, label=operation, log=False, bottom=0)
            if not wasSet and sum(dataRows[query][scale][treeType][cover][operation]['start time']) > 0:
              startTimeBar = plt.bar(index + n * bar_width + 0.5*bar_width, np.array(dataRows[query][scale][treeType][cover][operation]['start time']), bar_width, color='gray', label='start receiving time', log=False, bottom=0)
              wasSet = True;
            else:
              startTimeBar = plt.bar(index + n * bar_width + 0.5*bar_width, np.array(dataRows[query][scale][treeType][cover][operation]['start time']), bar_width, color='gray', log=False, bottom=0)
            exTimeBar = plt.bar(index + n * bar_width + 0.5*bar_width, np.array(dataRows[query][scale][treeType][cover][operation]['execution time']), bar_width, color=colors[n], label=operation, log=False, bottom=np.array(dataRows[query][scale][treeType][cover][operation]['start time']))
            totalTime = dataRows[query][scale][treeType][cover][operation]['total time']
          plt.axhline(y=totalTime, xmin=0, xmax=1, linewidth=2, color='red', label="last result sent to client")
          plt.xlabel("Slaves")
          plt.ylabel(measurementType + ' (in sec)')
          plt.xticks(index + 0.5, np.array(slaveSet))
          plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')
          plt.legend(bbox_to_anchor=(1.03,0,1/(scale/15.)/(len(operationSet)/4),1), loc='upper left', ncol=1, mode="expand", borderaxespad=0.)
          plt.title('Query operation execution time for query ' + query + '\n' + treeType + ' tree, ' + cover + ' cover and ' + str(scale) + ' chunks', y=1.05)
          plt.savefig(outputDir+'/queryOperationTime'+'_cover='+cover+'_scale='+str(scale)+'_query='+query+'_treeType='+treeType+'.'+imageType, bbox_inches='tight')
          plt.close(fig2)
          plt.close(fig)