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
  print("You must have the following arguments: <packageTransport.csv> <outputDir> <imageType>")
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
    if row[5]=='SUBJECT_SUBJECT_JOIN':
      continue;
    cover = ""
    if int(row[2]) != 0:
      cover += row[2] + "HOP_"
    cover += row[0]
    scale = row[1]
    treeType = row[3]
    if not cover in coverTypes:
      coverTypes[cover] = {}
    if not treeType in coverTypes[cover]:
      coverTypes[cover][treeType] = {}
    if not scale in coverTypes[cover][treeType]:
      coverTypes[cover][treeType][scale] = {}
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " #tp=" + str(int(row[6])+1) + " #ds=" + row[7] + " sel=" + row[8]
    coverTypes[cover][treeType][scale][query] = { "Package Transport":long(row[9])}

for measurementType in ["PackageTransport"]:
  for cover in coverTypes.keys():
    treeTypeSet = list(sorted(coverTypes[cover].keys()))
    scaleSet = list(sorted(coverTypes[cover][treeTypeSet[0]].keys()))
    dataRows = {}
    queryGroups = []
    for i, treeType in enumerate(treeTypeSet):
      dataRows[treeType] = {}
      for j, scale in enumerate(scaleSet):
        if i == 0:
          queryGroups = list(sorted(coverTypes[cover][treeType][scale].keys()))
        dataRows[treeType][scale] = []
        for query in queryGroups:
          dataRows[treeType][scale].append(coverTypes[cover][treeType][scale][query][measurementType]);

    # create diagramm sorted by tree type
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width =  1/float(len(treeTypeSet)*len(scaleSet)+2+len(treeTypeSet)*1)
    rects = []
    colormap = plt.cm.gist_ncar
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(treeTypeSet)*len(scaleSet))]
    for i, treeType in enumerate(treeTypeSet):
      for j, scale in enumerate(scaleSet):
        colorValue = colors[(i*len(treeTypeSet)+j)]
        rects.append(plt.bar(index + (i*len(treeTypeSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[treeType][scale]), bar_width, color=colorValue, label=treeType + ' ' + scale + ' chunks', log=True, bottom=1))
    plt.xlabel("Queries")
    plt.ylabel(measurementType)
    plt.title('Package Transport ' + cover, y=1.12)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    #plt.axis('tight')
    plt.title(measurementType + ' for ' + cover + ' cover sorted by tree type',y=1.37)
    plt.legend(bbox_to_anchor=(-0.2, 1.04, 1.2, .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig(outputDir+'/packageTransport_'+measurementType+'_cover-'+cover+'_forAll_treeTypes_sortedByTreeType.'+imageType, bbox_inches='tight')
    plt.close('all')

    # create diagramm sorted by number of chunks
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width =  1/float(len(treeTypeSet)*len(scaleSet)+2+len(treeTypeSet)*1)
    rects = []
    colormap = plt.cm.gist_ncar
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(treeTypeSet)*len(scaleSet))]
    for i, scale in enumerate(scaleSet):
      for j, treeType in enumerate(treeTypeSet):
        colorValue = colors[(i*len(scaleSet)+j)]
        rects.append(plt.bar(index + (i*len(scaleSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[treeType][scale]), bar_width, color=colorValue, label=treeType + ' ' + scale + ' chunks', log=True, bottom=1))
    plt.xlabel("Queries")
    plt.ylabel(measurementType)
    plt.title('Package Transport ' + cover, y=1.12)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    #plt.axis('tight')
    plt.title(measurementType + ' for ' + cover + ' cover sorted by number of chunks',y=1.37)
    plt.legend(bbox_to_anchor=(-0.2, 1.04, 1.2, .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig(outputDir+'/packageTransport_'+measurementType+'_cover-'+cover+'_forAll_treeTypes_sortedByNumberOfChunks.'+imageType, bbox_inches='tight')
    plt.close('all')
