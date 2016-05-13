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
# for each joinnumber create a diagram that
# shows for each query
# the computational effort per cover in a separate bar

# required map: joinNumber -> cover -> query -> measurmentType -> value

selectivitys = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    selectivity = row[7]
    if not selectivity in selectivitys:
      selectivitys[selectivity] = {}
    if not cover in selectivitys[selectivity]:
      selectivitys[selectivity][cover] = {}
    query = ("ss" if row[4]=='SUBJECT_SUBJECT_JOIN' else "so") + " tree=" + ("ll" if row[2]=='LEFT_LINEAR' else ("rl" if row[2]=='RIGHT_LINEAR' else "b")) + " #j=" + row[5] + " #ds=" + row[6]
    selectivitys[selectivity][cover][query] = { "Data Transfer":long(row[8])}

for measurementType in ["Data Transfer"]:
  for selectivity in selectivitys.keys():
    coverSet = list(sorted(selectivitys[selectivity].keys()))
    dataRows = []
    queryGroups = []
    for i, cover in enumerate(coverSet):
      if i == 0:
        queryGroups = list(sorted(selectivitys[selectivity][cover].keys()))
      dataRows.append([])
      for query in queryGroups:
        dataRows[i].append(selectivitys[selectivity][cover][query][measurementType]);
    # create diagramm
    n_groups = len(queryGroups)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 1/float(len(coverSet)+1)
    rects = []
    colorBase = 1 / float(len(coverSet)+1)
    for i, cover in enumerate(coverSet):
      colorValue = "{:f}".format(colorBase*(i+0.5))
      rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[i]), bar_width, color=colorValue, label=cover))
    plt.xlabel("Queries")
    plt.ylabel(measurementType)
    plt.title('Data transfer for selectivity ' + selectivity)
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = fig_size[0]
    plt.legend()
    plt.savefig(outputDir+'/dataTransfer_'+measurementType+'_selectivity-'+selectivity+'_forAll_covers.'+imageType, bbox_inches='tight')

