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
  print("You must have the following arguments: <computationalEffort.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

# for totalComputationalEffort, entropy, standard deviation
# for each tree type create a diagram that
# shows for each query
# the computational effort per cover in a separate bar

# required map: treetype -> cover -> query -> measurmentType -> value

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    treeType = row[2]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not cover in treeTypes[treeType]:
      treeTypes[treeType][cover] = {}
    query = ("ss" if row[4]=='SUBJECT_SUBJECT_JOIN' else "so") + " #j=" + row[5] + " #ds=" + row[6] + " sel=" + row[7]
    treeTypes[treeType][cover][query] = { "Data Transfer":long(row[8])}

for measurementType in ["Data Transfer"]:
  for treeType in treeTypes.keys():
    coverSet = list(sorted(treeTypes[treeType].keys()))
    dataRows = []
    queryGroups = []
    for i, cover in enumerate(coverSet):
      if i == 0:
        queryGroups = list(sorted(treeTypes[treeType][cover].keys()))
      dataRows.append([])
      for query in queryGroups:
        dataRows[i].append(treeTypes[treeType][cover][query][measurementType]);
    # create diagramm
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 1/float(len(coverSet)+1)
    rects = []
    colorBase = 1 / float(len(coverSet)+1)
    for i, cover in enumerate(coverSet):
      colorValue = "{:f}".format(colorBase*(i+0.5))
      rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[i]), bar_width, color=colorValue, label=cover))
    plt.xlabel("Queries")
    plt.ylabel(measurementType)
    plt.title('Data transfer for query execution tree type ' + treeType, y=1.20)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    plt.legend(bbox_to_anchor=(0., 1.04, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig(outputDir+'/dataTransfer_'+measurementType+'_treeType-'+treeType+'_forAll_covers.'+imageType, bbox_inches='tight')

