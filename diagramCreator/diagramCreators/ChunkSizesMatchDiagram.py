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

import os
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import DiagramDrawer
import Utilities

def createDiagram(inputFileChunkSizes, inputFileOperationOutput, dataRowFilter, outputDir, outputFileName, diagramScale, legendScale, legendColumns, isLatex, sort=True, logScale=False, y2LogScale=False):
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)
  outputFileName = Utilities.extendFileName(outputFileName, "-"+str(dataRowFilter["numberOfChunks"])+"Chunks"+"-"+Utilities.getDatasetSize(dataRowFilter,isLatex)+"Triples"+"-"+Utilities.getCoverName(dataRowFilter, False)+"-", isLatex)
  # collect data
  y2Values = None
  y2LegendNames = None
  y2LegendColours = None
  if not inputFileChunkSizes is None:
    # chunk sizes
    y2Values = []
    y2LegendNames = []
    y2LegendColours = []
    with open(inputFileChunkSizes, 'rb') as f:
      reader = csv.reader(f, delimiter='\t')
      reader.next()
      for row in reader:
        if Utilities.isMatch(row,dataRowFilter):
          y2Values.append(map(long,row[4:]))
          y2LegendNames.append("Chunk Size")
          y2LegendColours.append("grey")
  # number of matches per chunk
  dataRowFilters = []
  dataRowFilters.append(dataRowFilter)
  queries, abortedQueries = Utilities.getQueries(inputFileOperationOutput, dataRowFilters, isLatex, onlyFinishedQueries=True)
  ## determine slave identifiers
  slaves = list()
  with open(inputFileOperationOutput, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
      query = Utilities.getQuery(isLatex,row)
      if Utilities.isMatch(row,dataRowFilter) and (query in queries):
        operations = row[10:len(row)]
        for i, value in enumerate(operations):
          if i % 3 == 0:
            slaveName = operations[i]
            if not slaveName in slaves:
              slaves.append(slaveName)
  slaves = sorted(slaves)
  ## compute matches
  legendNames = []
  legendColours = []
  values = []
  legendNames.extend([""]*len(queries))
  values.extend([0]*len(queries))
  colormap = plt.cm.gist_ncar
  legendColours.extend([colormap(i) for i in np.linspace(0, 0.9, len(queries))])
  with open(inputFileOperationOutput, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
      query = Utilities.getQuery(isLatex,row)
      if Utilities.isMatch(row,dataRowFilter) and (query in queries):
        index = queries.index(query)
        legendNames[index]=query
        values[index]=[0.]*len(slaves)
        operations = row[10:len(row)]
        for i, value in enumerate(operations):
          if i % 3 == 0 and "match" in operations[i+1]:
            slaveIndex = slaves.index(operations[i])
            values[index][slaveIndex] = values[index][slaveIndex] + float(operations[i+2])
  # draw diagram
  DiagramDrawer.drawBarDiagram(outputDir + os.sep + outputFileName,isLatex,"Number of Matched Triples",1.5,"Slaves",1.5,list(range(1,len(values[0])+1)),False,legendNames,legendColours,values,legendScale,legendColumns,diagramScale,logScale=logScale, y2Label="Number of Triples", y2LabelPad=1.5, y2Values=y2Values, y2LegendNames=y2LegendNames, y2LegendColours=y2LegendColours, y2LogScale=y2LogScale)
