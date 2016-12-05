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
# shows for each query
# the computational effort per cover in a separate bar

# required map: cover -> query -> measurmentType -> value

covers = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[2]) != 0:
      cover += row[2] + "HOP_"
    cover += row[0]
    if not cover in covers:
      covers[cover] = {}
    scale = row[1]
    if not scale in covers[cover]:
      covers[cover][scale] = {}
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " tree=" + ("ll" if row[3]=='LEFT_LINEAR' else ("rl" if row[3]=='RIGHT_LINEAR' else "b")) + " #tp=" + str(int(row[6])+1) + " #ds=" + row[7] + " sel=" + row[8]
    covers[cover][scale][query] = { "Data Transfer":long(row[9])}

for measurementType in ["Data Transfer"]:
  for baseCover in covers.keys():
    coverSet = list(sorted(covers.keys()))
    scaleSet = list(sorted(covers[coverSet[0]].keys()))
    coverSet.remove(baseCover)
    dataRows = {}
    queryGroups = []
    for i, cover in enumerate(coverSet):
      dataRows[cover] = {}
      for j, scale in enumerate(scaleSet):
        if i == 0:
          queryGroups = list(sorted(covers[cover][scale].keys()))
        dataRows[cover][scale] = []
        for query in queryGroups:
          baseDataTransfer = covers[baseCover][scale][query][measurementType]
          currentDataTransfer = covers[cover][scale][query][measurementType]
          if baseDataTransfer > 0:
            dataRows[cover][scale].append((currentDataTransfer-baseDataTransfer)/float(baseDataTransfer));
          elif currentDataTransfer == 0:
            dataRows[cover][scale].append(0);
          else:
            dataRows[cover][scale].append(currentDataTransfer);
  
    # create diagramm grouped by cover
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(fig.get_figwidth()*3.5,fig.get_figheight()))
    index = np.arange(n_groups)
    bar_width = 1/float(len(coverSet)*len(scaleSet)+2+len(coverSet)*1)
    rects = []
    colormap = plt.cm.gist_ncar
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)*len(scaleSet))]
    #plt.axhline(y=1., xmin=0, xmax=1, linewidth=2, color='red', label="data transfer HASH")
    c=0
    for i, cover in enumerate(coverSet):
      for j, scale in enumerate(scaleSet):
        colorValue = colors[c]
        rects.append(plt.bar(index + c * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover + ' ' + scale + ' chunks'))
        c+=1
    plt.xlabel("Queries")
    plt.ylabel(measurementType+' relative change to '+baseCover+' cover')
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
    plt.savefig(outputDir+'/DataTransfer'+'_relativeTo_'+baseCover+'_sortedByCover.'+imageType, bbox_inches='tight')
    plt.close('all')
  
    # create diagramm grouped by chunks
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(fig.get_figwidth()*3.5,fig.get_figheight()))
    index = np.arange(n_groups)
    bar_width = 1/float(len(coverSet)*len(scaleSet)+2+len(scaleSet)*1)
    rects = []
    colormap = plt.cm.gist_ncar
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)*len(scaleSet))]
    #plt.axhline(y=1., xmin=0, xmax=1, linewidth=2, color='red', label="data transfer HASH")
    c=0
    for i, scale in enumerate(scaleSet):
      for j, cover in enumerate(coverSet):
        colorValue = colors[c]
        rects.append(plt.bar(index + c * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover + ' ' + scale + ' chunks'))
        c+=1
    plt.xlabel("Queries")
    plt.ylabel(measurementType+' relative change to '+baseCover+' cover')
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
    plt.savefig(outputDir+'/DataTransfer'+'_relativeTo_'+baseCover+'_sortedByNumberOfChunks.'+imageType, bbox_inches='tight')
    plt.close('all')

