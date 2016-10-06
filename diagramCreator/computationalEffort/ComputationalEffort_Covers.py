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
# shows for each query
# the computational effort per cover in a separate bar

# required map: cover -> query -> measurmentType -> value

covers = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    if not cover in covers:
      covers[cover] = {}
    query = ("ss" if row[4]=='SUBJECT_SUBJECT_JOIN' else "so") + " tree=" + ("ll" if row[2]=='LEFT_LINEAR' else ("rl" if row[2]=='RIGHT_LINEAR' else "b")) + " #j=" + row[5] + " #ds=" + row[6] + " sel=" + row[7]
    covers[cover][query] = { "Total":long(row[8]), "Entropy":float(row[9]), "Standard Deviation":float(row[10])}

for measurementType in ["Total", "Entropy", "Standard Deviation"]:
  coverSet = list(sorted(covers.keys()))
  dataRows = []
  queryGroups = []
  for i, cover in enumerate(coverSet):
    if i == 0:
      queryGroups = list(sorted(covers[cover].keys()))
    dataRows.append([])
    for query in queryGroups:
      dataRows[i].append(covers[cover][query][measurementType]);
  # create diagramm
  n_groups = len(queryGroups)
  fig, ax = plt.subplots()
  index = np.arange(n_groups)
  bar_width = 1/float(len(coverSet)+1)
  rects = []
  colorBase = 1 / float(len(coverSet)+1)
  for i, cover in enumerate(coverSet):
    colorValue = "{:f}".format(colorBase*(i+0.5))
    if measurementType == "Entropy":
      rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[i]), bar_width, color=colorValue, label=cover))
    else:
      rects.append(plt.bar(index + i * bar_width + 0.5*bar_width, np.array(dataRows[i]), bar_width, color=colorValue, label=cover, log=True, bottom=1))
  plt.xlabel("Queries")
  if measurementType == "Entropy":
    plt.ylabel(measurementType)
  else:
    plt.ylabel(measurementType + " (log-scale)")
  plt.xticks(index + 0.5, np.array(queryGroups))
  plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
  plt.axis('tight')
  fig_size = plt.rcParams["figure.figsize"]
  fig_size[0] = fig_size[0]
  fig_size[1] = fig_size[1]
  plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
  plt.savefig(outputDir+'/computationalEffort_'+measurementType+'.'+imageType, bbox_inches='tight')

