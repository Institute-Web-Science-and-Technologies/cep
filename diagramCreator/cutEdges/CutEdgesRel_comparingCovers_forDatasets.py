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

def prettyPrint(x):
  return str(x/1000000000)+'G' if x/1000000000>0 else str(x/1000000)+'M'

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
    if row[1]!='20':
      continue;
    cover = row[0].replace('_','\\_')
    scale = long(row[2])
    if not cover in treeTypes:
      treeTypes[cover] = {}
    if not scale in treeTypes[cover]:
      treeTypes[cover][scale] = {}
    treeTypes[cover][scale] = { "\\# Cut Edges":long(row[3])}

for measurementType in ["\\# Cut Edges"]:
    for baseCover in treeTypes.keys():
      coverSet = list(sorted(treeTypes.keys()))
      coverSet.remove(baseCover)
      dataRows = {}
      for i, cover in enumerate(coverSet):
        dataRows[cover] = []
        for scale in sorted(treeTypes[baseCover].keys()):
          base = treeTypes[baseCover][scale][measurementType]
          current = treeTypes[cover][scale][measurementType]
          if base > 0:
            dataRows[cover].append((current-base)/float(base)*100);
          elif currentDataTransfer == 0:
            dataRows[cover].append(0);
          else:
            dataRows[cover].append(current);

      if imageType=="latex":
        latex.latexify(scale=0.5)

      # create diagramm sorted by scale
      n_groups = len(treeTypes[baseCover].keys())
      fig, ax = plt.subplots()
      index = np.arange(n_groups)
      bar_width = 1/float(len(coverSet)+1)
      rects = []
      colormap = plt.cm.gist_ncar
      #if baseCover == "HASH":
        #colors = ["#00fc3e", "#32cd32", "#006400"]
      #elif baseCover == "HIERARCHICAL":
        #colors = ["#FFCD05", "#FF8C00", "#FF4500"]
      #else:
        #colors = ["#EC84EE", "#FF0000", "#8B0000"]
      c=0
      for i, cover in enumerate(coverSet):
        colorValue = "#00fc3e" if cover == "HASH" else "#FFCD05" if cover == "HIERARCHICAL" else "#EC84EE" #colors[i]#colors[c]
        rects.append(plt.bar(index + i*1*bar_width+0.5*bar_width, np.array(dataRows[cover]), bar_width, color=colorValue, label=cover, linewidth=0.5))
        c+=1
      plt.xlabel("Number of Chunks")
      plt.ylabel("\\parbox{200pt}{\centering " + measurementType+'\\\\(change to '+baseCover+ ' in \\%)'+"}")
      ax.yaxis.set_label_coords(-0.15, 0.45)
      plt.xticks(index + 0.5, np.array(map(prettyPrint,sorted(treeTypes[baseCover].keys()))))
      plt.xlim([min(index+0.5) - 0.5, max(index+0.5) + 0.5])
      #plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
      #plt.axis('tight')
      #plt.title(measurementType + ' for ' + treeType + ' trees sorted by number of chunks' + " relative to " + baseScale,y=1.25)
      if imageType=="latex":
        plt.legend(bbox_to_anchor=(0, 1.02, 1, 1), loc=3, ncol=2, mode="expand", borderaxespad=0., borderpad=0.2, labelspacing=0.2, handlelength=1.5, handletextpad=0.2)
        fig.tight_layout(rect=(-0.04,-0.05,1.04,0.99))
        latex.savefig(outputDir,'cutEdges'+'_relativeTo_'+baseCover+'_comparingCoversForDatasets')
      else:
        plt.legend(bbox_to_anchor=(-0.45, 1.04, 1.4, .103), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.savefig(outputDir+'/'+'cutEdges'+'_relativeTo_'+baseCover+'_comparingCoversForDatasets'+'.'+imageType, bbox_inches='tight')
      plt.close('all')
