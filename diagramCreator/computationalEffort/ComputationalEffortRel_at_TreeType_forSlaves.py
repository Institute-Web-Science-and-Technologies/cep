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

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + "HOP\\_"
    cover += row[0].replace('_','\\_')
    scale = row[1]
    dataset = row[2]
    treeType = row[4]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not cover in treeTypes[treeType]:
      treeTypes[treeType][cover] = {}
    if not scale in treeTypes[treeType][cover]:
      treeTypes[treeType][cover][scale] = {}
    if not dataset in treeTypes[treeType][cover][scale]:
      treeTypes[treeType][cover][scale][dataset] = {}
    query = ("ss" if row[6]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[7])+1) + " \\#ds=" + row[8] + " sel=" + row[9]
    treeTypes[treeType][cover][scale][dataset][query] = { "Computational Effort":long(row[10]), "Entropy":float(row[11]), "Workload Imbalance":float(row[13])}

for measurementType in ["Computational Effort"]:
  for treeType in treeTypes.keys():
    for baseCover in treeTypes[treeType].keys():
      for baseScale in treeTypes[treeType][baseCover].keys():
        coverSet = list(sorted(treeTypes[treeType].keys()))
        scaleSet = list(sorted(treeTypes[treeType][coverSet[0]].keys()))
        dataRows = {}
        queryGroups = []
        for i, cover in enumerate(coverSet):
          dataRows[cover] = {}
          for j, scale in enumerate(scaleSet):
            if i == 0:
              queryGroups = list(sorted(treeTypes[treeType][cover][scale]['1000000000'].keys()))
            dataRows[cover][scale] = []
            for query in queryGroups:
              baseDataTransfer = treeTypes[treeType][baseCover][baseScale]['1000000000'][query][measurementType]
              currentDataTransfer = treeTypes[treeType][cover][scale]['1000000000'][query][measurementType]
              if baseDataTransfer > 0:
                dataRows[cover][scale].append((currentDataTransfer-baseDataTransfer)/float(baseDataTransfer)*100);
              elif currentDataTransfer == 0:
                dataRows[cover][scale].append(0);
              else:
                dataRows[cover][scale].append(currentDataTransfer);

        if imageType=="latex":
          latex.latexify(scale=1)

        # create diagramm sorted by scale
        n_groups = len(queryGroups)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 1/float(len(coverSet)*len(scaleSet)+2+len(coverSet)*1)
        rects = []
        colormap = plt.cm.gist_ncar
        colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)*len(scaleSet))]
        c=0
        #print "\n" + treeType + " " + baseScale + " " + baseCover
        for i, scale in enumerate(scaleSet):
          for j, cover in enumerate(coverSet):
            #print scale + " " + cover + ": " + str(dataRows[cover][scale])
            colorValue = colors[j*len(scaleSet)+i]#colors[c]
            rects.append(plt.bar(index + c * bar_width + bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover  + ' ' + scale + ' slaves', linewidth=0.5))
            c+=1
        plt.xlabel("Queries")
        plt.ylabel("\\parbox{200pt}{\centering " + measurementType+'\\\\(change to '+baseCover + '\\\\at ' + baseScale + ' slaves' +' in \\%)'+"}")
        plt.xticks(index + 0.5, np.array(queryGroups))
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        #ax.set_yscale('symlog'), linthreshy=1e1)
        #plt.axis('tight')
        #plt.title(measurementType + ' for ' + treeType + ' trees sorted by number of chunks' + " relative to " + baseCover,y=1.25)
        if imageType=="latex":
          plt.legend(bbox_to_anchor=(-0.113, 1.05, 1.113, .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
          fig.tight_layout(rect=(-0.02,-0.035,1.02,0.87))
          latex.savefig(outputDir,'computationalEffort'+'_relativeTo_'+baseCover+baseScale+'_'+measurementType+'_treeType-'+treeType+'_forAll_covers_sortedByNumberOfChunks')
        else:
          plt.legend(bbox_to_anchor=(-0.4, 1.04, 1.4, .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
          plt.savefig(outputDir+'/computationalEffort'+'_relativeTo_'+baseCover+baseScale+'_'+measurementType+'_treeType-'+treeType+'_forAll_covers_sortedByNumberOfChunks.'+imageType, bbox_inches='tight')
        plt.close('all')
