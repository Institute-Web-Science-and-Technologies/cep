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
  }

  private void computeAverageTimeLines(Queue<long[]>[] timeLines) {
    StringBuilder timePoints = new StringBuilder();
    StringBuilder resultPercents = new StringBuilder();
    for (long[] timeSegment = getNextTimeSegment(
            timeLines); timeSegment != null; timeSegment = getNextTimeSegment(timeLines)) {
      timePoints.append("\t").append(timeSegment[0]);
      resultPercents.append("\t").append(timeSegment[1] / (double) numberOfResults);
    }
    writeLine(timePoints.toString());
    writeLine(resultPercents.toString());
  }

  private long[] getNextTimeSegment(Queue<long[]>[] timeLines) {
    long[] times = new long[timeLines.length];
    long maxNumberOfResults = Long.MAX_VALUE;
    int index2remove = -1;
    for (int i = 0; i < timeLines.length; i++) {
      long[] currentSegment = timeLines[i].peek();
      if (currentSegment == null) {
        return null;
      }
      times[i] = currentSegment[0];
      if (currentSegment[1] < maxNumberOfResults) {
        maxNumberOfResults = currentSegment[1];
        index2remove = i;
      }
    }
    // TODO Auto-generated method stub
    timeLines[index2remove].poll();
    int numberOfSkippedValues = numberOfRepetitions / 10;
    if (numberOfSkippedValues > 0) {
      Arrays.sort(times);
      times = Arrays.copyOfRange(times, numberOfSkippedValues,
              times.length - numberOfSkippedValues);
    }
    return new long[] { Utilities.computeArithmeticMean(times), maxNumberOfResults };
  }

}
