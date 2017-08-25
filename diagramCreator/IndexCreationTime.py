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

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import sys
import csv
import latexPlot as latex

if len(sys.argv) != 3:
  print("You must have the following arguments: <outputDir> <imageType>")
  sys.exit()

outputDir = sys.argv[1]
imageType = sys.argv[2]

if not os.path.exists(outputDir):
  os.makedirs(outputDir)

localIndexCreationTimes = {
  '\\textbf{slave 1 on server 6}': 1502971/1000/60,
  'slave 2 on server 3': 3645760/1000/60,
  'slave 3 on server 3': 1661639/1000/60,
  'slave 4 on server 5': 4636441/1000/60,
  'slave 5 on server 3': 4586060/1000/60,
  'slave 6 on server 3': 1698421/1000/60,
  'slave 7 on server 3': 3665011/1000/60,
  'slave 8 on server 3': 4728304/1000/60,
  'slave 9 on server 1': 1528794/1000/60,
  'slave 10 on server 3': 1681686/1000/60,
  'slave 11 on server 1': 1460679/1000/60,
  'slave 12 on server 1': 1563361/1000/60,
  'slave 13 on server 1': 1484758/1000/60,
  'slave 14 on server 3': 2444632/1000/60,
  'slave 15 on server 3': 1558751/1000/60,
  'slave 16 on server 1': 1572279/1000/60,
  'slave 17 on server 2': 1615377/1000/60,
  'slave 18 on server 5': 1853810/1000/60,
  'slave 19 on server 5': 2283221/1000/60,
  'slave 20 on server 6': 1610719/1000/60,
  'slave 21 on server 6': 1586159/1000/60,
  'slave 22 on server 3': 1695991/1000/60,
  'slave 23 on server 6': 1514264/1000/60,
  'slave 24 on server 3': 4265240/1000/60,
  'slave 25 on server 4': 14000290/1000/60,
  'slave 26 on server 6': 1426921/1000/60,
  'slave 27 on server 3': 2111980/1000/60,
  'slave 28 on server 4': 69672186/1000/60,
  'slave 29 on server 6': 1524873/1000/60,
  'slave 30 on server 3': 3357094/1000/60,
  'slave 31 on server 4': 30259380/1000/60,
  'slave 32 on server 6': 1454096/1000/60,
  'slave 33 on server 3': 1861643/1000/60,
  'slave 34 on server 4': 45608596/1000/60,
  'slave 35 on server 6': 1577999/1000/60,
  'slave 36 on server 4': 70780648/1000/60,
  'slave 37 on server 5': 1718528/1000/60,
  'slave 38 on server 2': 1684956/1000/60,
  'slave 39 on server 3': 3507392/1000/60,
  'slave 40 on server 1': 1629560/1000/60,
  }

times = [];
slaves = [];

for slave, time in sorted(localIndexCreationTimes.items(), key=lambda x: x[1], reverse=True):
  slaves.append(slave)
  times.append(time)

if imageType=="latex":
  latex.latexify(fig_height=3)

N = len(times)
fig, ax = plt.subplots()
ind = np.arange(N)
width = 0.5

plt.bar(ind, times, width, color='grey')
plt.ylabel('\parbox{253pt}{\centering Local Index Creation\\\\Time (in min)}')
plt.yticks(np.arange(0, times[0]+1, 120.0))
plt.xticks(ind + width/2., slaves, rotation=90)
plt.axis('tight')
if imageType=="latex":
  fig.tight_layout(rect=(-0.018,-0.03,1.02,1.03))

if imageType=="latex":
  latex.savefig(outputDir,'indexCreationTimes')
else:
  plt.savefig(outputDir+'/indexCreationTimes.'+imageType, bbox_inches='tight')
