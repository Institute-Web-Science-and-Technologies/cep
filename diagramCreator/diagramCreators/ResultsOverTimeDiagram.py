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
import re
import DiagramDrawer
import Utilities

def createDiagram(inputFile, dataRowFilters, outputDir, outputFileName, diagramScale, legendScale, legendColumns, isLatex, query, logScale=False, linewidth=1, legendNameExtension=None):
  #outputDir = outputDir + os.sep + 'query' + str(query)
  #if not os.path.exists(outputDir):
  #  os.makedirs(outputDir)
  queries, numberOfAbortedQueries = Utilities.getQueries(inputFile, dataRowFilters, isLatex, separateAbortedQueries=False, onlyFinishedQueries=False, onlySOJoin=False)
  query = queries[query]
  pattern1 = re.compile(r'\s+')
  pattern = re.compile(r'[^A-Za-z0-9-_]*')
  outputDir = outputDir + os.sep + pattern.sub(r'',pattern1.sub(r'-',str(query)))
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)
  headers, times, percentages = Utilities.getResultOverTimeDataForQuery(inputFile, dataRowFilters, 10, query, isLatex)
  for i in range(0,len(times)):
    if times[i][0] > 0:
      times[i].insert(0,times[i][0])
      times[i].insert(0,0)
      percentages[i].insert(0,0.)
      percentages[i].insert(0,0.)
    times[i] = map(lambda x: x/1000.,times[i])
  
  legendNames = Utilities.getLegendNames(isLatex, headers, legendNameExtension)
  # draw diagram
  DiagramDrawer.drawLineDiagram(outputDir + os.sep + outputFileName, isLatex, "% of Returned Results", 1.5, "Time (in sec)", 1.5, xTickVertical=False, legendNames=legendNames, legendColours=map(lambda x:x["colour"],headers), xValues=times, yValues=percentages, diagramScale=diagramScale, legendScale=legendScale, legendColumns=legendColumns, xLogScale=logScale, linewidth=linewidth)
