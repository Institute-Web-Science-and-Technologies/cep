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
    selectivity = row[7]
    if not cover in coverTypes:
      coverTypes[cover] = {}
    if not selectivity in coverTypes[cover]:
      coverTypes[cover][selectivity] = {}
    query = ("ss" if row[4]=='SUBJECT_SUBJECT_JOIN' else "so") + " tree=" + ("ll" if row[2]=='LEFT_LINEAR' else ("rl" if row[2]=='RIGHT_LINEAR' else "b")) + " #j=" + row[5] + " #ds=" + row[6]
    coverTypes[cover][selectivity][query] = { "Total":long(row[8]), "Entropy":float(row[9]), "Standard Deviation":float(row[10])}

for measurementType in ["Total", "Entropy", "Standard Deviation"]:
  for cover in coverTypes.keys():
    selectivitySet = list(sorted(coverTypes[cover].keys()))
    dataRows = []
    queryGroups = []
    for i, selectivity in enumerate(selectivitySet):
      if i == 0:
        queryGroups = list(sorted(coverTypes[cover][selectivity].keys()))
      dataRows.append([])
      for query in queryGroups:
        dataRows[i].append(coverTypes[cover][selectivity][query][measurementType]);
    # create diagramm
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 1/float(len(selectivitySet)+1)
    rects = []
    colorBase = 1 / float(len(selectivitySet)+1)
    for i, selectivity in enumerate(selectivitySet):
      colorValue = "{:f}".format(colorBase*(i+0.5))
      rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[i]), bar_width, color=colorValue, label='selectivity ' + selectivity))
    plt.xlabel("Queries")
    plt.ylabel(measurementType)
    plt.title('Computational effort for graph cover ' + cover)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    plt.legend()
    plt.savefig(outputDir+'/computationalEffort_'+measurementType+'_cover-'+cover+'_forAll_selectivitys.'+imageType, bbox_inches='tight')

