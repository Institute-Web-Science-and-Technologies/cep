#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import csv

if len(sys.argv) != 4:
  print("You must have the following arguments: <computationalEffort.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

# for totalComputationalEffort, entropy, standard deviation
# for each tree type create a diagram that
# shows for each query
# the computational effort per cover in a separate bar

# required map: treetype -> cover -> query -> measurmentType -> value

treeTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    treeType = row[2]
    if not treeType in treeTypes:
      treeTypes[treeType] = {}
    if not cover in treeTypes[treeType]:
      treeTypes[treeType][cover] = {}
    query = ("ss" if row[4]=='SUBJECT_SUBJECT_JOIN' else "so") + " #j=" + row[5] + " #ds=" + row[6] + " sel=" + row[7]
    treeTypes[treeType][cover][query] = { "Execution Time":long(row[8])}

for measurementType in ["Execution Time"]:
  for treeType in treeTypes.keys():
    coverSet = list(sorted(treeTypes[treeType].keys()))
    dataRows = []
    queryGroups = []
    for i, cover in enumerate(coverSet):
      if i == 0:
        queryGroups = list(sorted(treeTypes[treeType][cover].keys()))
      dataRows.append([])
      for query in queryGroups:
        dataRows[i].append(treeTypes[treeType][cover][query][measurementType]);
    # create diagramm
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 1/float(len(coverSet)+1)
    rects = []
    colorBase = 1 / float(len(coverSet)+1)
    for i, cover in enumerate(coverSet):
      colorValue = "{:f}".format(colorBase*(i+0.5))
      rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[i]), bar_width, color=colorValue, label=cover, log=True, bottom=1))
    plt.xlabel("Queries")
    plt.ylabel(measurementType + " (in msec, log-scale)")
    plt.title('Query execution time for tree type ' + treeType)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    plt.legend()
    plt.savefig(outputDir+'/queryExecution_'+measurementType+'_treeType-'+treeType+'_forAll_covers.'+imageType, bbox_inches='tight')

