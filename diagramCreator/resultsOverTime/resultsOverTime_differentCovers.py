#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import csv
from itertools import cycle

if len(sys.argv) != 4:
  print("You must have the following arguments: <computationalEffort.csv> <outputDir> <imageType>")
  sys.exit()

inputFile = sys.argv[1]
outputDir = sys.argv[2]
imageType = sys.argv[3]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

queries = {}

with open(inputFile, 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  reader.next()
  for row in reader:
    cover = ""
    if int(row[1]) != 0:
      cover += row[1] + "HOP_"
    cover += row[0]
    query = ("ss" if row[4]=='SUBJECT_SUBJECT_JOIN' else "so") + " tree=" + ("ll" if row[2]=='LEFT_LINEAR' else ("rl" if row[2]=='RIGHT_LINEAR' else "b")) + " #j=" + row[5] + " #ds=" + row[6] + " sel=" + row[7]
    row2 = reader.next();
    row = row[8:len(row)]
    row_time = []
    row_time.append(0)
    for time in row:
      row_time.append(long(time)-1)
      row_time.append(long(time))
    row2 = row2[8:len(row2)]
    row_percent = []
    row_percent.append(0)
    previous = 0
    for percent in row2:
      row_percent.append(previous)
      previous = float(percent)
      row_percent.append(previous)
    if not query in queries.keys():
      queries[query] = {}
    queries[query][cover] = { 'time':row_time, 'percent':row_percent}

lines = ["-","--","-.",":"]

for query in sorted(queries.keys()):
  # create diagram
  fig, ax = plt.subplots()
  coverSet = sorted(queries[query].keys())
  colorBase = 1 / float(len(coverSet)+1)
  linecycler = cycle(lines)
  for i, cover in enumerate(coverSet):
    colorValue = "{:f}".format(colorBase*(i+0.5))
    plt.plot(queries[query][cover]['time'], queries[query][cover]['percent'], label=cover, color=colorValue, linestyle=next(linecycler))
  plt.title(query)
  plt.xlabel("Time (in msec)")
  plt.ylabel("Percentage of returned results")
  plt.axis('tight')
  plt.legend(loc='upper left', ncol=len(sorted(queries[query].keys())), bbox_to_anchor=(0., -0.2, 1., .102))
  plt.savefig(outputDir+'/resultsOverTime_'+query+'.'+imageType, bbox_inches='tight')
  plt.close(fig)

