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
  print("You must have the following arguments: <plainResultsOverTime.csv> <outputDir> <imageType>")
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
matplotlib.rcParams.update({'font.size': 28})

def plotSortedByCover(ax, scale, coverSet, dataRows, queryGroups, measurementType):
  for i, cover in enumerate(coverSet):
    dataRows[cover] = []
    for query in sorted(list(queryGroups)):
      dataRows[cover].append(scales[scale][treeType][cover][query][measurementType]);
  n_groups = len(queryGroups)
  index = np.arange(n_groups)
  bar_width =  1/float(len(coverSet)+1)
  colormap = plt.cm.gist_ncar
  colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)+1)]
  plt.gca().set_color_cycle(colors)
  bars = []
  for i, cover in enumerate(coverSet):
    color=colors[i+1]
    bars.append(ax.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[cover]), bar_width, color=color, label=cover, log=False, bottom=1))
  ax.set_xticks(index + 0.5)
  ax.set_xticklabels(sorted(list(queryGroups)), rotation=45, horizontalalignment='right')
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
    row2 = reader.next();
    for i, value in enumerate(row2):
      if i>=9 and float(row2[i])>=0.5 and (i==9 or float(row2[i-1])<0.5):
        scales[scale][treeType][cover][query] = { "Execution Time":(long(row[i])/1000)}
        break;

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
          if scales[scale][treeType][cover][query][measurementType] > 4000:
            longTimeQueries.add(query)
            midTimeQueries.discard(query)
          elif (query not in longTimeQueries) and scales[scale][treeType][cover][query][measurementType] > 500:
            midTimeQueries.add(query)
      queryGroups = queryGroups.difference(longTimeQueries).difference(midTimeQueries)

      # create diagramm sorted by cover
      nColl=len(queryGroups)+len(midTimeQueries)+len(longTimeQueries)
      fig = plt.figure()
      fig2 = plt.figure(figsize=(fig.get_figwidth()*(len(longTimeQueries)+len(midTimeQueries)+len(queryGroups))/5,fig.get_figheight()*2))
      bars = []
      if len(queryGroups) > 0:
        ax1 = plt.subplot2grid((1,nColl+2), (0, 0), colspan=len(queryGroups))
        bars = plotSortedByCover(ax1, scale, coverSet, dataRows, queryGroups, measurementType)
      plt.ylabel(measurementType + " (in sec)")
      if len(midTimeQueries) > 0:
        ax2 = plt.subplot2grid((1,nColl+2), (0, len(queryGroups)+1), colspan=len(midTimeQueries))
        bars = plotSortedByCover(ax2, scale, coverSet, dataRows, midTimeQueries, measurementType)
      plt.xlabel("Queries")
      if len(longTimeQueries) > 0:
        ax3 = plt.subplot2grid((1,nColl+2), (0, len(queryGroups)+len(midTimeQueries)+2), colspan=len(longTimeQueries))
        bars = plotSortedByCover(ax3, scale, coverSet, dataRows, longTimeQueries, measurementType)
      plt.suptitle('Query execution half time for tree type ' + treeType + ' and ' + scale + ' chunks',y=1.05)
      plt.figlegend(bars, map(getLabel,bars), loc=3, ncol=3, bbox_to_anchor=(.1, 1.22, 0.8, 1), mode="expand", fontsize=24, borderaxespad=0.)
      #plt.subplots_adjust(left=0.1, right=1.3, wspace=4)
      plt.savefig(outputDir+'/queryExecutionHalfTime_'+measurementType+'_numberOfChunks-'+scale+'_treeType-'+treeType+'.'+imageType, bbox_inches='tight')
      plt.close('all')