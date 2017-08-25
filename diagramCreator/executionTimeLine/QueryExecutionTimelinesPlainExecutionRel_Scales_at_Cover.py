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

if len(sys.argv) < 4:
  print("You must have the following arguments: <executionTimelines.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

def isAborted(query):
  return query=="so \\#tp=8 \\#ds=3 sel=0.001" or query=="ss \\#tp=2 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.01" or query=="ss \\#tp=8 \\#ds=3 sel=0.001";

# for totalComputationalEffort, entropy, standard deviation
# for each tree type create a diagram that
# shows for each query
# the computational effort per cover in a separate bar

# required map: treetype -> cover -> query -> measurmentType -> value
#matplotlib.rcParams.update({'font.size': 28})

def plotSortedByCover(ax, scale, coverSet, dataRows, queryGroups, measurementType, baseCover):
  for i, cover in enumerate(coverSet):
    dataRows[cover] = []
    for query in sorted(list(queryGroups)):
      dataRows[cover].append((scales[scale][treeType][cover][query][measurementType][2]-scales[scale][treeType][baseCover][query][measurementType][2])*100/float(scales[scale][treeType][baseCover][query][measurementType][2]));
  n_groups = len(queryGroups)
  index = np.arange(n_groups)
  bar_width =  1/float(len(coverSet)+1)
  colormap = plt.cm.gist_ncar
  colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)+1+1)]
  colors = ["#EC84EE", "#FF0000", "#8B0000"]
  plt.gca().set_color_cycle(colors)
  bars = []
  for i, cover in enumerate(coverSet):
    color=colors[i+1]
    bars.append(ax.bar(index + i*bar_width+ 0.5*bar_width, np.array(dataRows[cover]), bar_width, color=color, label=scale + " " + cover+" slaves", linewidth=0.5))
  ax.set_xticks(index+0.5)
  ax.set_xticklabels(sorted(list(queryGroups)), rotation=45, horizontalalignment='right')
  #ax.set_yscale('symlog', linthreshy=1e1)
  plt.xlim(index.min(), index.max()+(len(coverSet)+1)*bar_width)
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
    cover += row[0].replace('_','\\_')
    scale = row[1]
    treeType = row[3]
    if not cover in scales:
      scales[cover] = {}
    if not treeType in scales[cover]:
      scales[cover][treeType] = {}
    if not scale in scales[cover][treeType]:
      scales[cover][treeType][scale] = {}
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[6])+1) + " \\#ds=" + row[7] + " sel=" + row[8]
    scales[cover][treeType][scale][query] = { "Execution Time":[(long(row[9])),(long(row[10])),(long(row[11]))]}

for measurementType in ["Execution Time"]:
  for scale in scales.keys():
    for treeType in scales[scale].keys():
      for baseCover in scales[scale][treeType].keys():
        coverSet = list(sorted(scales[scale][treeType].keys()))
        coverSet.remove(baseCover);
        dataRows = {}
        longTimeQueries = set();
        midTimeQueries = set();
        queryGroups = set(scales[scale][treeType][coverSet[0]].keys())
        for query in list(queryGroups):
          if isAborted(query):
            queryGroups.remove(query);
        #for i, cover in enumerate(coverSet):
        #  for query in queryGroups:
        #    if scales[scale][treeType][cover][query][measurementType][2] > 4000:
        #      longTimeQueries.add(query)
        #      midTimeQueries.discard(query)
        #    elif (query not in longTimeQueries) and scales[scale][treeType][cover][query][measurementType][2] > 500:
        #      midTimeQueries.add(query)
        #queryGroups = queryGroups.difference(longTimeQueries).difference(midTimeQueries)

        if imageType=="latex":
          latex.latexify(fig_height=7,scale=0.5)

        # create diagramm sorted by cover
        nColl=len(queryGroups)+len(midTimeQueries)+len(longTimeQueries)
        fig = plt.figure()
        #fig2 = plt.figure(figsize=(fig.get_figwidth()*(len(longTimeQueries)+len(midTimeQueries)+len(queryGroups))/5,fig.get_figheight()*2))
        bars = []
        if len(queryGroups) > 0:
          ax1 = plt.subplot2grid((1,nColl+2), (0, 0), colspan=len(queryGroups))
          bars = plotSortedByCover(ax1, scale, coverSet, dataRows, queryGroups, measurementType, baseCover)
        plt.ylabel("\\parbox{200pt}{\centering " + measurementType+'\\\\(change to '+baseCover+' slaves in \\%)'+"}")
        #plt.ylabel(measurementType + " (in sec)")
        if len(midTimeQueries) > 0:
          ax2 = plt.subplot2grid((1,nColl+2), (0, len(queryGroups)+1), colspan=len(midTimeQueries))
          bars = plotSortedByCover(ax2, scale, coverSet, dataRows, midTimeQueries, measurementType, baseCover)
        #plt.xlabel("Queries")
        if len(longTimeQueries) > 0:
          ax3 = plt.subplot2grid((1,nColl+2), (0, len(queryGroups)+len(midTimeQueries)+2), colspan=len(longTimeQueries))
          bars = plotSortedByCover(ax3, scale, coverSet, dataRows, longTimeQueries, measurementType, baseCover)
        #plt.suptitle('Plain query execution time for tree type ' + treeType + ' and ' + scale + ' chunks',y=1.05)
        plt.figlegend(bars, map(getLabel,bars), loc=3, ncol=1, bbox_to_anchor=(0.28, 0.9, 0.715, 1), mode="expand", borderaxespad=0., borderpad=0.2, labelspacing=0.2)
        #plt.subplots_adjust(left=0.1, right=1.3, wspace=4)
        fig.text(0.5, 0.01, 'Queries', ha='center')
        if imageType=="latex":
          if len(queryGroups) > 0 and len(midTimeQueries) > 0 and len(longTimeQueries) > 0:
            fig.subplots_adjust(left=0.15,bottom=0.26,right=0.999,top=0.93)
          else:
            fig.subplots_adjust(left=0.28,bottom=0.35,right=1.2,top=0.89)
        #  fig.tight_layout(rect=(0,0,0.9,1))
        if imageType=="latex":
          latex.savefig(outputDir,'plainQueryExecutionTime_executionTime_'+'relativeTo-'+baseCover+'_cover-'+scale+'_treeType-'+treeType)
        else:
          plt.savefig(outputDir+'/plainQueryExecutionTime_executionTime_'+'relativeTo-'+baseCover+'_cover-'+scale+'_treeType-'+treeType+'.'+imageType, bbox_inches='tight')
        plt.close('all')
