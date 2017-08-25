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

#matplotlib.rcParams.update({'font.size': 18})

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[2]) != 0:
      cover += row[2] + "HOP\\_"
    cover += row[0].replace('_','\\_')
    scale = row[1]
    treeType = row[3]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not cover in treeTypes[treeType]:
      treeTypes[treeType][cover] = {}
    if not scale in treeTypes[treeType][cover]:
      treeTypes[treeType][cover][scale] = {}
    query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[6])+1) + " \\#ds=" + row[7] + " sel=" + row[8]
    #if query=="ss \\#tp=8 \\#ds=1 sel=0.001" or query=="ss \\#tp=2 \\#ds=1 sel=0.01":
    #  continue;
    treeTypes[treeType][cover][scale][query] = { "Execution Time":long(row[9])}

for measurementType in ["Execution Time"]:
  for treeType in treeTypes.keys():
    for baseCover in treeTypes[treeType].keys():
      coverSet = list(sorted(treeTypes[treeType].keys()))
      scaleSet = list(sorted(treeTypes[treeType][coverSet[0]].keys()))
      coverSet.remove(baseCover)
      dataRows = {}
      queryGroups = []
      for i, cover in enumerate(coverSet):
        dataRows[cover] = {}
        for j, scale in enumerate(scaleSet):
          if i == 0:
            queryGroups = list(sorted(treeTypes[treeType][cover][scale].keys()))
          dataRows[cover][scale] = []
          for query in queryGroups:
            baseDataTransfer = treeTypes[treeType][baseCover][scale][query][measurementType]
            currentDataTransfer = treeTypes[treeType][cover][scale][query][measurementType]
            if baseDataTransfer > 0:
              dataRows[cover][scale].append((currentDataTransfer-baseDataTransfer)*100/float(baseDataTransfer));
            elif currentDataTransfer == 0:
              dataRows[cover][scale].append(0);
            else:
              dataRows[cover][scale].append(currentDataTransfer);

      if imageType=="latex":
        latex.latexify(scale=1)

      # create diagramm sorted by cover
      n_groups = len(queryGroups)
      fig, ax = plt.subplots()
      index = np.arange(n_groups)
      bar_width = 1/float(len(coverSet)*len(scaleSet)+1)
      rects = []
      colors = ["#ffd600", "#ff1924", "#0055c9", "#a5cf00", "#6200d9", "#82fcff", "#fc9200", "#00cfe6"]
      c=0
      for i, cover in enumerate(coverSet):
        for j, scale in enumerate(scaleSet):
          colorValue = colors[c]
          rects.append(plt.bar(index + 0.5*bar_width + i*1*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover, linewidth=0.5, log=True, bottom=0))
          c+=1
      plt.xlabel("Queries", labelpad=-3)
      plt.ylabel("\\parbox{200pt}{\centering " + measurementType+' (log scale, \\\\change to '+baseCover+' in \\%)'+"}")
      plt.xticks(index + 0.5, np.array(queryGroups))
      ax.tick_params(axis='x', which='major', pad=0)
      ax.set_yscale('symlog', linthreshy=1e1)
      plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
      #plt.axis('tight')
      #plt.title(measurementType + ' for ' + treeType + ' trees sorted by cover strategy' + " relative to " + baseCover,y=1.25)
      if imageType=="latex":
        plt.legend(bbox_to_anchor=(0, 1.03, 1, .102), loc=3, ncol=2, mode="expand", borderaxespad=0., handletextpad=0.2, borderpad=0.2, handlelength=1.8)
        fig.tight_layout(rect=(-0.04,-0.06,1.035,0.99))
        latex.savefig(outputDir,'QueryExecution'+'_relativeTo_'+baseCover+'_'+measurementType+'_treeType-'+treeType+'_forAll_covers_sortedByCover')
      else:
        plt.legend(bbox_to_anchor=(-0.2, 1.03, 1.2, .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig(outputDir+'/QueryExecution'+'_relativeTo_'+baseCover+'_'+measurementType+'_treeType-'+treeType+'_forAll_covers_sortedByCover.'+imageType, bbox_inches='tight')
      plt.close('all')
