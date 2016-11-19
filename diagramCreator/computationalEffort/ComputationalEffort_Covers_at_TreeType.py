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
    if int(row[2]) != 0:
      cover += row[2] + "HOP_"
    cover += row[0]
    scale = row[1]
    treeType = row[3]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not cover in treeTypes[treeType]:
      treeTypes[treeType][cover] = {}
    if not scale in treeTypes[treeType][cover]:
      treeTypes[treeType][cover][scale] = {}
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " #tp=" + str(int(row[6])+1) + " #ds=" + row[7] + " sel=" + row[8]
    treeTypes[treeType][cover][scale][query] = { "Total":long(row[9]), "Entropy":float(row[10])}

for measurementType in ["Total"]:
  for treeType in treeTypes.keys():
    coverSet = list(sorted(treeTypes[treeType].keys()))
    scaleSet = list(sorted(treeTypes[treeType][coverSet[0]].keys()))
    dataRows = {}
    queryGroups = []
    for i, cover in enumerate(coverSet):
      dataRows[cover] = {}
      for j, scale in enumerate(scaleSet):
        if i == 0:
          queryGroups = list(sorted(treeTypes[treeType][cover][scale].keys()))
        dataRows[cover][scale] = []
        for query in queryGroups:
          dataRows[cover][scale].append(treeTypes[treeType][cover][scale][query][measurementType]);
    # create diagramm sorted by cover
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(fig.get_figwidth()*2.5,fig.get_figheight()))
    index = np.arange(n_groups)
    bar_width =  1/float(len(coverSet)*len(scaleSet)+2+len(coverSet)*1)
    rects = []
    colorBase =  1 / float(len(coverSet)*len(scaleSet)+1)
    for i, cover in enumerate(coverSet):
      for j, scale in enumerate(scaleSet):
        colorValue = "{:f}".format(colorBase*(j*len(coverSet)+i))
        if measurementType == "Entropy":
          rects.append(plt.bar(index + (i*len(coverSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover + ' ' + scale + ' chunks'))
        else:
          rects.append(plt.bar(index + (i*len(coverSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover + ' ' + scale + ' chunks', log=True, bottom=1))
    plt.xlabel("Queries")
    if measurementType == "Entropy":
      plt.ylabel(measurementType)
    else:
      plt.ylabel(measurementType + " (log-scale)")
    plt.title('Computational effort for query execution tree type ' + treeType + ' sorted by cover', y=1.28)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    plt.legend(bbox_to_anchor=(0., 1.04, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
    plt.savefig(outputDir+'/computationalEffort_'+measurementType+'_treeType-'+treeType+'_sortedByCover.'+imageType, bbox_inches='tight')

for measurementType in ["Total", "Entropy"]:
  for treeType in treeTypes.keys():
    coverSet = list(sorted(treeTypes[treeType].keys()))
    scaleSet = list(sorted(treeTypes[treeType][coverSet[0]].keys()))
    dataRows = {}
    queryGroups = []
    for i, cover in enumerate(coverSet):
      dataRows[cover] = {}
      for j, scale in enumerate(scaleSet):
        if i == 0:
          queryGroups = list(sorted(treeTypes[treeType][cover][scale].keys()))
        dataRows[cover][scale] = []
        for query in queryGroups:
          dataRows[cover][scale].append(treeTypes[treeType][cover][scale][query][measurementType]);
    # create diagramm sorted by number of chunks
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(fig.get_figwidth()*2.5,fig.get_figheight()))
    index = np.arange(n_groups)
    bar_width =  1/float(len(coverSet)*len(scaleSet)+2+len(coverSet)*1)
    rects = []
    colorBase =  1 / float(len(coverSet)*len(scaleSet)+1)
    for i, scale in enumerate(scaleSet):
      for j, cover in enumerate(coverSet):
        colorValue = "{:f}".format(colorBase*(j*len(scaleSet)+i))
        if measurementType == "Entropy":
          rects.append(plt.bar(index + (i*len(scaleSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover + ' ' + scale + ' chunks'))
        else:
          rects.append(plt.bar(index + (i*len(scaleSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover + ' ' + scale + ' chunks', log=True, bottom=1))
    plt.xlabel("Queries")
    if measurementType == "Entropy":
      plt.ylabel(measurementType)
    else:
      plt.ylabel(measurementType + " (log-scale)")
    plt.title('Computational effort for query execution tree type ' + treeType + ' sorted by number of chunks', y=1.28)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    plt.legend(bbox_to_anchor=(0., 1.04, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
    plt.savefig(outputDir+'/computationalEffort_'+measurementType+'_treeType-'+treeType+'_sortedByNumberOfChunks.'+imageType, bbox_inches='tight')
