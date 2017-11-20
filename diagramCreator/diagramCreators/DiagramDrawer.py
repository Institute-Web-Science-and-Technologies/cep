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

import matplotlib
import latexPlot as latex
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def setLogScale(ax):
  ax.set_yscale('symlog', linthreshy=1e1)
  ymin, ymax = ax.get_ylim()
  if ymin < 0 and ymin >= -15:
    plt.ylim(ymin=-15)
  if ymax > 0:
    if ymax <= 10:
      plt.ylim(ymax=15)
    elif ymax <= 100:
      plt.ylim(ymax=150)
  if ymax <= 1000 and ymin >= -1000:
    sf = ScalarFormatter()
    sf.set_powerlimits((-4,4))
    ax.yaxis.set_major_formatter(sf)

def drawLineDiagram(outputFileName, isLatex, yLabel, yLabelPad, xLabel, xLabelPad, xTickVertical, legendNames, legendColours, xValues, yValues, diagramScale, legendScale, legendColumns, xLogScale=False, linewidth=1):
  fig, ax = plt.subplots()
  if isLatex:
    yLabel = yLabel.replace("_","\\_").replace("#","\\#").replace("%","\\%")
    xLabel = xLabel.replace("_","\\_").replace("#","\\#").replace("%","\\%")
  for i, value in enumerate(xValues):
    plt.plot(xValues[i], yValues[i], label=legendNames[i], color=legendColours[i], linewidth=linewidth)
  if xLogScale:
    ax.set_xscale('symlog', linthreshy=1e1)
    xmin, xmax = ax.get_xlim()
    if xmin < 0 and xmin >= -15:
      plt.xlim(xmin=-15)
    if xmax > 0:
      if xmax <= 10:
        plt.xlim(xmax=15)
      elif xmax <= 100:
        plt.xlim(xmax=150)
    if xmax <= 1000 and xmin >= -1000:
      sf = ScalarFormatter()
      sf.set_powerlimits((-3,3))
      ax.xaxis.set_major_formatter(sf)
  plt.xlabel(xLabel + ("(log-scale)" if xLogScale else ""),labelpad=xLabelPad)
  plt.ylabel(yLabel,labelpad=yLabelPad)
  plt.legend(bbox_to_anchor=legendScale, loc=3, ncol=legendColumns, mode="expand", labelspacing=0, handlelength=1.5, handletextpad=0.2, borderpad=0.2, borderaxespad=0., columnspacing=0.5)
  fig.tight_layout(rect=diagramScale)
  if isLatex:
    latex.savefig(outputFileName)
  else:
    plt.savefig(outputFileName)
  plt.close(fig)

def drawSimpleBarDiagram(outputFileName, isLatex, yLabel, yLabelPad, xLabel, xLabelPad, xTicks, xTickVertical, values, diagramScale, logScale=False):
  fig, ax = plt.subplots()
  n_groups = len(values)
  index = np.arange(n_groups)
  bar_width = 0.8
  coverNames = []
  colours = []
  for rowDescriptor in xTicks:
    if rowDescriptor["numberOfChunks"] == 1:
      coverName = "Centralized"
    else:
      coverName = rowDescriptor["cover"]
      if rowDescriptor["n-hop"] > 0:
        coverName = str(rowDescriptor["n-hop"]) + "HOP_" + coverName
      if isLatex:
        coverName = coverName.replace("_","\\_").replace("#","\\#")
    coverNames.append(coverName)
    colours.append(rowDescriptor["colour"])
  plt.bar(index + 0.1, np.array(values), bar_width, color=colours, log=False, bottom=0, linewidth=0.5)
  plt.xlabel(xLabel,labelpad=xLabelPad)
  plt.xticks(index + 0.5, np.array(coverNames))
  if xTickVertical:
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
  if logScale:
    ax.set_yscale('symlog', linthreshy=1e1)
  if logScale:
    setLogScale(ax)
  if logScale:
    if isLatex:
      yLabel = "\\parbox{200pt}{\centering " + yLabel.replace("_","\\_").replace("#","\\#") + "\\\\(log-scale)}"
    else:
      yLabel = yLabel + "\n(log-scale)"
  plt.ylabel(yLabel,labelpad=yLabelPad)
  fig.tight_layout(rect=diagramScale)
  if isLatex:
    latex.savefig(outputFileName)
  else:
    plt.savefig(outputFileName)
  plt.close(fig)

def drawBarDiagram(outputFileName, isLatex, yLabel, yLabelPad, xLabel, xLabelPad, xTicks, xTickVertical, legendNames, legendColours, values, legendScale, legendColumns, diagramScale, numberOfAbortedQueries=0, titleGap=0.02, logScale=False, perResult=False, relName=None, y2Label="", y2LabelPad=1.5, y2Values=None, y2LegendNames=None, y2LegendColours=None, y2LogScale=False):
  fig, ax = plt.subplots()
  if y2Values is None:
    bar_width = 1/float(len(values)+1)
  else:
    bar_width = 1/float(len(values)+len(y2Values)+1)
  n_groups = len(values[0])
  index = np.arange(n_groups)
  bars = []
  for i, value in enumerate(values):
    bars.append(ax.bar(index + i*bar_width + 0.5*bar_width, np.array(value), bar_width, color=legendColours[i], label=legendNames[i], log=False, bottom=0, linewidth=0.5))
  ax.set_xlabel(xLabel,labelpad=xLabelPad)
  plt.xticks(index + 0.5, np.array(xTicks))
  if xTickVertical:
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
  if logScale:
    setLogScale(ax)
  if numberOfAbortedQueries > 0:
    numberOfFinishedQueries = n_groups-numberOfAbortedQueries;
    plt.axvline(x=index[numberOfFinishedQueries],color="black")
    ymin, ymax = ax.get_ylim()
    plt.text(numberOfFinishedQueries/2-1,ymax+titleGap,'finished')
    plt.text(numberOfFinishedQueries+numberOfAbortedQueries/2-1,ymax+titleGap,'aborted')
  if logScale or perResult or not (relName is None):
    if isLatex:
      yLabel = "\\parbox{200pt}{\centering " + yLabel.replace("_","\\_").replace("#","\\#") + "\\\\(" + ("log-scale" if logScale else "") + (", " if logScale and perResult else "") + ("per Query Result" if perResult else "") + (",\\\\" if (logScale or perResult) and not (relName is None) else "") + ("change to " + relName + " in \\%" if not (relName is None) else "") + ")}"
    else:
      yLabel = yLabel + "\n(" + ("log-scale" if logScale else "") + (", " if logScale and perResult else "") + ("per Query Result" if perResult else "") + (",\n" if (logScale or perResult) and not (relName is None) else "") + ("change to " + relName + " in %" if not (relName is None) else "") + ")"
  ax.set_ylabel(yLabel,labelpad=yLabelPad)
  if not y2Values is None:
    ax2 = ax.twinx()
    for i, value in enumerate(y2Values):
      bars.append(ax2.bar(index + (len(values)+i)*bar_width + 0.5*bar_width, np.array(value), bar_width, color=y2LegendColours[i], label=y2LegendNames[i], log=False, bottom=0, linewidth=0.5))
    if y2LogScale:
      setLogScale(ax2)
      if isLatex:
        y2Label = "\\parbox{200pt}{\centering " + y2Label.replace("_","\\_").replace("#","\\#") + "\\\\(log-scale)}"
      else:
        y2Label = y2Label + "\n(log-scale)"
    ax2.set_ylabel(y2Label,labelpad=y2LabelPad)
  ax.legend(bars, map(lambda x: x.get_label(),bars) ,bbox_to_anchor=legendScale, loc=3, ncol=legendColumns, mode="expand", labelspacing=0, handlelength=1.5, handletextpad=0.2, borderpad=0.2, borderaxespad=0., columnspacing=0.5)
  fig.tight_layout(rect=diagramScale)
  if isLatex:
    latex.savefig(outputFileName)
  else:
    plt.savefig(outputFileName)
  plt.close(fig)