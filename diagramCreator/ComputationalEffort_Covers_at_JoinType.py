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
# for each joinType create a diagram that
# shows for each query
# the computational effort per cover in a separate bar

# required map: joinType -> cover -> query -> measurmentType -> value

joinTypes = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    joinType = row[4]
    if not joinType in joinTypes:
      joinTypes[joinType] = {}
    if not cover in joinTypes[joinType]:
      joinTypes[joinType][cover] = {}
    query = "tree=" + ("ll" if row[2]=='LEFT_LINEAR' else ("rl" if row[2]=='RIGHT_LINEAR' else "b")) + " #j=" + row[5] + " #ds=" + row[6] + " sel=" + row[7]
    joinTypes[joinType][cover][query] = { "Total":long(row[8]), "Entropy":float(row[9]), "Standard Deviation":float(row[10])}

for measurementType in ["Total", "Entropy", "Standard Deviation"]:
  for joinType in joinTypes.keys():
    coverSet = list(sorted(joinTypes[joinType].keys()))
    dataRows = []
    queryGroups = []
    for i, cover in enumerate(coverSet):
      if i == 0:
        queryGroups = list(sorted(joinTypes[joinType][cover].keys()))
      dataRows.append([])
      for query in queryGroups:
        dataRows[i].append(joinTypes[joinType][cover][query][measurementType]);
    # create diagramm
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 1/float(len(coverSet)+1)
    rects = []
    colorBase = 1 / float(len(coverSet)+1)
    for i, cover in enumerate(coverSet):
      colorValue = "{:f}".format(colorBase*(i+0.5))
      rects.append(plt.bar(index + i * bar_width, np.array(dataRows[i]), bar_width, color=colorValue, label=cover))
    plt.xlabel("Queries")
    plt.ylabel(measurementType)
    plt.title('Computational effort for join type ' + joinType)
    plt.xticks(index + bar_width, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.legend()
    plt.savefig(outputDir+'/computationalEffort_'+measurementType+'_joinType-'+joinType+'_forAll_covers.'+imageType, bbox_inches='tight')

