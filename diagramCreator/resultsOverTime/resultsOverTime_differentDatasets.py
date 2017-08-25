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
from itertools import cycle
import latexPlot as latex

if len(sys.argv) != 4:
  print("You must have the following arguments: <computationalEffort.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

def isAborted(query):
  return query=="so-tp8-ds3-sel0.001" or query=="so-tp8-ds3-sel0.01" or query=="ss-tp2-ds1-sel0.001" or query=="ss-tp8-ds1-sel0.001" or query=="ss-tp8-ds1-sel0.01" or query=="ss-tp8-ds3-sel0.001";

def prettyPrint(x):
  return str(x/1000000000)+'G' if x/1000000000>0 else str(x/1000000)+'M'

queries = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    if row[4]!='BUSHY':
      continue;
    if row[1]!='20':
      continue;
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + "HOP\\_"
    cover += row[0].replace('_','\\_')
    scale = long(row[2])
    treeType = row[4]
    query = ("ss" if row[6]=='SUBJECT_SUBJECT_JOIN' else "so") + "-tp" + str(int(row[7])+1) + "-ds" + row[8] + "-sel" + row[9]
    #query = ("ss" if row[5]=='SUBJECT_SUBJECT_JOIN' else "so") + " \\#tp=" + str(int(row[6])+1) + " \\#ds=" + row[7] + " sel=" + row[8]
    row2 = reader.next();
    row = row[10:len(row)]
    row_time = []
    row_time.append(0)
    for time in row:
      row_time.append((long(time)-1)/float(1000))
      row_time.append(long(time)/float(1000))
    row2 = row2[10:len(row2)]
    row_percent = []
    row_percent.append(0)
    previous = 0
    for percent in row2:
      row_percent.append(previous)
      previous = float(percent)
      row_percent.append(previous)
    if not query in queries.keys():
      queries[query] = {}
    if not cover in queries[query].keys():
      queries[query][cover] = {}
    if not treeType in queries[query][cover].keys():
      queries[query][cover][treeType] = {}
    queries[query][cover][treeType][scale] = { 'time':row_time, 'percent':row_percent}

if imageType=="latex":
  latex.latexify(fig_height=2.5,fig_width=3,scale=0.7)

for query in sorted(queries.keys()):
  if not isAborted(query):
    continue;
  for cover in sorted(queries[query].keys()):
    for treeType in sorted(queries[query][cover].keys()):
      # create diagram
      fig, ax = plt.subplots()
      scaleSet = sorted(queries[query][cover][treeType].keys())
      colormap = plt.cm.gist_ncar
      if cover == "HASH":
        colors = ["#00fc3e", "#32cd32", "#006400"]
      elif cover == "HIERARCHICAL":
        colors = ["#FFCD05", "#FF8C00", "#FF4500"]
      else:
        colors = ["#EC84EE", "#FF0000", "#8B0000"]
      for i, scale in enumerate(scaleSet):
        colorValue = colors[i]
        plt.plot(queries[query][cover][treeType][scale]['time'], queries[query][cover][treeType][scale]['percent'], label=cover+" "+prettyPrint(scale)+' triples', color=colorValue, linewidth=2)
      #plt.title(query + ' for ' + treeType + ' trees and '+cover+' cover',y=1.02)
      plt.xlabel("Time (in sec)")
      plt.ylabel("\\% of returned results")
      plt.axis('tight')
      if imageType=="latex":
        plt.legend(bbox_to_anchor=(0, 1.02, 1, 0), loc=3, ncol=1, mode="expand", borderaxespad=0., borderpad=0.2, labelspacing=0.2, handletextpad=0.2, handlelength=1.2)
        fig.tight_layout(rect=(-0.04,-0.04,1.04,0.82))
        latex.savefig(outputDir,'resultsOverTimeScale_'+query + '_cover-'+ cover)# + '_'+treeType)
      else:
        plt.legend(loc='upper left', ncol=len(sorted(queries[query][cover][treeType].keys())), bbox_to_anchor=(0., -0.2, 1., .102))
        plt.savefig(outputDir+'/resultsOverTime_'+query + '_cover-'+ cover + '_'+treeType +'.'+imageType, bbox_inches='tight')
      plt.close(fig)

