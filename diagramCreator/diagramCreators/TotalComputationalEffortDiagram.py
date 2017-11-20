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

def createDiagram(inputFile, dataRowFilters, outputDir, outputFileName, diagramScale, legendScale, legendColumns, isLatex, onlyFinishedQueries=False, separateAbortedQueries=True, titleGap=0.02, logScale=False, perResult=False, relativeValue=None, relHeader=None, legendNameExtension=None):
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)
  queries, numberOfAbortedQueries = Utilities.getQueries(inputFile, dataRowFilters, isLatex, separateAbortedQueries, onlyFinishedQueries)
  if perResult:
    headers, values = Utilities.getDataForQueriesPerResult(inputFile, dataRowFilters, 10, queries, isLatex)
  else:
    headers, values = Utilities.getDataForQueries(inputFile, dataRowFilters, 10, queries, isLatex)
  
  if relativeValue is None:
    legendNames = Utilities.getLegendNames(isLatex, headers, legendNameExtension)
    # draw diagram
    if separateAbortedQueries:
      DiagramDrawer.drawBarDiagram(outputDir + os.sep + outputFileName,isLatex,"Total Computational Effort",1.5,"Queries",1.5,queries,True,legendNames,map(lambda x:x["colour"],headers),values,legendScale,legendColumns,diagramScale,numberOfAbortedQueries,titleGap,logScale=logScale,perResult=perResult)
    else:
      DiagramDrawer.drawBarDiagram(outputDir + os.sep + outputFileName,isLatex,"Total Computational Effort",1.5,"Queries",1.5,queries,True,legendNames,map(lambda x:x["colour"],headers),values,legendScale,legendColumns,diagramScale,titleGap=titleGap,logScale=logScale,perResult=perResult)
  else:
    newHeaders, newValues = Utilities.getRelativeDataForQueries(headers, values, relHeader)
    legendNames = Utilities.getLegendNames(isLatex, newHeaders, legendNameExtension)
    # draw diagram
    fileSuffix = str(relHeader[relativeValue])
    if relativeValue == "cover":
       if relHeader["n-hop"] > 0:
         fileSuffix = str(relHeader["n-hop"]) + "HOP_" + fileSuffix
    fileSuffix = "-RelTo" + fileSuffix
    oFileName = Utilities.extendFileName(outputFileName,fileSuffix,isLatex)
    if separateAbortedQueries:
      DiagramDrawer.drawBarDiagram(outputDir + os.sep + oFileName,isLatex,"Total Computational Effort",1.5,"Queries",1.5,queries,True,legendNames,map(lambda x:x["colour"],newHeaders),newValues,legendScale,legendColumns,diagramScale,numberOfAbortedQueries,titleGap,logScale=logScale,perResult=perResult, relName=Utilities.getLegendName(isLatex,relHeader,legendNameExtension))
    else:
      DiagramDrawer.drawBarDiagram(outputDir + os.sep + outputFileName,isLatex,"Total Computational Effort",1.5,"Queries",1.5,queries,True,legendNames,map(lambda x:x["colour"],newHeaders),newValues,legendScale,legendColumns,diagramScale,titleGap=titleGap,logScale=logScale,perResult=perResult,relName=Utilities.getLegendName(isLatex,relHeader,legendNameExtension))