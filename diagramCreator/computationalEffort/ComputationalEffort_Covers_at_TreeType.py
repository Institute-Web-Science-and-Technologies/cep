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
import latexPlot as latex

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

#matplotlib.rcParams.update({'font.size': 20})

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + ("HOP\\_" if imageType=="latex" else "HOP_")
    if imageType=="latex":
      cover += row[0].replace('_','\\_')
    else:
      cover += row[0]
    scale = row[1]
    treeType = row[3]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not cover in treeTypes[treeType]:
      treeTypes[treeType][cover] = {}
    if not scale in treeTypes[treeType][cover]:
      treeTypes[treeType][cover][scale] = {}
    if imageType=="latex":
      query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[7])+1) + " \\#ds=" + row[8] + " sel=" + row[9]
    else:
      query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " #tp=" + str(int(row[7])+1) + " #ds=" + row[8] + " sel=" + row[9]
    treeTypes[treeType][cover][scale][query] = { "Total":long(row[10]), "Entropy":float(row[11]), "Workload Imbalance":float(row[13])}

for measurementType in ["Total", "Workload Imbalance"]:
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

    if imageType=="latex":
      latex.latexify(scale=1)

    # create diagramm sorted by cover
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    if imageType!="latex":
      fig = plt.figure(figsize=(fig.get_figwidth()*2.5,fig.get_figheight()))
    index = np.arange(n_groups)
    bar_width =  1/float(len(coverSet)*len(scaleSet)+2+len(coverSet)*1)
    rects = []
    colormap = plt.cm.gist_ncar
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(list(sorted(treeTypes[treeType].keys())))+1)]
    for i, cover in enumerate(coverSet):
      for j, scale in enumerate(scaleSet):
        colorValue = colors[list(sorted(treeTypes[treeType].keys())).index(cover)+1]
        if measurementType == "Total":
          rects.append(plt.bar(index + (i*len(coverSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover, log=True, bottom=1))
        else:
          rects.append(plt.bar(index + (i*len(coverSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, linewidth=0.5, label=cover))
    plt.xlabel("Queries")
    if measurementType == "Total":
      plt.ylabel(measurementType + " (log-scale)")
    else:
      plt.ylabel(measurementType)
    #plt.title('Computational effort for query execution tree type ' + treeType + ' sorted by cover', y=1.28)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    if imageType=="latex":
      plt.legend(bbox_to_anchor=(-0.145, 1.02, 1.145, .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
      fig.tight_layout(rect=(-0.03,-0.035,1.02,0.865))
      latex.savefig(outputDir,'computationalEffort_'+measurementType+'_treeType-'+treeType+'_sortedByCover')
    else:
      plt.legend(bbox_to_anchor=(0., 1.04, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0., fontsize=16)
      plt.savefig(outputDir+'/computationalEffort_'+measurementType+'_treeType-'+treeType+'_sortedByCover.'+imageType, bbox_inches='tight')
    plt.close('all')

#for measurementType in ["Total", "Entropy", "Workload Imbalance"]:
#  for treeType in treeTypes.keys():
#    coverSet = list(sorted(treeTypes[treeType].keys()))
#    scaleSet = list(sorted(treeTypes[treeType][coverSet[0]].keys()))
#    dataRows = {}
#    queryGroups = []
#    for i, cover in enumerate(coverSet):
#      dataRows[cover] = {}
#      for j, scale in enumerate(scaleSet):
#        if i == 0:
#          queryGroups = list(sorted(treeTypes[treeType][cover][scale].keys()))
#        dataRows[cover][scale] = []
#        for query in queryGroups:
#          dataRows[cover][scale].append(treeTypes[treeType][cover][scale][query][measurementType]);

#    if imageType=="latex":
#      latex.latexify(scale=1)

#    # create diagramm sorted by number of chunks
#    n_groups = len(queryGroups)
#    fig, ax = plt.subplots()
#    if imageType!="latex":
#      fig = plt.figure(figsize=(fig.get_figwidth()*2.5,fig.get_figheight()))
#    index = np.arange(n_groups)
#    bar_width =  1/float(len(coverSet)*len(scaleSet)+2+len(coverSet)*1)
#    rects = []
#    colormap = plt.cm.gist_ncar
#    colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)*len(scaleSet))]
#    for i, scale in enumerate(scaleSet):
#      for j, cover in enumerate(coverSet):
#        colorValue = colors[(i*len(scaleSet)+j)]
#        if measurementType == "Total":
#          rects.append(plt.bar(index + (i*len(scaleSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover + ' ' + scale + ' chunks', log=True, bottom=1))
#        else:
#          rects.append(plt.bar(index + (i*len(scaleSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover + ' ' + scale + ' chunks'))
#    plt.xlabel("Queries")
#    if measurementType == "Total":
#      plt.ylabel(measurementType + " (log-scale)")
#    else:
#      plt.ylabel(measurementType)
#    #plt.title('Computational effort for query execution tree type ' + treeType + ' sorted by number of chunks', y=1.28)
#    plt.xticks(index + 0.5, np.array(queryGroups))
#    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
#    plt.axis('tight')
#    if imageType=="latex":
#      plt.legend(bbox_to_anchor=(-0.09, 1.06, 1.09, .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
#      fig.tight_layout(rect=(-0.035,-0.035,1.02,0.865))
#      latex.savefig(outputDir,'computationalEffort_'+measurementType+'_treeType-'+treeType+'_sortedByNumberOfChunks')
#    else:
#      plt.legend(bbox_to_anchor=(0., 1.04, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0., fontsize=16)
#      plt.savefig(outputDir+'/computationalEffort_'+measurementType+'_treeType-'+treeType+'_sortedByNumberOfChunks.'+imageType, bbox_inches='tight')
#    plt.close('all')
