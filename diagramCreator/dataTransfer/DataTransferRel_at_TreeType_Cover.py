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
  print("You must have the following arguments: <packageTransport.csv> <outputDir> <imageType>")
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
    if row[6]=='SUBJECT_SUBJECT_JOIN':
      continue;
    if row[2]!='1000000000':
      continue;
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + "HOP\\_"
    cover += row[0].replace('_','\\_')
    scale = row[1]
    treeType = row[4]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not scale in treeTypes[treeType]:
      treeTypes[treeType][scale] = {}
    if not cover in treeTypes[treeType][scale]:
      treeTypes[treeType][scale][cover] = {}
    query = ("ss" if row[6]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[7])+1) + " \\#ds=" + row[8] + " sel=" + row[9]
    treeTypes[treeType][scale][cover][query] = { "Data Transfer":long(row[10])}

for measurementType in ["Data Transfer"]:
  for treeType in treeTypes.keys():
    for baseScale in treeTypes[treeType].keys():
      for baseCover in treeTypes[treeType][baseScale].keys():
        scaleSet = list(sorted(treeTypes[treeType].keys()))
        scaleSet.remove(baseScale)
        dataRows = {}
        queryGroups = []
        for i, scale in enumerate(scaleSet):
          dataRows[scale] = []
          if i == 0:
            queryGroups = list(sorted(treeTypes[treeType][scale][baseCover].keys()))
          for query in queryGroups:
           baseDataTransfer = treeTypes[treeType][baseScale][baseCover][query][measurementType]
           currentDataTransfer = treeTypes[treeType][scale][baseCover][query][measurementType]
           if baseDataTransfer > 0:
             dataRows[scale].append((currentDataTransfer-baseDataTransfer)/float(baseDataTransfer)*100);
           elif currentDataTransfer == 0:
             dataRows[scale].append(0);
           else:
             dataRows[scale].append(currentDataTransfer);

        if imageType=="latex":
          latex.latexify(fig_height=7,scale=0.5)

        # create diagramm sorted by scale
        n_groups = len(queryGroups)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 1/float(len(scaleSet)+1)
        rects = []
        colormap = plt.cm.gist_ncar
        if baseCover == "HASH":
          colors = ["#00fc3e", "#32cd32", "#006400"]
        elif baseCover == "HIERARCHICAL":
          colors = ["#FFCD05", "#FF8C00", "#FF4500"]
        else:
          colors = ["#EC84EE", "#FF0000", "#8B0000"]
        c=0
        for i, scale in enumerate(scaleSet):
          colorValue = colors[i+1]#colors[c]
          rects.append(plt.bar(index + i*1*bar_width+0.5*bar_width, np.array(dataRows[scale]), bar_width, color=colorValue, label=baseCover+" "+scale+" slaves", linewidth=0.5))
          c+=1
        plt.xlabel("Queries")
        plt.ylabel("\\parbox{200pt}{\centering " + measurementType+'\\\\(change to '+baseCover+"\\\\at "+baseScale + ' slaves in \\%)'+"}")
        ax.yaxis.set_label_coords(-0.15, 0.45)
        plt.xticks(index + 0.5, np.array(queryGroups))
        plt.xlim([min(index+0.5) - 0.5, max(index+0.5) + 0.5])
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        #plt.axis('tight')
        #plt.title(measurementType + ' for ' + treeType + ' trees sorted by number of chunks' + " relative to " + baseScale,y=1.25)
        if imageType=="latex":
          if baseCover == "HASH":
            plt.legend(bbox_to_anchor=(-0.37, 1.05, 1.37, .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
            fig.tight_layout(rect=(-0.04,-0.045,1.04,0.96))
          else:
            plt.legend(bbox_to_anchor=(0, 1.02, 1, 1), loc=3, ncol=1, mode="expand", borderaxespad=0., borderpad=0.2, labelspacing=0.2)
            fig.tight_layout(rect=(-0.04,-0.045,1.04,0.95))
          latex.savefig(outputDir,'dataTransfer'+'_relativeTo_'+baseScale+'_'+measurementType+'_treeType-'+treeType+'_cover-'+baseCover)
        else:
          plt.legend(bbox_to_anchor=(-0.45, 1.04, 1.4, .103), loc=3, ncol=2, mode="expand", borderaxespad=0.)
          plt.savefig(outputDir+'/DataTransfer'+'_relativeTo_'+baseScale+'_'+measurementType+'_treeType-'+treeType+'_cover-'+baseCover+'.'+imageType, bbox_inches='tight')
        plt.close('all')
