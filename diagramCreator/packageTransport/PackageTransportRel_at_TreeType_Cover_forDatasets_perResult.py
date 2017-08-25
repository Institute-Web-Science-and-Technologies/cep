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

queryNames = {
  "so \\#tp=2 \\#ds=1 sel=0.001": "Q1",
  "so \\#tp=2 \\#ds=1 sel=0.01": "Q2",
  "so \\#tp=8 \\#ds=1 sel=0.001": "Q3",
  "so \\#tp=8 \\#ds=1 sel=0.01": "Q4",
  "so \\#tp=8 \\#ds=3 sel=0.001": "Q5",
  "so \\#tp=8 \\#ds=3 sel=0.01": "Q6",
  "ss \\#tp=2 \\#ds=1 sel=0.001": "Q7",
  "ss \\#tp=2 \\#ds=1 sel=0.01": "Q8",
  "ss \\#tp=8 \\#ds=1 sel=0.001": "Q9",
  "ss \\#tp=8 \\#ds=1 sel=0.01": "Q10",
  "ss \\#tp=8 \\#ds=3 sel=0.001": "Q11",
  "ss \\#tp=8 \\#ds=3 sel=0.01": "Q12"
}


if imageType!='latex':
  matplotlib.rcParams.update({'font.size': 16})

resultSetSize = {
  "so \\#tp=2 \\#ds=1 sel=0.001":{"500M":855, "1G":1262, "2G":2961},
  "so \\#tp=2 \\#ds=1 sel=0.01":{"500M":86093, "1G":127169, "2G":173281},
  "so \\#tp=8 \\#ds=1 sel=0.001":{"500M":5903, "1G":61358, "2G":596701},
  "so \\#tp=8 \\#ds=1 sel=0.01":{"500M":241, "1G":1365, "2G":144115},
  "so \\#tp=8 \\#ds=3 sel=0.001":{"500M":1000000, "1G":1000000, "2G":1000000},
  "so \\#tp=8 \\#ds=3 sel=0.01":{"500M":327984, "1G":754495, "2G":1000000},
  "ss \\#tp=2 \\#ds=1 sel=0.001":{"500M":1000000, "1G":1000000, "2G":1000000},
  "ss \\#tp=2 \\#ds=1 sel=0.01":{"500M":65081, "1G":104776, "2G":148389},
  "ss \\#tp=8 \\#ds=1 sel=0.001":{"500M":1000000, "1G":1000000, "2G":1000000},
  "ss \\#tp=8 \\#ds=1 sel=0.01":{"500M":1000000, "1G":1000000, "2G":1000000},
  "ss \\#tp=8 \\#ds=3 sel=0.001":{"500M":1000000, "1G":1000000, "2G":1000000},
  "ss \\#tp=8 \\#ds=3 sel=0.01":{"500M":4, "1G":12, "2G":60}
}

def isAborted(query):
  return query=="so \\#tp=8 \\#ds=3 sel=0.001" or query=="so \\#tp=8 \\#ds=3 sel=0.01" or query=="ss \\#tp=2 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.01" or query=="ss \\#tp=8 \\#ds=3 sel=0.001";

def prettyPrint(x):
  return str(x/1000000000)+'G' if x/1000000000>0 else str(x/1000000)+'M'

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    if row[6]=='SUBJECT_SUBJECT_JOIN':
      continue;
    if row[1]!='20':
      continue;
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + ("HOP\\_" if imageType=='latex' else "HOP_")
    cover += (row[0].replace("_","\\_") if imageType=='latex' else row[0])
    scale = long(row[2])
    treeType = row[4]
    query = ("ss" if row[6]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[7])+1) + " \\#ds=" + row[8] + " sel=" + row[9]
    if isAborted(query):
      continue;
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not scale in treeTypes[treeType]:
      treeTypes[treeType][scale] = {}
    if not cover in treeTypes[treeType][scale]:
      treeTypes[treeType][scale][cover] = {}
    treeTypes[treeType][scale][cover][query] = { "Transferred Packages":long(row[10])}

for measurementType in ["Transferred Packages"]:
  for treeType in treeTypes.keys():
    if treeType!='BUSHY':
      continue;
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
          latex.latexify(fig_height=3.5,scale=1)

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
          rects.append(plt.bar(index + i*1*bar_width+0.5*bar_width, np.array(dataRows[scale]), bar_width, color=colorValue, label=baseCover+" "+prettyPrint(scale)+" triples", linewidth=0.5))
          c+=1
        plt.xlabel("Queries")
        if imageType=="latex":
          plt.ylabel("\\parbox{200pt}{\centering \\# " + measurementType+' per Query Result\\\\(change to '+prettyPrint(baseScale) + ' triples in \\%)'+"}")
        else:
          plt.ylabel("# "+measurementType+' per Query Result\n(change to '+prettyPrint(baseScale)+' triples in %)')
        ax.yaxis.set_label_coords(-0.15, 0.45)
        plt.xticks(index + 0.5, np.array(queryGroups) if imageType=='latex' else np.array(map(lambda x:queryNames[x],queryGroups)))
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
          latex.savefig(outputDir,'packageTransport'+'_relativeTo_'+prettyPrint(baseScale)+'_'+measurementType+'_treeType-'+treeType+'_cover-'+baseCover+"_perQueryResult")
        else:
          plt.legend(bbox_to_anchor=(0, 1.04, 1, .103), loc=3, ncol=1, mode="expand", borderaxespad=0.)
          plt.savefig(outputDir+'/PackageTransport'+'_relativeTo_'+prettyPrint(baseScale)+'_'+measurementType+'_treeType-'+treeType+'_cover-'+baseCover+"_perQueryResult"+'.'+imageType, bbox_inches='tight')
        plt.close('all')
