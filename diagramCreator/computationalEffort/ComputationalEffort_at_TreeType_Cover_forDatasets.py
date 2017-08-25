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

def isAborted(query):
  return query=="so \\#tp=8 \\#ds=3 sel=0.001" or query=="so \\#tp=8 \\#ds=3 sel=0.01" or query=="ss \\#tp=2 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.01" or query=="ss \\#tp=8 \\#ds=3 sel=0.001";

def prettyPrint(x):
  return str(x/1000000000)+'G' if x/1000000000>0 else str(x/1000000)+'M'

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    if row[1] != '20':
      continue;
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + ("HOP\\_" if imageType=='latex' else "HOP_")
    cover += (row[0].replace("_","\\_") if imageType=='latex' else row[0])
    scale = long(row[2])
    treeType = row[4]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not scale in treeTypes[treeType]:
      treeTypes[treeType][scale] = {}
    if not cover in treeTypes[treeType][scale]:
      treeTypes[treeType][scale][cover] = {}
    query = ("ss" if row[6]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[7])+1) + " \\#ds=" + row[8] + " sel=" + row[9]
    #if isAborted(query):
    #  continue;
    treeTypes[treeType][scale][cover][query] = { "Total":long(row[10]), "Entropy":float(row[11]), "Workload Imbalance":float(row[13])}

def difference(a, b):
  c = []
  for i, aValue in enumerate(a):
     c.append((float(b[i])-float(aValue))/aValue*100)
  return c;


for measurementType in ["Workload Imbalance"]:
  for treeType in treeTypes.keys():
    if treeType!='BUSHY':
      continue;
    for baseScale in treeTypes[treeType].keys():
      for baseCover in treeTypes[treeType][baseScale].keys():
        scaleSet = list(sorted(treeTypes[treeType].keys()))
        dataRows = {}
        queryGroups = []
        for i, scale in enumerate(scaleSet):
          dataRows[scale] = []
          if i == 0:
            #queryGroups = list(sorted(treeTypes[treeType][scale][baseCover].keys()))
            queryGroups = list(sorted(treeTypes[treeType][scale][baseCover].keys(), key=lambda query: ("b" if isAborted(query) else "a")+query))
          for query in queryGroups:
           currentDataTransfer = treeTypes[treeType][scale][baseCover][query][measurementType]
           if currentDataTransfer == 0:
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
        #print "\n" + treeType + " " + prettyPrint(baseScale) + " " + baseCover
        for i, scale in enumerate(scaleSet):
          colorValue = colors[i]#colors[c]
          #if i>0:
            #change=difference(dataRows[scaleSet[0]],dataRows[scale])
            #print prettyPrint(scale) + ": " + str(dataRows[scale])
            #print treeType+"-"+baseCover+"-"+prettyPrint(scale)+": "+str(change)+" average: "+str(sum(change)/len(change))+" median: "+str((sorted(change)[5]+sorted(change)[6])/2.)
          rects.append(plt.bar(index + i*1*bar_width+0.5*bar_width, np.array(dataRows[scale]), bar_width, color=colorValue, label=baseCover+" "+prettyPrint(scale)+" triples", linewidth=0.5))
          c+=1
        plt.xlabel("Queries")
        plt.ylabel(measurementType)
        plt.xticks(index + 0.5, np.array(queryGroups) if imageType=='latex' else np.array(map(lambda x:queryNames[x],queryGroups)))
        plt.xlim([min(index+0.5) - 0.5, max(index+0.5) + 0.5])
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        plt.axvline(x=index[6],color="black")
        plt.text(2,0.7,'finished')
        plt.text(8.5,0.7,'aborted')
        #plt.axis('tight')
        #plt.title(measurementType + ' for ' + treeType + ' trees sorted by number of chunks' + " relative to " + baseScale,y=1.25)
        if imageType=="latex":
          plt.legend(bbox_to_anchor=(0, 1.01, 1, .102), loc=3, ncol=1, mode="expand", borderaxespad=0., borderpad=0.2, labelspacing=0.2, handletextpad=0.2, handlelength=1)
          fig.tight_layout(rect=(-0.04,-0.045,1.04,0.91))
          latex.savefig(outputDir,'computationalEffort'+'_'+measurementType+'_treeType-'+treeType+'_cover-'+baseCover + '_forDatasets')
        else:
          plt.legend(bbox_to_anchor=(0, 1.04, 1, .103), loc=3, ncol=1, mode="expand", borderaxespad=0.)
          plt.savefig(outputDir+'/computationalEffort'+'_'+measurementType+'_treeType-'+treeType+'_cover-'+baseCover + '_forDatasets'+'.'+imageType, bbox_inches='tight')
        plt.close('all')
