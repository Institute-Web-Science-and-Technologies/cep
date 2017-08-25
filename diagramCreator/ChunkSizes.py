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
  print("You must have the following arguments: <chunkSizes.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

# required map: cover -> chunk -> value
if imageType!='latex':
  matplotlib.rcParams.update({'font.size': 16})

covers = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[3]) != 0:
      cover += row[3] + ("HOP\\_" if imageType=='latex' else "HOP_")
    cover += (row[0].replace("_","\\_") if imageType=='latex' else row[0])
    if not cover in covers:
      covers[cover] = {}
    scale = int(row[1]);
    if not scale in covers[cover]:
      covers[cover][scale] = {}
    dataset = long(row[2]);
    if not dataset in covers[cover][scale]:
      covers[cover][scale][dataset] = {}
    for i in range(len(row)):
      if i >= 4 :
        chunk = i - 4
        covers[cover][scale][dataset][chunk] = long(row[i])

for measurementType in ["Chunk Sizes"]:
  coverSet = list(sorted(covers.keys()))
  scaleSet = set()
  for cover in coverSet:
    scaleSet = scaleSet.union(covers[cover].keys())
  scaleSet = list(sorted(scaleSet))
  datasetSet = set()
  for cover in coverSet:
    for scale in scaleSet:
      datasetSet = datasetSet.union(covers[cover][scale].keys())
  datasetSet = list(sorted(datasetSet))
  dataRows = {}
  for i, cover in enumerate(coverSet):
    dataRows[cover] = {}
    for j, scale in enumerate(scaleSet):
      dataRows[cover][scale] = {}
      for l, dataset in enumerate(datasetSet):
        if dataset in covers[cover][scale]:
          dataRows[cover][scale][dataset] = []
          for k, chunk in enumerate(covers[cover][scale][dataset]):
            dataRows[cover][scale][dataset].append(covers[cover][scale][dataset][chunk]);

  # create diagramms per scale
  for dataset in datasetSet:
    for j, scale in enumerate(scaleSet):
      if not dataset in dataRows[coverSet[0]][scale]:
        continue;
      if imageType=="latex":
        if scale==10:
          latex.latexify(fig_height=6,scale=0.4)
        elif scale==20:
          latex.latexify(scale=1)
        else:
          latex.latexify(fig_height=2,scale=1.1)
      n_groups = scale
      fig, ax = plt.subplots()
      #fig = plt.figure(figsize=(fig.get_figwidth()*(scale/20.),3))
      index = np.arange(n_groups)
      bar_width = 1/float(len(coverSet)+1)
      rects = []
      colormap = plt.cm.gist_ncar
      colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet)+1)]
      for i, cover in enumerate(coverSet):
        colorValue = colors[i+1]
        rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(sorted(dataRows[cover][scale][dataset],reverse=True)), bar_width, color=colorValue, label=cover, log=False, bottom=0, linewidth=0.5))
      plt.xlabel("Chunks")
      plt.ylabel("Number of Triples")
      plt.xticks(index + 0.5, np.array(list(range(scale))))
      plt.setp(plt.gca().get_xticklabels())#, rotation=0, horizontalalignment='right')
      #plt.axis('tight')
      #fig_size = plt.rcParams["figure.figsize"]
      #fig_size[0] = fig_size[0]
      #fig_size[1] = fig_size[1]
      #plt.legend(bbox_to_anchor=(-0.25, 1.1, 1.25, .102), loc=3, ncol=2, mode="expand", borderaxespad=0., fontsize=14)
      if imageType=="latex":
        if scale==10:
          plt.legend(bbox_to_anchor=(0, 1.2, 1, .102), loc=3, ncol=1, mode="expand", borderaxespad=0.)
        else:
          plt.legend()
      else:
        plt.legend()
      #plt.title('Chunk sizes for ' + str(scale) + ' chunks', y=1.05)
      if imageType=="latex":
        if scale==10:
          fig.tight_layout(rect=(-0.05,-0.05,1.05,0.75))
        elif scale==40:
          fig.tight_layout(rect=(-0.018,-0.055,1.018,1.05))
        else:
          fig.tight_layout(rect=(-0.035,-0.06,1.034,1.05))
      if imageType=="latex":
        latex.savefig(outputDir,'chunkSizes_scale='+str(scale)+'_dataset_'+str(dataset))
      else:
        plt.savefig(outputDir+'/chunkSizes_scale='+str(scale)+'_dataset_'+str(dataset)+'.'+imageType, bbox_inches='tight')
      plt.close(fig)
