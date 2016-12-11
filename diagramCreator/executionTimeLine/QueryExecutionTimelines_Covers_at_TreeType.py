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

def plotSortedByCover(ax, scaleSet, coverSet, dataRows, queryGroups, measurementType):
  for i, cover in enumerate(coverSet):
    dataRows[cover] = {}
    for j, scale in enumerate(scaleSet):
      dataRows[cover][scale] = [[],[],[]]
      for query in sorted(list(queryGroups)):
        dataRows[cover][scale][0].append(treeTypes[treeType][cover][scale][query][measurementType][0]);
        dataRows[cover][scale][1].append(treeTypes[treeType][cover][scale][query][measurementType][1]);
        dataRows[cover][scale][2].append(treeTypes[treeType][cover][scale][query][measurementType][2]);
  n_groups = len(queryGroups)
  index = np.arange(n_groups)
  bar_width = 1/float(len(coverSet)*len(scaleSet)+2+len(coverSet)*1)
  #colorBase = 1 / float(len(coverSet)*len(scaleSet)+1)
  colormap = plt.cm.gist_ncar
  colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)*len(scaleSet))]
  plt.gca().set_color_cycle(colors)
  bars = []
  for i, cover in enumerate(coverSet):
    for j, scale in enumerate(scaleSet):
      #colorValue = "{:f}".format(colorBase*(j*len(coverSet)+i))
      color=colors[i*len(coverSet)+j]
      bars.append(ax.bar(index + (i*len(coverSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale][0]), bar_width, color=color, edgecolor="{:f}".format(0.6), linewidth=2, hatch='//', label=cover + ' ' + scale + ' chunks parsing', log=False, bottom=1))
      bars.append(ax.bar(index + (i*len(coverSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale][1]), bar_width, color=color, edgecolor="{:f}".format(0.4), linewidth=2, hatch='.', label=cover + ' ' + scale + ' chunks submitting', log=False, bottom=1+np.array(dataRows[cover][scale][0])))
      bars.append(ax.bar(index + (i*len(coverSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale][2]), bar_width, color=color, label=cover + ' ' + scale + ' chunks executing', log=False, bottom=1+np.array(dataRows[cover][scale][0])+np.array(dataRows[cover][scale][1])))
  ax.set_xticks(index + 0.5)
  ax.set_xticklabels(sorted(list(queryGroups)), rotation=45, horizontalalignment='right')
  #plt.axis('tight')
  return bars

def plotSortedByScale(ax, scaleSet, coverSet, dataRows, queryGroups, measurementType):
  for i, cover in enumerate(coverSet):
    dataRows[cover] = {}
    for j, scale in enumerate(scaleSet):
      dataRows[cover][scale] = [[],[],[]]
      for query in sorted(list(queryGroups)):
        dataRows[cover][scale][0].append(treeTypes[treeType][cover][scale][query][measurementType][0]);
        dataRows[cover][scale][1].append(treeTypes[treeType][cover][scale][query][measurementType][1]);
        dataRows[cover][scale][2].append(treeTypes[treeType][cover][scale][query][measurementType][2]);
  n_groups = len(queryGroups)
  index = np.arange(n_groups)
  bar_width = 1/float(len(coverSet)*len(scaleSet)+2+len(coverSet)*1)
  #colorBase = 1 / float(len(coverSet)*len(scaleSet)+1)
  colormap = plt.cm.gist_ncar
  colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)*len(scaleSet))]
  plt.gca().set_color_cycle(colors)
  bars = []
  for i, scale in enumerate(scaleSet):
    for j, cover in enumerate(coverSet):
      #colorValue = "{:f}".format(colorBase*(j*len(coverSet)+i))
      color=colors[i*len(scaleSet)+j]
      bars.append(ax.bar(index + (i*len(scaleSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale][0]), bar_width, color=color, edgecolor="{:f}".format(0.6), linewidth=2, hatch='//', label=cover + ' ' + scale + ' chunks parsing', log=False, bottom=1))
      bars.append(ax.bar(index + (i*len(scaleSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale][1]), bar_width, color=color, edgecolor="{:f}".format(0.4), linewidth=2, hatch='.', label=cover + ' ' + scale + ' chunks submitting', log=False, bottom=1+np.array(dataRows[cover][scale][0])))
      bars.append(ax.bar(index + (i*len(scaleSet) + j) * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale][2]), bar_width, color=color, label=cover + ' ' + scale + ' chunks executing', log=False, bottom=1+np.array(dataRows[cover][scale][0])+np.array(dataRows[cover][scale][1])))
  ax.set_xticks(index + 0.5)
  ax.set_xticklabels(sorted(list(queryGroups)), rotation=45, horizontalalignment='right')
  #plt.axis('tight')
  return bars

def getLabel(bar):
  return bar.get_label()

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
    treeTypes[treeType][cover][scale][query] = { "Execution Time":[(long(row[9])/1000),(long(row[10])/1000),(long(row[11])/1000)]}

for measurementType in ["Execution Time"]:
  for treeType in treeTypes.keys():
    coverSet = list(sorted(treeTypes[treeType].keys()))
    scaleSet = list(sorted(treeTypes[treeType][coverSet[0]].keys()))
    dataRows = {}
    longTimeQueries = set();
    midTimeQueries = set();
    queryGroups = set()
    for i, cover in enumerate(coverSet):
      for j, scale in enumerate(scaleSet):
        if i==0:
          queryGroups = set(treeTypes[treeType][cover][scale].keys())
        for query in queryGroups:
          if sum(treeTypes[treeType][cover][scale][query][measurementType]) > 4000:
            longTimeQueries.add(query)
            midTimeQueries.discard(query)
          elif (query not in longTimeQueries) and sum(treeTypes[treeType][cover][scale][query][measurementType]) > 500:
            midTimeQueries.add(query)
    queryGroups = queryGroups.difference(longTimeQueries).difference(midTimeQueries)

    # create diagramm sorted by cover
    nColl=len(queryGroups)+len(midTimeQueries)+len(longTimeQueries)
    fig = plt.figure()
    fig2 = plt.figure(figsize=(fig.get_figwidth()*(len(longTimeQueries)+len(midTimeQueries)+len(queryGroups))/5,fig.get_figheight()*2))
    ax1 = plt.subplot2grid((1,nColl+2), (0, 0), colspan=len(queryGroups))
    bars = plotSortedByCover(ax1, scaleSet, coverSet, dataRows, queryGroups, measurementType)
    plt.ylabel(measurementType + " (in sec)")
    ax2 = plt.subplot2grid((1,nColl+2), (0, len(queryGroups)+1), colspan=len(midTimeQueries))
    plotSortedByCover(ax2, scaleSet, coverSet, dataRows, midTimeQueries, measurementType)
    plt.xlabel("Queries")
    ax3 = plt.subplot2grid((1,nColl+2), (0, len(queryGroups)+len(midTimeQueries)+2), colspan=len(longTimeQueries))
    plotSortedByCover(ax3, scaleSet, coverSet, dataRows, longTimeQueries, measurementType)
    plt.suptitle(measurementType + ' for ' + treeType + ' trees sorted by cover strategy',y=1.18)
    plt.figlegend(bars, map(getLabel,bars), loc=3, ncol=3, bbox_to_anchor=(.05, 1, .8, 1), mode="expand", borderaxespad=0.)
    #plt.subplots_adjust(wspace=1)
    plt.savefig(outputDir+'/queryExecution_'+measurementType+'_treeType-'+treeType+'_sortedByCover.'+imageType, bbox_inches='tight')
    plt.close('all')

    # create diagramm sorted by scale
    nColl=len(queryGroups)+len(midTimeQueries)+len(longTimeQueries)
    fig = plt.figure()
    fig2 = plt.figure(figsize=(fig.get_figwidth()*(len(longTimeQueries)+len(midTimeQueries)+len(queryGroups))/5,fig.get_figheight()*2))
    ax1 = plt.subplot2grid((1,nColl+2), (0, 0), colspan=len(queryGroups))
    bars = plotSortedByScale(ax1, scaleSet, coverSet, dataRows, queryGroups, measurementType)
    plt.ylabel(measurementType + " (in sec)")
    ax2 = plt.subplot2grid((1,nColl+2), (0, len(queryGroups)+1), colspan=len(midTimeQueries))
    plotSortedByScale(ax2, scaleSet, coverSet, dataRows, midTimeQueries, measurementType)
    plt.xlabel("Queries")
    ax3 = plt.subplot2grid((1,nColl+2), (0, len(queryGroups)+len(midTimeQueries)+2), colspan=len(longTimeQueries))
    plotSortedByScale(ax3, scaleSet, coverSet, dataRows, longTimeQueries, measurementType)
    plt.suptitle(measurementType + ' for ' + treeType + ' trees sorted by number of chunks',y=1.18)
    plt.figlegend(bars, map(getLabel,bars), loc=3, ncol=3, bbox_to_anchor=(.05, 1, .8, 1), mode="expand", borderaxespad=0.)
    #plt.subplots_adjust(wspace=1)
    plt.savefig(outputDir+'/queryExecution_'+measurementType+'_treeType-'+treeType+'_sortedByNumberOfChunks.'+imageType, bbox_inches='tight')
    plt.close('all')
