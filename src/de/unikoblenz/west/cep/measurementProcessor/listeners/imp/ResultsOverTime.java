/*
 * This file is part of CEP.
 *
 * CEP is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * CEP is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Leser General Public License
 * along with CEP.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright 2016 Daniel Janke
 */
package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryTimesListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Queue;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class ResultsOverTime extends QueryTimesListener {

  private final Map<QuerySignature, Queue<long[]>[]> query2repetitiontimes;

  private long queryStartTime;

  private Queue<long[]> sequenceOfResults;

  private long numberOfResults;

  public ResultsOverTime() {
    super();
    query2repetitiontimes = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "resultsOverTime.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine();
  }

  @Override
  protected void processQueryStart(CoverStrategyType graphCoverStrategy, int nHopReplication,
          ExtendedQuerySignature query, long queryStartTime) {
    this.queryStartTime = queryStartTime;
    sequenceOfResults = new LinkedList<>();
  }

  @Override
  protected void processQueryResult(CoverStrategyType graphCoverStrategy, int nHopReplication,
          ExtendedQuerySignature query, long queryResultSentTime, long firstResultNumber,
          long lastResultNumber) {
    sequenceOfResults.add(new long[] { queryResultSentTime - queryStartTime, lastResultNumber });
    if (lastResultNumber > numberOfResults) {
      numberOfResults = lastResultNumber;
    }
  }

  @SuppressWarnings("unchecked")
  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    QuerySignature signature = query.getBasicSignature();
    Queue<long[]>[] timeLines = query2repetitiontimes.get(signature);
    if (timeLines == null) {
      timeLines = new Queue[numberOfRepetitions];
      query2repetitiontimes.put(signature, timeLines);
    }
    timeLines[query.repetition - 1] = sequenceOfResults;
    if (query.repetition == numberOfRepetitions) {
      query2repetitiontimes.remove(signature);
      computeAverageTimeLines(timeLines);
    }
    queryStartTime = 0;
    sequenceOfResults = new LinkedList<>();
    numberOfResults = 0;
  }

  private void computeAverageTimeLines(Queue<long[]>[] timeLines) {
    StringBuilder timePoints = new StringBuilder();
    StringBuilder resultPercents = new StringBuilder();
    long[] previousTimeSegment = null;
    for (long[] timeSegment = getNextTimeSegment(
            timeLines); timeSegment != null; timeSegment = getNextTimeSegment(timeLines)) {
      if ((previousTimeSegment != null) && (previousTimeSegment[0] != timeSegment[0])) {
        // write previous result segment if the timestamp has changed
        timePoints.append("\t").append(previousTimeSegment[0]);
        resultPercents.append("\t").append(previousTimeSegment[1] / (double) numberOfResults);
      }
      previousTimeSegment = timeSegment;
    }
    timePoints.append("\t").append(previousTimeSegment[0]);
    resultPercents.append("\t").append(
            numberOfResults > 0 ? previousTimeSegment[1] / (double) numberOfResults : "1.0");
    writeLine(timePoints.toString());
    writeLine(resultPercents.toString());
  }

  private long[] getNextTimeSegment(Queue<long[]>[] timeLines) {
    long[] times = new long[timeLines.length];
    long maxNumberOfResults = Long.MAX_VALUE;
    for (int i = 0; i < timeLines.length; i++) {
      long[] currentSegment = timeLines[i].peek();
      if (currentSegment == null) {
        return null;
      }
      times[i] = currentSegment[0];
      if (currentSegment[1] < maxNumberOfResults) {
        maxNumberOfResults = currentSegment[1];
      }
    }
    for (Queue<long[]> queue : timeLines) {
      if (queue.peek()[1] == maxNumberOfResults) {
        queue.poll();
      }
    }
    int numberOfSkippedValues = numberOfRepetitions / 10;
    if (numberOfSkippedValues > 0) {
      Arrays.sort(times);
      times = Arrays.copyOfRange(times, numberOfSkippedValues,
              times.length - numberOfSkippedValues);
    }
    return new long[] { Utilities.computeArithmeticMean(times), maxNumberOfResults };
  }

}
