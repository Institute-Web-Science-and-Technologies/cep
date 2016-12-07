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
  print("You must have the following arguments: <computationalEffortPerChunk.csv> <outputDir> <imageType>")
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
    if not cover in queries[query][scale]:
      queries[query][scale][cover] = {}
    if not treeType in queries[query][scale][cover]:
      queries[query][scale][cover][treeType] = {}
    for i in range(len(row)):
      if i >= 9 and i % 2 == 0 :
        chunk = row[i-1].split(':')[0]
        queries[query][scale][cover][treeType][chunk] = long(row[i])

for measurementType in ["Computational Effort"]:
  querySet = list(sorted(queries.keys()))
  scaleSet = list(sorted(queries[querySet[0]].keys()))
  coverSet = list(sorted(queries[querySet[0]][scaleSet[0]].keys()))
  treeTypeSet = list(sorted(queries[querySet[0]][scaleSet[0]][coverSet[0]].keys()))
  dataRows = {}
  for i, query in enumerate(querySet):
    dataRows[query] = {}
    for j, scale in enumerate(scaleSet):
      dataRows[query][scale] = {}
      for k, cover in enumerate(coverSet):
        dataRows[query][scale][cover] = {}
        for l, treeType in enumerate(treeTypeSet):
          dataRows[query][scale][cover][treeType] = []
          for m, chunk in enumerate(sorted(queries[query][scale][cover][treeType])):
            dataRows[query][scale][cover][treeType].append(queries[query][scale][cover][treeType][chunk]);

  # create diagramms per treeType
  for i, query in enumerate(querySet):
    for j, scale in enumerate(scaleSet):
      for k, cover in enumerate(coverSet):
        for l, treeType in enumerate(treeTypeSet):
          n_groups = scale
          fig, ax = plt.subplots()
          fig = plt.figure(figsize=(fig.get_figwidth()*(scale/20.),5))
          index = np.arange(n_groups)
          bar_width = 1/float(len(treeTypeSet)+1)
          rects = []
          rects.append(plt.bar(index + l * bar_width + 0.5*bar_width, np.array(dataRows[query][scale][cover][treeType]), bar_width, color='grey', label=treeType, log=False, bottom=0))
          plt.xlabel("Chunks")
          plt.ylabel(measurementType)
          plt.xticks(index + 0.5, np.array(list(sorted(queries[query][scale][cover][treeTypeSet[0]]))))
          plt.setp(plt.gca().get_xticklabels(), rotation=90, horizontalalignment='right')
          #plt.axis('tight')
          plt.title('Computational Effort for query ' + query + '\n' + cover + ' cover and ' + str(scale) + ' chunks', y=1.15)
          plt.savefig(outputDir+'/computationalEffortUnsorted'+'_cover='+cover+'_scale='+str(scale)+'_query='+query+'_treeType='+treeType+'.'+imageType, bbox_inches='tight')
          plt.close('all')
