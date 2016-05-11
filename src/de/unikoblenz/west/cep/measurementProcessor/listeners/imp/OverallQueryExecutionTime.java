package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryTimesListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class OverallQueryExecutionTime extends QueryTimesListener {

  private final Map<QuerySignature, long[]> query2repetitiontimes;

  private long queryStartTime;

  private long totalQueryExecutionTime;

  public OverallQueryExecutionTime() {
    super();
    query2repetitiontimes = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "totalExecutionTime.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\ttotalExecutionTime";
  }

  @Override
  protected void processQueryStart(CoverStrategyType graphCoverStrategy, int nHopReplication,
          ExtendedQuerySignature query, long queryStartTime) {
    this.queryStartTime = queryStartTime;
  }

  @Override
  protected void processQueryResult(CoverStrategyType graphCoverStrategy, int nHopReplication,
          ExtendedQuerySignature query, long queryResultSentTime, long firstResultNumber,
          long lastResultNumber) {
    long executionTime = queryResultSentTime - queryStartTime;
    if (executionTime > totalQueryExecutionTime) {
      totalQueryExecutionTime = executionTime;
    }
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    QuerySignature basicSignature = query.getBasicSignature();
    long[] repetitions = query2repetitiontimes.get(basicSignature);
    if (repetitions == null) {
      repetitions = new long[numberOfRepetitions];
      query2repetitiontimes.put(basicSignature, repetitions);
    }
    repetitions[query.repetition - 1] = totalQueryExecutionTime;
    if (query.repetition == numberOfRepetitions) {
      query2repetitiontimes.remove(basicSignature);
      int numberOfSkippedValues = numberOfRepetitions / 10;
      if (numberOfSkippedValues > 0) {
        Arrays.sort(repetitions);
        repetitions = Arrays.copyOfRange(repetitions, numberOfSkippedValues,
                repetitions.length - numberOfSkippedValues);
      }
      writeLine("\t" + Utilities.computeArithmeticMean(repetitions));
    }
    queryStartTime = 0;
    totalQueryExecutionTime = 0;
  }

}
