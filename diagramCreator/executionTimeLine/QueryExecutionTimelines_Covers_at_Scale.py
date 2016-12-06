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
# for each tree type create a diagram that
# shows for each query
# the computational effort per cover in a separate bar

# required map: treetype -> cover -> query -> measurmentType -> value

def plotSortedByCover(ax, scale, coverSet, dataRows, queryGroups, measurementType):
  for i, cover in enumerate(coverSet):
    dataRows[cover] = [[],[],[]]
    for query in queryGroups:
      dataRows[cover][0].append(scales[scale][treeType][cover][query][measurementType][0]);
      dataRows[cover][1].append(scales[scale][treeType][cover][query][measurementType][1]);
      dataRows[cover][2].append(scales[scale][treeType][cover][query][measurementType][2]);
  n_groups = len(queryGroups)
  index = np.arange(n_groups)
  bar_width =  1/float(len(coverSet)+1)
  colormap = plt.cm.gist_ncar
  colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet))]
  plt.gca().set_color_cycle(colors)
  bars = []
  for i, cover in enumerate(coverSet):
    color=colors[i]
    bars.append(ax.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[cover][0]), bar_width, color=color, edgecolor="{:f}".format(0.6), linewidth=2, hatch='//', label=cover + ' parsing', log=False, bottom=1))
    bars.append(ax.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[cover][1]), bar_width, color=color, edgecolor="{:f}".format(0.4), linewidth=2, hatch='.', label=cover + ' submitting', log=False, bottom=1+np.array(dataRows[cover][0])))
    bars.append(ax.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[cover][2]), bar_width, color=color, label=cover + ' executing', log=False, bottom=1+np.array(dataRows[cover][0])+np.array(dataRows[cover][1])))
  ax.set_xticks(index + 0.5)
  ax.set_xticklabels(sorted(list(queryGroups)), rotation=45, horizontalalignment='right')
  #plt.axis('tight')
  return bars

def getLabel(bar):
  return bar.get_label()

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
    scales[scale][treeType][cover][query] = { "Execution Time":[(long(row[9])/1000),(long(row[10])/1000),(long(row[11])/1000)]}

for measurementType in ["Execution Time"]:
  for scale in scales.keys():
    for treeType in scales[scale].keys():
      coverSet = list(sorted(scales[scale][treeType].keys()))
      dataRows = {}
      longTimeQueries = set();
      midTimeQueries = set();
      queryGroups = set(scales[scale][treeType][cover].keys())
      for i, cover in enumerate(coverSet):
        for query in queryGroups:
          if sum(scales[scale][treeType][cover][query][measurementType]) > 4000:
            longTimeQueries.add(query)
            midTimeQueries.discard(query)
          elif (query not in longTimeQueries) and sum(scales[scale][treeType][cover][query][measurementType]) > 500:
            midTimeQueries.add(query)
      queryGroups = queryGroups.difference(longTimeQueries).difference(midTimeQueries)

      # create diagramm sorted by cover
      nColl=len(queryGroups)+len(midTimeQueries)+len(longTimeQueries)
      fig = plt.figure()
      fig2 = plt.figure(figsize=(fig.get_figwidth()*(len(longTimeQueries)+len(midTimeQueries)+len(queryGroups))/5,fig.get_figheight()*2))
      bars = []
      if len(queryGroups) > 0:
        ax1 = plt.subplot2grid((1,nColl), (0, 0), colspan=len(queryGroups))
        bars = plotSortedByCover(ax1, scale, coverSet, dataRows, queryGroups, measurementType)
      plt.ylabel(measurementType + " (in sec)")
      if len(midTimeQueries) > 0:
        ax2 = plt.subplot2grid((1,nColl), (0, len(queryGroups)), colspan=len(midTimeQueries))
        bars = plotSortedByCover(ax2, scale, coverSet, dataRows, midTimeQueries, measurementType)
      plt.xlabel("Queries")
      if len(longTimeQueries) > 0:
        ax3 = plt.subplot2grid((1,nColl), (0, len(queryGroups)+len(midTimeQueries)), colspan=len(longTimeQueries))
        bars = plotSortedByCover(ax3, scale, coverSet, dataRows, longTimeQueries, measurementType)
      plt.suptitle('Query execution time for tree type ' + treeType + ' and ' + scale + ' chunks',y=1.05)
      plt.figlegend(bars, map(getLabel,bars), loc=3, ncol=3, bbox_to_anchor=(.05, 1, .8, 1), mode="expand", borderaxespad=0.)
      plt.subplots_adjust(wspace=1)
      plt.savefig(outputDir+'/queryExecutionTimeline_'+measurementType+'_numberOfChunks-'+scale+'_treeType-'+treeType+'.'+imageType, bbox_inches='tight')
      plt.close('all')
