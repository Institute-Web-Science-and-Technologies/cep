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
import matplotlib
import diagramCreators.latexPlot as latex
import diagramCreators.LoadingTimeDiagram as LoadingTimeDiagram
import diagramCreators.ChunkSizesDiagram as ChunkSizesDiagram
import diagramCreators.ExecutionTimeDiagram as ExecutionTimeDiagram
import diagramCreators.WorkloadImbalanceDiagram as WorkloadImbalanceDiagram
import diagramCreators.TotalComputationalEffortDiagram as TotalComputationalEffortDiagram
import diagramCreators.DataTransferDiagram as DataTransferDiagram
import diagramCreators.PackageTransferDiagram as PackageTransferDiagram
import diagramCreators.ResultsOverTimeDiagram as ResultsOverTimeDiagram

if len(sys.argv) != 4:
  print("You must have the following arguments: <inputDir> <outputDir> <imageType>")
  sys.exit()

# for colour names see https://matplotlib.org/examples/color/named_colors.html
dataRowSelection = list()

#dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'green'})
dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'green'})
dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'lime'})
dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'greenyellow'})
#dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'greenyellow'})

#dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'darkblue'})
dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'darkblue'})
dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'royalblue'})
dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'cyan'})
#dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'cyan'})

#dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'darkred'})
dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'darkred'})
dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'red'})
dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'lightsalmon'})
#dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'lightsalmon'})

#dataRowSelection.append({"cover":"VERTICAL","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'gold'})

#dataRowSelection.append({"cover":"HASH","n-hop":2,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'purple'})

#dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":1,"datasetSize":1000000000,"treeType":"BUSHY","colour":'grey'})

inputDir = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]
isLatex = imageType == 'latex'
outputFileName = '-102040Chunks-HHM'
if not isLatex:
  outputFileName = outputFileName + '.' + imageType
  matplotlib.rcParams.update({'font.size': 16})


if isLatex:
  latex.latexify(fig_height=1.7)
  LoadingTimeDiagram.createDiagram(inputDir + os.sep + 'loadingTime.csv', dataRowSelection, outputDir + os.sep + 'loadingTime', 'loading' + outputFileName,
    diagramScale=(-0.04,-0.08,1.04,0.93), legendScale=(0, 1.02, 1, .102), legendColumns=2, isLatex=isLatex, xTickDescriptor="numberOfChunks", xLabel="Number of Graph Chunks")
else:
  LoadingTimeDiagram.createDiagram(inputDir + os.sep + 'loadingTime.csv', dataRowSelection, outputDir + os.sep + 'loadingTime', 'loading' + outputFileName,
    diagramScale=(0.0,0,1.0,0.9), legendScale=(0, 1.02, 1, .102), legendColumns=2, isLatex=isLatex, xTickDescriptor="numberOfChunks", xLabel="Number of Graph Chunks")