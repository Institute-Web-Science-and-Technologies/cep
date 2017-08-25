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

def isAborted(query):
  return query=="so \\#tp=8 \\#ds=3 sel=0.001" or query=="ss \\#tp=2 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.01" or query=="ss \\#tp=8 \\#ds=3 sel=0.001";

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    if row[2] != '1000000000':
      continue;
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + "HOP\\_"
    cover += row[0].replace('_','\\_')
    scale = row[1]
    treeType = row[4]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not cover in treeTypes[treeType]:
      treeTypes[treeType][cover] = {}
    if not scale in treeTypes[treeType][cover]:
      treeTypes[treeType][cover][scale] = {}
    query = ("ss" if row[6]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[7])+1) + " \\#ds=" + row[8] + " sel=" + row[9]
    treeTypes[treeType][cover][scale][query] = { "Total":long(row[10]), "Entropy":float(row[11]), "Workload Imbalance":float(row[13])}

for measurementType in ["Workload Imbalance"]:
  for treeType in treeTypes.keys():
    if treeType!='BUSHY':
      continue;
    for baseCover in treeTypes[treeType].keys():
      for baseScale in treeTypes[treeType][baseCover].keys():
        if not baseScale in treeTypes[treeType][baseCover]:
          continue;
        coverSet = list(sorted(treeTypes[treeType].keys()))
        dataRows = {}
        queryGroups = []
        for i, cover in enumerate(coverSet):
          dataRows[cover] = []
          if i == 0:
            queryGroups = list(sorted(treeTypes[treeType][cover][baseScale].keys()))
            #queryGroups = list(sorted(treeTypes[treeType][cover][baseScale].keys(), key=lambda query: ("b" if isAborted(query) else "a")+query))
          for query in queryGroups:
           if not baseScale in treeTypes[treeType][cover]:
             currentDataTransfer = 0
           else:
             currentDataTransfer = treeTypes[treeType][cover][baseScale][query][measurementType]
           dataRows[cover].append(currentDataTransfer);

        if imageType=="latex":
          latex.latexify(fig_height=3,scale=1)

        # create diagramm sorted by scale
        n_groups = len(queryGroups)
        fig, ax = plt.subplots()
        index = np.arange(n_groups)
        bar_width = 1/float(len(coverSet)+1)
        rects = []
        colormap = plt.cm.gist_ncar
        colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)+1)]
        c=0
        for i, cover in enumerate(coverSet):
          colorValue = colors[i+1]#colors[c]
          #print treeType+"-"+baseScale+"-"+cover+" finished: "+str(sum(map(float,dataRows[cover][0:6]))/float(len(dataRows[cover][0:6])))
          #print treeType+"-"+baseScale+"-"+cover+" aborted: "+str(sum(map(float,dataRows[cover][7:11]))/float(len(dataRows[cover][7:11])))
          #print "difference: "+ str(sum(map(float,dataRows[cover][7:11]))/float(len(dataRows[cover][7:11]))-sum(map(float,dataRows[cover][0:6]))/float(len(dataRows[cover][0:6])))
          rects.append(plt.bar(index + i*1*bar_width+0.5*bar_width, np.array(dataRows[cover]), bar_width, color=colorValue, label=cover, linewidth=0.5))
          c+=1
        plt.xlabel("Queries")
        plt.ylabel(measurementType)
        plt.xticks(index + 0.5, np.array(queryGroups))
        plt.xlim([min(index+0.5) - 0.5, max(index+0.5) + 0.5])
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        #plt.axvline(x=index[7],color="black")
        #plt.text(2,0.5,'finished')
        #plt.text(8.5,0.5,'aborted')
        #plt.axis('tight')
        #plt.title(measurementType + ' for ' + treeType + ' trees sorted by number of chunks' + " relative to " + baseCover,y=1.25)
        if imageType=="latex":
          plt.legend(bbox_to_anchor=(-0.5, 1.07, 1.5, .102), loc=3, ncol=2, mode="expand", borderaxespad=0., borderpad=0.2, labelspacing=0.2)
          fig.tight_layout(rect=(-0.04,-0.045,1.04,0.92))
          latex.savefig(outputDir,'computationalEffort'+'_'+measurementType+'_treeType-'+treeType+'_scale-'+baseScale)
        else:
          plt.legend(bbox_to_anchor=(-0.45, 1.04, 1.4, .103), loc=3, ncol=2, mode="expand", borderaxespad=0.)
          plt.savefig(outputDir+'/computationalEffort'+'_'+measurementType+'_treeType-'+treeType+'_scale-'+baseScale+'.'+imageType, bbox_inches='tight')
        plt.close('all')
