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
import DiagramDrawer
import Utilities

def createDiagram(inputFile, dataRowFilters, outputDir, outputFileName, diagramScale, legendScale, legendColumns, isLatex, xTickDescriptor=None, xLabel=None, logScale=False):
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)
  if xTickDescriptor is None:
    xTicks = []
    values = []
    # collect data
    with open(inputFile, 'rb') as f:
      reader = csv.reader(f, delimiter='\t')
      reader.next()
      for row in reader:
        rowDescriptor = Utilities.getFilter(row,dataRowFilters)
        if not rowDescriptor is None:
          xTicks.append(rowDescriptor)
          values.append((float(row[5])+float(row[7]))/1000/60/60)
    # draw diagram
    DiagramDrawer.drawSimpleBarDiagram(outputDir + os.sep + outputFileName,isLatex,"Loading Time (in h)",1.5,"Graph Cover Strategies",1.5,xTicks,True,values,diagramScale,logScale=logScale)
  else:
    xTicks = []
    legendNames = []
    legendColours = []
    values = []
    # collect data
    with open(inputFile, 'rb') as f:
      reader = csv.reader(f, delimiter='\t')
      reader.next()
      for row in reader:
        rowDescriptor = Utilities.getFilter(row,dataRowFilters)
        if not rowDescriptor is None:
          coverName = Utilities.getCoverName(rowDescriptor,isLatex)
          if not coverName in legendNames:
            legendNames.append(coverName)
            legendColours.append(rowDescriptor["colour"])
            values.append([])
          coverIndex = legendNames.index(coverName)
          xTick = str(rowDescriptor[xTickDescriptor])
          if not xTick in xTicks:
            xTicks.append(xTick)
          tickIndex = xTicks.index(xTick)
          while tickIndex >= len(values[coverIndex]):
            values[coverIndex].append(0)
          values[coverIndex][tickIndex] = (float(row[5])+float(row[7]))/1000/60/60
    # draw diagram
    DiagramDrawer.drawBarDiagram(outputDir + os.sep + outputFileName, isLatex, "Loading Time (in h)", 1.5, xLabel, 1.5, xTicks, xTickVertical=False, legendNames=legendNames, legendColours=legendColours, values=values, legendScale=legendScale, legendColumns=legendColumns, diagramScale=diagramScale, logScale=logScale)