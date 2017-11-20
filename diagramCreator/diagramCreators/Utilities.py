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

import csv

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def isMatch(row, rowFilter):
  return rowFilter["cover"] == row[0] and rowFilter["n-hop"] == int(row[3]) and rowFilter["numberOfChunks"] == int(row[1]) and rowFilter["datasetSize"] == int(row[2]) and ((isNumber(row[4])) or (rowFilter["treeType"] == row[4]))

def getFilter(row, dataRowFilters):
  for rowFilter in dataRowFilters:
    if isMatch(row, rowFilter):
      return rowFilter
  return None

def extendFileName(outputFileName, fileSuffix, isLatex):
  if isLatex:
    oFileName = outputFileName + fileSuffix
  else:
    fileParts = outputFileName.rsplit(".",1)
    oFileName = fileParts[0] + fileSuffix + "." + fileParts[1]
  return oFileName

def getCoverName(rowFilter, isLatex):
  if rowFilter["numberOfChunks"] == 1:
    coverName = "Centralized"
  else:
    coverName = rowFilter["cover"]
    if rowFilter["n-hop"] > 0:
      coverName = str(rowFilter["n-hop"]) + "HOP_" + coverName
    if isLatex:
      coverName = coverName.replace("_","\\_").replace("#","\\#")
  return coverName
  
def getChunkNumber(header,isLatex):
  if isLatex:
    return str(header["numberOfChunks"]).replace("_","\\_").replace("#","\\#") + " slaves"
  else:
    return str(header["numberOfChunks"]) + " slaves"
  
def getDatasetSize(header,isLatex):
  if isLatex:
    return str(long(header["datasetSize"])/1000000).replace("_","\\_").replace("#","\\#") + "M triples"
  else:
    return str(long(header["datasetSize"])/1000000) + "M triples"
  
def getTreeType(header,isLatex):
  if isLatex:
    return str(header["treeType"]).replace("_","\\_").replace("#","\\#").lower()
  else:
    return str(header["treeType"]).lower()

def getLegendNames(isLatex, headers, legendNameExtension):
  return map(lambda x:getLegendName(isLatex, x, legendNameExtension),headers)

def getLegendName(isLatex, header, legendNameExtension):
  legendName = getCoverName(header,isLatex)
  if not legendNameExtension is None:
    if legendNameExtension == "numberOfChunks":
      legendName = legendName + " " + getChunkNumber(header,isLatex)
    elif legendNameExtension == "datasetSize":
      legendName = legendName + " " + getDatasetSize(header,isLatex)
    elif legendNameExtension == "treeType":
      legendName = legendName + " " + getTreeType(header,isLatex)
  return legendName

def getQuery(isLatex, row):
  return getQueryName(isLatex,row[6],row[7],row[8],row[9])

def getQueryName(isLatex, joinPattern, numberOfJoins, numberOfDataSources, selectivity):
  return ("so" if joinPattern=="SUBJECT_OBJECT_JOIN" else "ss") + " " + ("\\#" if isLatex else "#") + "tp=" + str(int(numberOfJoins)+1) + " " + ("\\#" if isLatex else "#") + "ds=" + numberOfDataSources + " sel=" + selectivity

def getNumberOfResults(query, nHop, datasetSize):
  query = query.replace("\\","");
  if nHop==0:
    if datasetSize==500000000:
      if query=="so #tp=2 #ds=1 sel=0.001":
        return 855;
      elif query=="so #tp=2 #ds=1 sel=0.01":
        return 86093;
      elif query=="so #tp=8 #ds=1 sel=0.001":
        return 5903;
      elif query=="so #tp=8 #ds=1 sel=0.01":
        return 241;
      elif query=="so #tp=8 #ds=3 sel=0.001":
        return 1000000;
      elif query=="so #tp=8 #ds=3 sel=0.01":
        return 327984;
      elif query=="ss #tp=2 #ds=1 sel=0.001":
        return 1000000;
      elif query=="ss #tp=2 #ds=1 sel=0.01":
        return 65081;
      elif query=="ss #tp=8 #ds=1 sel=0.001":
        return 1000000;
      elif query=="ss #tp=8 #ds=1 sel=0.01":
        return 1000000;
      elif query=="ss #tp=8 #ds=3 sel=0.001":
        return 1000000;
      elif query=="ss #tp=8 #ds=3 sel=0.01":
        return 4;
    elif datasetSize==1000000000:
      if query=="so #tp=2 #ds=1 sel=0.001":
        return 1262;
      elif query=="so #tp=2 #ds=1 sel=0.01":
        return 127169;
      elif query=="so #tp=8 #ds=1 sel=0.001":
        return 61358;
      elif query=="so #tp=8 #ds=1 sel=0.01":
        return 1365;
      elif query=="so #tp=8 #ds=3 sel=0.001":
        return 1000000;
      elif query=="so #tp=8 #ds=3 sel=0.01":
        return 754495;
      elif query=="ss #tp=2 #ds=1 sel=0.001":
        return 1000000;
      elif query=="ss #tp=2 #ds=1 sel=0.01":
        return 104776;
      elif query=="ss #tp=8 #ds=1 sel=0.001":
        return 1000000;
      elif query=="ss #tp=8 #ds=1 sel=0.01":
        return 1000000;
      elif query=="ss #tp=8 #ds=3 sel=0.001":
        return 1000000;
      elif query=="ss #tp=8 #ds=3 sel=0.01":
        return 12;
    elif datasetSize==2000000000:
      if query=="so #tp=2 #ds=1 sel=0.001":
        return 2961;
      elif query=="so #tp=2 #ds=1 sel=0.01":
        return 173281;
      elif query=="so #tp=8 #ds=1 sel=0.001":
        return 596701;
      elif query=="so #tp=8 #ds=1 sel=0.01":
        return 144115;
      elif query=="so #tp=8 #ds=3 sel=0.001":
        return 1000000;
      elif query=="so #tp=8 #ds=3 sel=0.01":
        return 1000000;
      elif query=="ss #tp=2 #ds=1 sel=0.001":
        return 1000000;
      elif query=="ss #tp=2 #ds=1 sel=0.01":
        return 148389;
      elif query=="ss #tp=8 #ds=1 sel=0.001":
        return 1000000;
      elif query=="ss #tp=8 #ds=1 sel=0.01":
        return 1000000;
      elif query=="ss #tp=8 #ds=3 sel=0.001":
        return 1000000;
      elif query=="ss #tp=8 #ds=3 sel=0.01":
        return 60;
  elif nHop==2:
    if datasetSize==1000000000:
      if query=="so #tp=2 #ds=1 sel=0.001":
        return 12620;
      elif query=="so #tp=2 #ds=1 sel=0.01":
        return 904983;
      elif query=="so #tp=8 #ds=1 sel=0.001":
        return 560675;
      elif query=="so #tp=8 #ds=1 sel=0.01":
        return 12789;
      elif query=="so #tp=8 #ds=3 sel=0.001":
        return 1000000;
      elif query=="so #tp=8 #ds=3 sel=0.01":
        return 1000000;
      elif query=="ss #tp=2 #ds=1 sel=0.001":
        return 1000000;
      elif query=="ss #tp=2 #ds=1 sel=0.01":
        return 710061;
      elif query=="ss #tp=8 #ds=1 sel=0.001":
        return 1000000;
      elif query=="ss #tp=8 #ds=1 sel=0.01":
        return 1000000;
      elif query=="ss #tp=8 #ds=3 sel=0.001":
        return 1000000;
      elif query=="ss #tp=8 #ds=3 sel=0.01":
        return 120;
  return -1;

def isAborted(query, nHop, datasetSize):
  return getNumberOfResults(query, nHop, datasetSize) >= 1000000

def getMaxNHopAndDatasetSize(dataRowFilters):
  nHop=0;
  datasetSize=0;
  for rowFilter in dataRowFilters:
    if rowFilter["n-hop"]>nHop:
      nHop = rowFilter["n-hop"]
    if rowFilter["datasetSize"]>datasetSize:
      datasetSize = rowFilter["datasetSize"]
  return nHop, datasetSize

def getQueries(inputFile, dataRowFilters, isLatex, separateAbortedQueries=True, onlyFinishedQueries=False, onlySOJoin=False):
  nHop, datasetSize=getMaxNHopAndDatasetSize(dataRowFilters)
  queriesFinished = set()
  queriesAborted = set()
  with open(inputFile, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
      rowDescriptor = getFilter(row,dataRowFilters)
      if not rowDescriptor is None:
        if onlySOJoin and row[6]!="SUBJECT_OBJECT_JOIN":
          continue; 
        query = getQuery(isLatex,row)
        if isAborted(query,nHop,datasetSize):
          queriesAborted.add(query)
        else:
          queriesFinished.add(query)
  if separateAbortedQueries:
    queriesFinished = list(sorted(queriesFinished))
    queriesAborted = list(sorted(queriesAborted))
    queries = []
    queries.extend(queriesFinished)
    queries.extend(queriesAborted)
  else:
    queries = set()
    queries.update(queriesFinished)
    queries.update(queriesAborted)
    queries = list(sorted(queries))
  if onlyFinishedQueries:
    return queriesFinished, 0
  else:
    return queries, len(queriesAborted)

def getDataForQueries(inputFile, dataRowFilters, dataColumn, queries, isLatex):
  headers = [None]*len(dataRowFilters)
  values = [0]*len(dataRowFilters)
  with open(inputFile, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
      rowDescriptor = getFilter(row,dataRowFilters)
      query = getQuery(isLatex,row)
      if (not rowDescriptor is None) and (query in queries):
        index = dataRowFilters.index(rowDescriptor)
        if headers[index] is None:
          headers[index]=rowDescriptor
          values[index]=[0]*len(queries)
        values[index][queries.index(query)]=float(row[dataColumn])
  return headers, values

def getDataForQueriesPerResult(inputFile, dataRowFilters, dataColumn, queries, isLatex):
  nHop, datasetSize=getMaxNHopAndDatasetSize(dataRowFilters)
  headers, values = getDataForQueries(inputFile, dataRowFilters, dataColumn, queries, isLatex)
  for i, rowFiler in enumerate(dataRowFilters):
    for j, query in enumerate(queries):
      values[i][j] = values[i][j]/float(getNumberOfResults(query, nHop, datasetSize))
  return headers, values

def getRelativeDataForQueries(headers, values, relHeader):
  indexOfRelHeader = headers.index(relHeader)
  relValue = values[indexOfRelHeader]
  newHeaders = []
  newValues = []
  isRelSkipped = False
  for i in range(0,len(headers)):
    if i != indexOfRelHeader:
      newHeaders.append(headers[i])
      newValues.append([])
      for j, value in enumerate(values[i]):
        if relValue[j] == 0.:
          newValues[i-1 if isRelSkipped else i].append(-1.)
        else:
          newValues[i-1 if isRelSkipped else i].append((value-relValue[j])/float(relValue[j])*100)
    else:
      isRelSkipped = True
  return newHeaders, newValues

def getResultOverTimeDataForQuery(inputFile, dataRowFilters, dataColumnStart, queryFilter, isLatex):
  headers = []
  times = []
  percentages = []
  with open(inputFile, 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
      rowDescriptor = getFilter(row,dataRowFilters)
      query = getQuery(isLatex,row)
      if (not rowDescriptor is None) and (query == queryFilter):
        if len(headers) == 0:
          headers = [None]*len(dataRowFilters)
          times = [None]*len(dataRowFilters)
          percentages = [None]*len(dataRowFilters)
        index = dataRowFilters.index(rowDescriptor)
        headers[index]=rowDescriptor
        times[index]=map(float,row[dataColumnStart:len(row)])
        row = reader.next()
        percentages[index]=map(float,row[dataColumnStart:len(row)])
  for i in range(0,len(times)):
    previousTime = 0.
    previousPercentage = 0.
    newTime = []
    newPercentage = []
    for j in range(0,len(times[i])):
      newTime.append(previousTime)
      newTime.append(times[i][j])
      previousTime=times[i][j]
      newPercentage.append(previousPercentage)
      newPercentage.append(previousPercentage)
      previousPercentage=percentages[i][j]
      if j == len(times[i])-1:
        newTime.append(times[i][j])
        newPercentage.append(percentages[i][j])
    times[i] = newTime
    percentages[i] = newPercentage
  return headers, times, percentages
