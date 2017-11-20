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

def createDiagram(inputFile, dataRowFilter, outputDir, outputFileName, diagramScale, legendScale, legendColumns, isLatex, sort=True):
  if not os.path.exists(outputDir):
    os.makedirs(outputDir)
  headers = []
  values = []
  # collect data
  with open(inputFile, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
      rowDescriptor = Utilities.getFilter(row,dataRowFilter)
      if not rowDescriptor is None:
        headers.append(rowDescriptor)
        if sort:
          values.append(sorted(map(long,row[4:]),reverse=True))
        else:
          values.append(map(long,row[4:]))
  # draw diagram
  DiagramDrawer.drawBarDiagram(outputDir + os.sep + outputFileName,isLatex,"Number of Triples",1.5,"Chunks",1.5,list(range(1,len(values[0])+1)),False,map(lambda x:Utilities.getCoverName(x,isLatex),headers),map(lambda x:x["colour"],headers),values,legendScale,legendColumns,diagramScale)