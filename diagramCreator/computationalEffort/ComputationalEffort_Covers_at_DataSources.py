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

dataSources = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    dataSource = row[6]
    if not dataSource in dataSources:
      dataSources[dataSource] = {}
    if not cover in dataSources[dataSource]:
      dataSources[dataSource][cover] = {}
    query = ("ss" if row[4]=='SUBJECT_SUBJECT_JOIN' else "so") + " tree=" + ("ll" if row[2]=='LEFT_LINEAR' else ("rl" if row[2]=='RIGHT_LINEAR' else "b")) + " #j=" + row[5] + " sel=" + row[7]
    dataSources[dataSource][cover][query] = { "Total":long(row[8]), "Entropy":float(row[9]), "Standard Deviation":float(row[10])}

for measurementType in ["Total", "Entropy", "Standard Deviation"]:
  for dataSource in dataSources.keys():
    coverSet = list(sorted(dataSources[dataSource].keys()))
    dataRows = []
    queryGroups = []
    for i, cover in enumerate(coverSet):
      if i == 0:
        queryGroups = list(sorted(dataSources[dataSource][cover].keys()))
      dataRows.append([])
      for query in queryGroups:
        dataRows[i].append(dataSources[dataSource][cover][query][measurementType]);
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
    plt.title('Computational effort for ' + dataSource + ' data source' + ( "" if int(dataSource) == 1 else "s"))
    plt.xticks(index + 0.5, np.array(queryGroups))
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.axis('tight')
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = fig_size[0]
    plt.legend()
    plt.savefig(outputDir+'/computationalEffort_'+measurementType+'_dataSource-'+dataSource+'_forAll_covers.'+imageType, bbox_inches='tight')

