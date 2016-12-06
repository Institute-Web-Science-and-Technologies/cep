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

if len(sys.argv) != 4:
  print("You must have the following arguments: <chunkSizes.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

# required map: cover -> chunk -> value

covers = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[2]) != 0:
      cover += row[2] + "HOP_"
    cover += row[0]
    if not cover in covers:
      covers[cover] = {}
    scale = int(row[1]);
    if not scale in covers[cover]:
      covers[cover][scale] = {}
    for i in range(len(row)):
      if i >= 3 :
        chunk = i - 3
        covers[cover][scale][chunk] = long(row[i])

for measurementType in ["Chunk Sizes"]:
  coverSet = list(sorted(covers.keys()))
  scaleSet = list(sorted(covers[coverSet[0]]))
  dataRows = {}
  for i, cover in enumerate(coverSet):
    dataRows[cover] = {}
    for j, scale in enumerate(scaleSet):
      dataRows[cover][scale] = []
      for k, chunk in enumerate(covers[cover][scale]):
        dataRows[cover][scale].append(covers[cover][scale][chunk]);

  # create diagramms per scale
  for j, scale in enumerate(scaleSet):
    n_groups = scale
    fig, ax = plt.subplots()
    fig = plt.figure(figsize=(fig.get_figwidth()*(scale/20.),5))
    index = np.arange(n_groups)
    bar_width = 1/float(len(coverSet)+1)
    rects = []
    colormap = plt.cm.gist_ncar
    colors = [colormap(i) for i in np.linspace(0, 0.9, len(coverSet))]
    for i, cover in enumerate(coverSet):
      colorValue = colors[i]
      rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[cover][scale]), bar_width, color=colorValue, label=cover, log=False, bottom=0))
    plt.xlabel("Chunks")
    plt.ylabel(measurementType)
    plt.xticks(index + 0.5, np.array(list(range(scale)))+1)
    plt.setp(plt.gca().get_xticklabels())
    #plt.axis('tight')
    if scale < 20:
      plt.legend(bbox_to_anchor=(0., 1.06, 1., .106), loc=3, ncol=1, mode="expand", borderaxespad=0.)
      plt.title('Chunk sizes for ' + str(scale) + ' chunks', y=1.3)
    else:
      plt.legend(bbox_to_anchor=(0., 1.06, 1., .106), loc=3, ncol=3, mode="expand", borderaxespad=0.)
      plt.title('Chunk sizes for ' + str(scale) + ' chunks', y=1.15)
    plt.savefig(outputDir+'/chunkSizes_unsorted_scale='+str(scale)+'.'+imageType, bbox_inches='tight')

