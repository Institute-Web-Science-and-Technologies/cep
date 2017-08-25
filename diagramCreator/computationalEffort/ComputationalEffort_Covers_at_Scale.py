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

matplotlib.rcParams.update({'font.size': 16})

scales = {}

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
    if not scale in scales:
      scales[scale] = {}
    if not treeType in scales[scale]:
      scales[scale][treeType] = {}
    if not cover in scales[scale][treeType]:
      scales[scale][treeType][cover] = {}
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " #tp=" + str(int(row[6])+1) + " #ds=" + row[7] + " sel=" + row[8]
    scales[scale][treeType][cover][query] = { "Total":long(row[9]), "Entropy":float(row[10]), "Gini Coefficient":float(row[12])}

for measurementType in ["Total", "Entropy", "Gini Coefficient"]:
  for scale in scales.keys():
    for treeType in scales[scale].keys():
      coverSet = list(sorted(scales[scale][treeType].keys()))
      dataRows = {}
      queryGroups = []
      for i, cover in enumerate(coverSet):
        if i == 0:
          queryGroups = list(sorted(scales[scale][treeType][cover].keys()))
        dataRows[cover] = []
        for query in queryGroups:
          dataRows[cover].append(scales[scale][treeType][cover][query][measurementType]);
      # create diagramm sorted by cover
      n_groups = len(queryGroups)
      fig, ax = plt.subplots()
      #fig = plt.figure(figsize=(fig.get_figwidth()*2.5,fig.get_figheight()))
      index = np.arange(n_groups)
      bar_width =  1/float(len(coverSet)+1)
      rects = []
      colormap = plt.cm.gist_ncar
      colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet))]
      for i, cover in enumerate(coverSet):
        colorValue = colors[i]
        if measurementType == "Total":
          rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[cover]), bar_width, color=colorValue, label=cover, log=True, bottom=1))
        else:
          rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[cover]), bar_width, color=colorValue, label=cover))
      plt.xlabel("Queries")
      if measurementType == "Total":
        plt.ylabel(measurementType + " (log-scale)")
      else:
        plt.ylabel('Workload Imbalance')
      #plt.title('Computational effort for query execution tree type ' + treeType + ' and ' + scale + ' chunks', y=1.15, x=0.4)
      plt.xticks(index + 0.5, np.array(queryGroups))
      plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
      #plt.axis('tight')
      plt.legend(bbox_to_anchor=(-0.3, 1.04, 1.3, .102), loc=3, ncol=3, mode="expand", borderaxespad=0.,fontsize=16)
      plt.savefig(outputDir+'/computationalEffort_'+measurementType+'_numberOfChunks-'+scale+'_treeType-'+treeType+'.'+imageType, bbox_inches='tight')
      plt.close('all')
