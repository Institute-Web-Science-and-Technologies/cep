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
from matplotlib.ticker import ScalarFormatter
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
  return query=="so \\#tp=8 \\#ds=3 sel=0.001" or query=="ss \\#tp=2 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.001" or query=="ss \\#tp=8 \\#ds=1 sel=0.01" or query=="ss \\#tp=8 \\#ds=3 sel=0.001";

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    if row[2]!='1000000000':
      continue;
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + ("HOP\\_" if imageType=='latex' else "HOP_")
    cover += (row[0].replace("_","\\_") if imageType=='latex' else row[0])
    scale = row[1]
    treeType = row[4]
    query = ("ss" if row[6]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[7])+1) + " \\#ds=" + row[8] + " sel=" + row[9]
    #if isAborted(query):
    #  continue;
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not cover in treeTypes[treeType]:
      treeTypes[treeType][cover] = {}
    if not scale in treeTypes[treeType][cover]:
      treeTypes[treeType][cover][scale] = {}
    treeTypes[treeType][cover][scale][query] = { "Execution Time":long(row[12])}

for measurementType in ["Execution Time"]:
  for treeType in treeTypes.keys():
    if treeType!='BUSHY':
      continue;
    for baseCover in treeTypes[treeType].keys():
      for baseScale in treeTypes[treeType][baseCover].keys():
        if not baseScale in treeTypes[treeType][baseCover]:
          continue;
        coverSet = list(sorted(treeTypes[treeType].keys()))
        coverSet.remove(baseCover)
        dataRows = {}
        queryGroups = []
        for i, cover in enumerate(coverSet):
          dataRows[cover] = []
          if i == 0:
            queryGroups = list(sorted(treeTypes[treeType][cover][baseScale].keys()))
          for query in queryGroups:
           baseDataTransfer = treeTypes[treeType][baseCover][baseScale][query][measurementType]
           if not baseScale in treeTypes[treeType][cover]:
             currentDataTransfer = 0
           else:
             currentDataTransfer = treeTypes[treeType][cover][baseScale][query][measurementType]
           if baseDataTransfer > 0:
             dataRows[cover].append((currentDataTransfer-baseDataTransfer)/float(baseDataTransfer)*100);
           elif currentDataTransfer == 0:
             dataRows[cover].append(0);
           else:
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
        colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)+1+1)]
        c=0
        for i, cover in enumerate(coverSet):
          colorValue = colors[i+1+1]#colors[c]
          rects.append(plt.bar(index + i*1*bar_width+0.5*bar_width, np.array(dataRows[cover]), bar_width, color=colorValue, label=cover, linewidth=0.5))
          c+=1
        plt.xlabel("Queries")
        if imageType=="latex":
          plt.ylabel("\\parbox{200pt}{\centering " + measurementType+' (log scale,\\\\ change to '+baseCover + ' in \\%)'+"}")
        else:
          plt.ylabel(measurementType+' (log scale,\n change to '+baseCover + ' in %)')
        ymin, ymax = plt.ylim();
        plt.ylim(ymin if ymin <= -10 else -10,ymax)
        plt.xticks(index + 0.5, np.array(queryGroups) if imageType=='latex' else np.array(map(lambda x:queryNames[x],queryGroups)))
        plt.xlim([min(index+0.5) - 0.5, max(index+0.5) + 0.5])
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
        ax.set_yscale('symlog', linthreshy=1e1)
        ax.yaxis.set_major_formatter(ScalarFormatter())
        #plt.axis('tight')
        #plt.title(measurementType + ' for ' + treeType + ' trees sorted by number of chunks' + " relative to " + baseCover,y=1.25)
        if imageType=="latex":
          plt.legend(bbox_to_anchor=(0, 1.01, 1, .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
          fig.tight_layout(rect=(-0.04,-0.045,1.03,0.96))
          latex.savefig(outputDir,'executionTime'+'_relativeTo_'+baseCover+'_'+measurementType+'_treeType-'+treeType+'_scale-'+baseScale)
        else:
          plt.legend(bbox_to_anchor=(0, 1.04, 1, .103), loc=3, ncol=2, mode="expand", borderaxespad=0.)
          plt.savefig(outputDir+'/ExecutionTime'+'_relativeTo_'+baseCover+'_'+measurementType+'_treeType-'+treeType+'_scale-'+baseScale+'.'+imageType, bbox_inches='tight')
        plt.close('all')
