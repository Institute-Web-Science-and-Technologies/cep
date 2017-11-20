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

def createDiagram(inputFile, dataRowFilters, outputDir, outputFileName, diagramScale, legendScale, legendColumns, isLatex, separateAbortedQueries=True, titleGap=0.02, logScale=False, legendNameExtension=None):
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)
  queries, numberOfAbortedQueries = Utilities.getQueries(inputFile, dataRowFilters, isLatex, separateAbortedQueries=True)
  headers, values = Utilities.getDataForQueries(inputFile, dataRowFilters, 13, queries, isLatex)
  legendNames = Utilities.getLegendNames(isLatex, headers, legendNameExtension)
        
  # draw diagram
  if separateAbortedQueries:
    DiagramDrawer.drawBarDiagram(outputDir + os.sep + outputFileName,isLatex,"Workload Imbalance",1.5,"Queries",1.5,queries,True,legendNames,map(lambda x:x["colour"],headers),values,legendScale,legendColumns,diagramScale,numberOfAbortedQueries,logScale=logScale)
  else:
    DiagramDrawer.drawBarDiagram(outputDir + os.sep + outputFileName,isLatex,"Workload Imbalance",1.5,"Queries",1.5,queries,True,legendNames,map(lambda x:x["colour"],headers),values,legendScale,legendColumns,diagramScale,logScale=logScale)