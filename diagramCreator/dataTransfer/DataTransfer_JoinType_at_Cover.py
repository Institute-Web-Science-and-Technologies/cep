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
# for each cover create a diagram that
# shows for each query
# the computational effort per tree type in a separate bar

# required map: treetype -> cover -> query -> measurmentType -> value

coverTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    joinType = row[4]
    if not cover in coverTypes:
      coverTypes[cover] = {}
    if not joinType in coverTypes[cover]:
      coverTypes[cover][joinType] = {}
    query = "tree=" + ("ll" if row[2]=='LEFT_LINEAR' else ("rl" if row[2]=='RIGHT_LINEAR' else "b")) + " #j=" + row[5] + " #ds=" + row[6] + " sel=" + row[7]
    coverTypes[cover][joinType][query] = { "Data Transfer":long(row[8])}

for measurementType in ["Data Transfer"]:
  for cover in coverTypes.keys():
    joinTypeSet = list(sorted(coverTypes[cover].keys()))
    dataRows = []
    queryGroups = []
    for i, joinType in enumerate(joinTypeSet):
      if i == 0:
        queryGroups = list(sorted(coverTypes[cover][joinType].keys()))
      dataRows.append([])
      for query in queryGroups:
        dataRows[i].append(coverTypes[cover][joinType][query][measurementType]);
    # create diagramm
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 1/float(len(joinTypeSet)+1)
    rects = []
    colorBase = 1 / float(len(joinTypeSet)+1)
    for i, joinType in enumerate(joinTypeSet):
      colorValue = "{:f}".format(colorBase*(i+0.5))
      rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[i]), bar_width, color=colorValue, label=joinType))
    plt.xlabel("Queries")
    plt.ylabel(measurementType)
    plt.title('Data transfer for graph cover ' + cover)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    plt.legend()
    plt.savefig(outputDir+'/dataTransfer_'+measurementType+'_cover-'+cover+'_forAll_joinTypes.'+imageType, bbox_inches='tight')

