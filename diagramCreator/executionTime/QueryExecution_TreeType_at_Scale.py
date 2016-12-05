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
  print("You must have the following arguments: <totalExecutionTime.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

# for totalComputationalEffort, entropy, standard deviation
# for each cover create a diagram that
# shows for each query
# the computational effort per tree type in a separate bar

# required map: treetype -> cover -> query -> measurmentType -> value

coverTypes = {}

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
    if not cover in coverTypes:
      coverTypes[cover] = {}
    if not scale in coverTypes[cover]:
      coverTypes[cover][scale] = {}
    if not treeType in coverTypes[cover][scale]:
      coverTypes[cover][scale][treeType] = {}
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " #tp=" + str(int(row[6])+1) + " #ds=" + row[7] + " sel=" + row[8]
    coverTypes[cover][scale][treeType][query] = { "Execution Time":(long(row[9])/1000)}

for measurementType in ["Execution Time"]:
  for cover in coverTypes.keys():
    for scale in coverTypes[cover].keys():
      treeTypeSet = list(sorted(coverTypes[cover][scale].keys()))
      dataRows = {}
      queryGroups = []
      for i, treeType in enumerate(treeTypeSet):
        if i == 0:
          queryGroups = list(sorted(coverTypes[cover][scale][treeType].keys()))
        dataRows[treeType] = []
        for query in queryGroups:
          dataRows[treeType].append(coverTypes[cover][scale][treeType][query][measurementType]);

      # create diagramm sorted by tree type
      n_groups = len(queryGroups)
      fig, ax = plt.subplots()
      index = np.arange(n_groups)
      bar_width =  1/float(len(treeTypeSet)+1)
      rects = []
      colormap = plt.cm.gist_ncar
      colors = [colormap(i) for i in np.linspace(0, 0.9, len(treeTypeSet))]
      for i, treeType in enumerate(treeTypeSet):
        colorValue = colors[i]
        rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[treeType]), bar_width, color=colorValue, label=treeType, log=True, bottom=1))
      plt.xlabel("Queries")
      plt.ylabel(measurementType + " (in sec, log-scale)")
      plt.title('Query execution time for ' + cover + ' cover and ' + scale + ' chunks', y=1.12)
      plt.xticks(index + 0.5, np.array(queryGroups))
      plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
      #plt.axis('tight')
      plt.legend(bbox_to_anchor=(0., 1.04, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
      plt.savefig(outputDir+'/queryExecution_'+measurementType+'_cover-'+cover+'_numberOfChunks-'+scale+'.'+imageType, bbox_inches='tight')
      plt.close('all')

