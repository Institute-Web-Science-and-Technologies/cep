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

dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'green'})
#dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'green'})
#dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'lime'})
#dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'greenyellow'})
#dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'greenyellow'})

dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'darkblue'})
#dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'darkblue'})
#dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'royalblue'})
#dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'cyan'})
#dataRowSelection.append({"cover":"HIERARCHICAL","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'cyan'})

dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":500000000,"treeType":"BUSHY","colour":'darkred'})
#dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'darkred'})
#dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":1000000000,"treeType":"BUSHY","colour":'red'})
#dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":40,"datasetSize":1000000000,"treeType":"BUSHY","colour":'lightsalmon'})
#dataRowSelection.append({"cover":"MIN_EDGE_CUT","n-hop":0,"numberOfChunks":20,"datasetSize":2000000000,"treeType":"BUSHY","colour":'lightsalmon'})

#dataRowSelection.append({"cover":"VERTICAL","n-hop":0,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'gold'})

#dataRowSelection.append({"cover":"HASH","n-hop":2,"numberOfChunks":10,"datasetSize":1000000000,"treeType":"BUSHY","colour":'purple'})

#dataRowSelection.append({"cover":"HASH","n-hop":0,"numberOfChunks":1,"datasetSize":1000000000,"treeType":"BUSHY","colour":'grey'})

inputDir = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]
isLatex = imageType == 'latex'
outputFileName = '-20Chunks-500M-HHM'
if not isLatex:
  outputFileName = outputFileName + '.' + imageType
  matplotlib.rcParams.update({'font.size': 16})


if isLatex:
  latex.latexify(fig_height=3)
  LoadingTimeDiagram.createDiagram(inputDir + os.sep + 'loadingTime.csv', dataRowSelection, outputDir + os.sep + 'loadingTime', 'loading' + outputFileName,
    diagramScale=(-0.04,-0.04,1.04,1.045), legendScale=(0, 1.15, 1, .102), legendColumns=2, isLatex=isLatex)
  
  latex.latexify(fig_height=2.3)
  ChunkSizesDiagram.createDiagram(inputDir + os.sep + 'chunkSizes.csv', dataRowSelection, outputDir + os.sep + 'chunkSizes', 'chunkSizes' + outputFileName,
    diagramScale= (-0.04,-0.07,1.04,0.89), legendScale= (0, 1.15, 1, .102), legendColumns=2, isLatex=isLatex)
  ChunkSizesDiagram.createDiagram(inputDir + os.sep + 'chunkSizes.csv', dataRowSelection, outputDir + os.sep + 'chunkSizesUnsorted', 'chunkSizesUnsorted' + outputFileName,
    diagramScale= (-0.04,-0.07,1.04,0.89), legendScale= (0, 1.15, 1, .102), legendColumns=2, isLatex=isLatex,
    sort=False)
  
  latex.latexify(fig_height=3.5,scale=1)
  ExecutionTimeDiagram.createDiagram(inputDir + os.sep + 'executionTimelines.csv', dataRowSelection, outputDir + os.sep + 'executionTime', 'executionTime' + outputFileName,
    diagramScale= (-0.05,-0.044,1.04,0.93), legendScale= (-0.4, 1.07, 1.4, .102), legendColumns= 2, isLatex=isLatex,
    titleGap=20, logScale=True, perResult=False)
  ExecutionTimeDiagram.createDiagram(inputDir + os.sep + 'executionTimelines.csv', dataRowSelection, outputDir + os.sep + 'executionTimeRel', 'executionTimeRel' + outputFileName,
    diagramScale= (-0.05,-0.044,1.04,0.975), legendScale= (-0.4, 1.05, 1.4, .102), legendColumns= 2, isLatex=isLatex,
    titleGap=20, logScale=True, perResult=False, relativeValue="cover", relHeader=dataRowSelection[0])
  WorkloadImbalanceDiagram.createDiagram(inputDir + os.sep + 'computationalEffort.csv', dataRowSelection, outputDir + os.sep + 'workloadImbalance', 'workloadImbalance' + outputFileName,
    diagramScale= (-0.05,-0.044,1.04,0.92), legendScale= (-0.48, 1.1, 1.48, .102), legendColumns= 2, isLatex=isLatex,
    titleGap=0.02)
  TotalComputationalEffortDiagram.createDiagram(inputDir + os.sep + 'computationalEffort.csv', dataRowSelection, outputDir + os.sep + 'totalComputationalEffort', 'totalComputationalEffort' + outputFileName,
    diagramScale= (-0.05,-0.044,1.04,0.91), legendScale= (-0.48, 1.12, 1.48, .102), legendColumns= 2, isLatex=isLatex,
    titleGap=100000000, logScale=True)
  TotalComputationalEffortDiagram.createDiagram(inputDir + os.sep + 'computationalEffort.csv', dataRowSelection, outputDir + os.sep + 'totalComputationalEffortPerResult', 'totalComputationalEffortPerResult' + outputFileName,
    diagramScale= (-0.05,-0.044,1.04,0.94), legendScale= (-0.48, 1.12, 1.48, .102), legendColumns= 2, isLatex=isLatex,
    titleGap=3, logScale=False, perResult=True, relativeValue="cover", relHeader=dataRowSelection[0])
  DataTransferDiagram.createDiagram(inputDir + os.sep + 'dataTransfer.csv', dataRowSelection, outputDir + os.sep + 'dataTransfer', 'dataTransfer' + outputFileName,
    diagramScale= (-0.05,-0.044,1.04,0.93), legendScale= (-0.39, 1.07, 1.39, .102), legendColumns= 2, isLatex=isLatex,
    onlySOJoin=True, titleGap=20, logScale=True, perResult=False)
  DataTransferDiagram.createDiagram(inputDir + os.sep + 'dataTransfer.csv', dataRowSelection, outputDir + os.sep + 'dataTransferRel', 'dataTransferRel' + outputFileName,
    diagramScale= (-0.04,-0.044,1.04,0.97), legendScale= (-0.39, 1.05, 1.39, .102), legendColumns= 2, isLatex=isLatex,
    onlySOJoin=True, titleGap=20, logScale=False, perResult=False, relativeValue="cover", relHeader=dataRowSelection[0])
  PackageTransferDiagram.createDiagram(inputDir + os.sep + 'packageTransfer.csv', dataRowSelection, outputDir + os.sep + 'packageTransfer', 'packageTransfer' + outputFileName,
    diagramScale= (-0.05,-0.044,1.04,0.93), legendScale= (-0.39, 1.07, 1.39, .102), legendColumns= 2, isLatex=isLatex,
    onlySOJoin=True, titleGap=20, logScale=True, perResult=False)
  PackageTransferDiagram.createDiagram(inputDir + os.sep + 'packageTransfer.csv', dataRowSelection, outputDir + os.sep + 'packageTransferRel', 'packageTransferRel' + outputFileName,
    diagramScale= (-0.04,-0.044,1.04,0.97), legendScale= (-0.39, 1.05, 1.39, .102), legendColumns= 2, isLatex=isLatex,
    onlySOJoin=True, titleGap=20, logScale=False, perResult=False, relativeValue="cover", relHeader=dataRowSelection[0])
  
  latex.latexify(fig_height=1.95,fig_width=2.1,scale=1)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=0, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=1, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=2, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=3, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=4, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=6, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=7, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=8, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=9, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=10, logScale=False)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.065,-0.075,1.065,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=11, logScale=False)
  latex.latexify(fig_height=1.95,fig_width=3,scale=1)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.05,-0.075,1.05,0.86), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=5, logScale=False)
  
else:
  LoadingTimeDiagram.createDiagram(inputDir + os.sep + 'loadingTime.csv', dataRowSelection, outputDir + os.sep + 'loadingTime', 'loading' + outputFileName,
    diagramScale=(0.0,0,1.0,1.), legendScale=(0, 1.1, 1, .102), legendColumns=2, isLatex=isLatex)
  ChunkSizesDiagram.createDiagram(inputDir + os.sep + 'chunkSizes.csv', dataRowSelection, outputDir + os.sep + 'chunkSizes', 'chunkSizes' + outputFileName,
    diagramScale= (0.01,0,1.0,0.82), legendScale= (0, 1.1, 1, .102), legendColumns= 2, isLatex=isLatex)
  ChunkSizesDiagram.createDiagram(inputDir + os.sep + 'chunkSizes.csv', dataRowSelection, outputDir + os.sep + 'chunkSizesUnsorted', 'chunkSizesUnsorted' + outputFileName,
    diagramScale= (0.01,0,1.0,0.82), legendScale= (0, 1.1, 1, .102), legendColumns= 2, isLatex=isLatex,
    sort=False)
  
  matplotlib.rcParams.update({'figure.figsize': (10, 9)})
  ExecutionTimeDiagram.createDiagram(inputDir + os.sep + 'executionTimelines.csv', dataRowSelection, outputDir + os.sep + 'executionTime', 'executionTime' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.2, 1.04, 1.2, .102), legendColumns= 2, isLatex=isLatex,
    titleGap=20, logScale=True, perResult=False)
  ExecutionTimeDiagram.createDiagram(inputDir + os.sep + 'executionTimelines.csv', dataRowSelection, outputDir + os.sep + 'executionTimeRel', 'executionTimeRel' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.2, 1.1, 1.2, .102), legendColumns = 3, isLatex=isLatex,
    titleGap=20, logScale=True, perResult=False, relativeValue="cover", relHeader=dataRowSelection[0])
  WorkloadImbalanceDiagram.createDiagram(inputDir + os.sep + 'computationalEffort.csv', dataRowSelection, outputDir + os.sep + 'workloadImbalance', 'workloadImbalance' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.3, 1.1, 1.3, .102), legendColumns= 2, isLatex=isLatex,
    titleGap=0.02)
  TotalComputationalEffortDiagram.createDiagram(inputDir + os.sep + 'computationalEffort.csv', dataRowSelection, outputDir + os.sep + 'totalComputationalEffort', 'totalComputationalEffort' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.3, 1.1, 1.3, .102), legendColumns= 2, isLatex=isLatex,
    titleGap=100000000, logScale=True)
  TotalComputationalEffortDiagram.createDiagram(inputDir + os.sep + 'computationalEffort.csv', dataRowSelection, outputDir + os.sep + 'totalComputationalEffortPerResult', 'totalComputationalEffortPerResult' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.3, 1.1, 1.3, .102), legendColumns= 3, isLatex=isLatex,
    titleGap=3, logScale=False, perResult=False, relativeValue="cover", relHeader=dataRowSelection[0])
  DataTransferDiagram.createDiagram(inputDir + os.sep + 'dataTransfer.csv', dataRowSelection, outputDir + os.sep + 'dataTransfer', 'dataTransfer' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.2, 1.04, 1.2, .102), legendColumns= 3, isLatex=isLatex,
    onlySOJoin=True, titleGap=20, logScale=True, perResult=False)
  DataTransferDiagram.createDiagram(inputDir + os.sep + 'dataTransfer.csv', dataRowSelection, outputDir + os.sep + 'dataTransferRel', 'dataTransferRel' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.2, 1.1, 1.2, .102), legendColumns= 3, isLatex=isLatex,
    onlySOJoin=True, titleGap=20, logScale=False, perResult=False, relativeValue="cover", relHeader=dataRowSelection[0])
  PackageTransferDiagram.createDiagram(inputDir + os.sep + 'packageTransfer.csv', dataRowSelection, outputDir + os.sep + 'packageTransfer', 'packageTransfer' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.2, 1.04, 1.2, .102), legendColumns= 3, isLatex=isLatex,
    onlySOJoin=True, titleGap=20, logScale=True, perResult=False)
  PackageTransferDiagram.createDiagram(inputDir + os.sep + 'packageTransfer.csv', dataRowSelection, outputDir + os.sep + 'packageTransferRel', 'packageTransferRel' + outputFileName,
    diagramScale= (0.01,0,1.0,0.9), legendScale= (-0.2, 1.1, 1.2, .102), legendColumns= 3, isLatex=isLatex,
    onlySOJoin=True, titleGap=20, logScale=False, perResult=False, relativeValue="cover", relHeader=dataRowSelection[0])

  matplotlib.rcParams.update({'figure.figsize': (5, 5)})
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=0, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=1, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=2, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=3, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=4, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=6, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=7, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=8, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=9, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=10, logScale=False, linewidth=5)
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.04,-0.05,1.04,0.795), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=11, logScale=False, linewidth=5)
  matplotlib.rcParams.update({'figure.figsize': (6, 5)})
  ResultsOverTimeDiagram.createDiagram(inputDir + os.sep + 'plainResultsOverTime.csv', dataRowSelection, outputDir + os.sep + 'resultsOverTime', 'resultsOverTime' + outputFileName, diagramScale=(-0.03,-0.05,1.03,0.775), legendScale=(0, 1.02, 1, 0), legendColumns=1, isLatex=isLatex, query=5, logScale=False, linewidth=5)
