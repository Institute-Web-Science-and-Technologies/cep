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
import diagramCreators.ChunkSizesMatchDiagram as ChunkSizesMatchDiagram

if len(sys.argv) != 4:
  print("You must have the following arguments: <inputDir> <outputDir> <imageType>")
  sys.exit()

inputDir = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]
isLatex = imageType == 'latex'
outputFileName = ''
if not isLatex:
  outputFileName = outputFileName + '.' + imageType
  matplotlib.rcParams.update({'font.size': 16})

if isLatex:
  latex.latexify(fig_height=1.5,scale=2)
  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'green'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'darkblue'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'darkred'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"VERTICAL","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'gold'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HASH","n-hop":2,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'purple'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  #dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":1,"datasetSize":1000000000,"treeType":"BUSHY","colour":'grey'}

  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'green'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'lime'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'greenyellow'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'darkblue'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'royalblue'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'cyan'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'darkred'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'red'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'lightsalmon'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.02,-0.05,1.02,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  
  latex.latexify(fig_height=0.75,scale=4)
  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'greenyellow'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.05,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'cyan'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.05,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'lightsalmon'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.05,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
else:
  matplotlib.rcParams.update({'figure.figsize': (15, 9)})
  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'green'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'darkblue'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'darkred'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"VERTICAL","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'gold'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HASH","n-hop":2,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'purple'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  #dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":1,"datasetSize":1000000000,"treeType":"BUSHY","colour":'grey'}

  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'green'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'lime'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'greenyellow'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'darkblue'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'royalblue'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'cyan'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'darkred'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'red'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'lightsalmon'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  
  matplotlib.rcParams.update({'figure.figsize': (20, 9)})
  dataRowFilter={"cover":"HASH","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'greenyellow'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'cyan'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)
  dataRowFilter={"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'lightsalmon'}
  ChunkSizesMatchDiagram.createDiagram(None,inputDir + os.sep + 'operationOutput.csv', dataRowFilter, outputDir + os.sep + 'matchesPerChunk', 'matchesPerChunk' + outputFileName,
    diagramScale= (-0.01,-0.03,1.01,0.87), legendScale= (0, 1.01, 1, .102), legendColumns=2, isLatex=isLatex, logScale=True)