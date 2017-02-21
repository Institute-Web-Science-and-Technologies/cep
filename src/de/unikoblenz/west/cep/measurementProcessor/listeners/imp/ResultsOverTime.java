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

  protected final Map<QuerySignature, long[]> queryStartTime;

  protected final Map<QuerySignature, long[]> queryEndTime;

  protected final Map<QuerySignature, long[]> queryExecutionStartTime;

  private final Map<QuerySignature, long[]> numberOfResults;

  public ResultsOverTime() {
    super();
    query2repetitiontimes = new HashMap<>();
    queryExecutionStartTime = new HashMap<>();
    queryStartTime = new HashMap<>();
    queryEndTime = new HashMap<>();
    numberOfResults = new HashMap<>();
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
          int numberOfChunks, ExtendedQuerySignature query, long queryStartTime) {
    QuerySignature signature = query.getBasicSignature();
    long[] startTimes = queryExecutionStartTime.get(signature);
    if (startTimes == null) {
      startTimes = new long[numberOfRepetitions];
      queryExecutionStartTime.put(signature, startTimes);
    } else if (startTimes.length < query.repetition) {
      long[] newStartTimes = new long[query.repetition];
      System.arraycopy(startTimes, 0, newStartTimes, 0, startTimes.length);
      startTimes = newStartTimes;
      queryExecutionStartTime.put(signature, startTimes);

    }
    startTimes[query.repetition - 1] = queryStartTime;

    long[] startTime = this.queryStartTime.get(signature);
    if (startTime == null) {
      startTime = new long[numberOfRepetitions];
      this.queryStartTime.put(signature, startTime);
    } else if (startTime.length < query.repetition) {
      long[] newStartTime = new long[query.repetition];
      System.arraycopy(startTime, 0, newStartTime, 0, startTime.length);
      startTime = newStartTime;
      this.queryStartTime.put(signature, startTime);

    }
    startTime[query.repetition - 1] = queryStartTime;
  }

  @Override
  protected void processQueryCoordinatorSendQueryStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
  }

  @SuppressWarnings("unchecked")
  @Override
  protected void processQueryResult(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, long queryResultSentTime,
          long firstResultNumber, long lastResultNumber) {
    QuerySignature signature = query.getBasicSignature();
    Queue<long[]>[] timeLines = query2repetitiontimes.get(signature);
    if (timeLines == null) {
      timeLines = new Queue[numberOfRepetitions];
      query2repetitiontimes.put(signature, timeLines);
    }
    if (timeLines.length < query.repetition) {
      timeLines = Arrays.copyOf(timeLines, query.repetition);
      query2repetitiontimes.put(signature, timeLines);
    }
    if (timeLines[query.repetition - 1] == null) {
      timeLines[query.repetition - 1] = new LinkedList<>();
    }
    timeLines[query.repetition - 1].add(new long[] {
            queryResultSentTime - queryExecutionStartTime.get(signature)[query.repetition - 1],
            lastResultNumber });

    long[] ends = queryEndTime.get(signature);
    if (ends == null) {
      ends = new long[numberOfRepetitions];
      queryEndTime.put(signature, ends);
    }
    if (ends.length < query.repetition) {
      ends = Arrays.copyOf(ends, query.repetition);
      queryEndTime.put(signature, ends);
    }
    if (ends[query.repetition - 1] < queryResultSentTime) {
      ends[query.repetition - 1] = queryResultSentTime;
    }

    long[] numberOfResult = numberOfResults.get(signature);
    if (numberOfResult == null) {
      numberOfResult = new long[numberOfRepetitions];
      numberOfResults.put(signature, numberOfResult);
    }
    if (numberOfResult.length < query.repetition) {
      numberOfResult = Arrays.copyOf(numberOfResult, query.repetition);
      numberOfResults.put(signature, numberOfResult);
    }
    if (lastResultNumber > numberOfResult[query.repetition - 1]) {
      numberOfResult[query.repetition - 1] = lastResultNumber;
    }
  }

  @SuppressWarnings("unchecked")
  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    if (query.repetition >= numberOfRepetitions) {
      QuerySignature signature = query.getBasicSignature();
      Queue<long[]>[] timeLines = query2repetitiontimes.get(signature);
      Queue<long[]> minTimeLine = null;
      int minIndex = 0;
      long minExecutionTime = Long.MAX_VALUE;
      for (int i = 0; i < timeLines.length; i++) {
        Queue<long[]> queue = timeLines[i];
        long exTime = queryEndTime.get(signature)[i] - queryStartTime.get(signature)[i];
        if (exTime < minExecutionTime) {
          minIndex = i;
          minTimeLine = queue;
          minExecutionTime = exTime;
        }
      }
      Queue<long[]> copy = new LinkedList<>();
      for (long[] elem : minTimeLine) {
        copy.offer(elem);
      }
      computeAverageTimeLines(new Queue[] { copy }, numberOfResults.get(signature)[minIndex]);
    }
  }

  private void computeAverageTimeLines(Queue<long[]>[] timeLines, long numberOfResults) {
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
    resultPercents.append("\t")
            .append(/*
                     * numberOfResults > 0 ? previousTimeSegment[1] / (double)
                     * numberOfResults :
                     */ "1.0");
    writeLine(timePoints.toString(), resultPercents.toString());
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
    return new long[] { Utilities.computeArithmeticMean(times), maxNumberOfResults };
  }

}
