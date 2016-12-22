package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryOperationListener;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class QueryExecutionTimeline extends QueryOperationListener {

  private final Map<QuerySignature, long[]> parseStarts;

  private final Map<QuerySignature, long[]> parseEnds;

  private final Map<QuerySignature, long[]> sendQueryEnds;

  private final Map<QuerySignature, long[]> executionEnds;

  public QueryExecutionTimeline() {
    super();
    parseStarts = new HashMap<>();
    parseEnds = new HashMap<>();
    sendQueryEnds = new HashMap<>();
    executionEnds = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "executionTimelines.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\tparseTime\tquerySendTime\texecutionTime";
  }

  @Override
  protected void processQueryCoordinatorStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature query,
          long queryCoordinatorStartTime) {
    QuerySignature basicSignature = query.getBasicSignature();
    long[] starts = parseStarts.get(basicSignature);
    if (starts == null) {
      starts = new long[numberOfRepetitions];
      parseStarts.put(basicSignature, starts);
    }
    starts[query.repetition - 1] = queryCoordinatorStartTime;
  }

  @Override
  protected void processQueryCoordinatorParseStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
  }

  @Override
  protected void processQueryCoordinatorParseEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    long[] ends = parseEnds.get(basicSignature);
    if (ends == null) {
      ends = new long[numberOfRepetitions];
      parseEnds.put(basicSignature, ends);
    }
    ends[extendedQuerySignature.repetition - 1] = timestamp;
  }

  @Override
  protected void processQueryCoordinatorSendQueryToSlaves(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
  }

  @Override
  protected void processSlaveCreatesQueryStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, String computer,
          ExtendedQuerySignature extendedQuerySignature, long timestamp) {
  }

  @Override
  protected void processSlaveCreatesQueryEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, String computer,
          ExtendedQuerySignature extendedQuerySignature, long timestamp) {
  }

  @Override
  protected void processQueryCoordinatorSendQueryStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    long[] ends = sendQueryEnds.get(basicSignature);
    if (ends == null) {
      ends = new long[numberOfRepetitions];
      sendQueryEnds.put(basicSignature, ends);
    }
    ends[extendedQuerySignature.repetition - 1] = timestamp;
  }

  @Override
  protected void processQueryOperationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          String operation, String computer, long timestamp) {
  }

  @Override
  protected void processQueryOperationSentMappingsToOtherSlaves(
          CoverStrategyType graphCoverStrategy, int nHopReplication, int numberOfChunks,
          ExtendedQuerySignature extendedQuerySignature, String operation, String computer,
          long[] emittedValuesToOtherSlaves) {
  }

  @Override
  protected void processQueryOperationEnd(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature extendedQuerySignature, String operation,
          String computer, long timestamp, long[] emittedMappings) {
  }

  @Override
  protected void processQueryResult(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature extendedQuerySignature, long timestamp,
          long firstResultNumber, long lastResultNumber) {
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    long[] ends = executionEnds.get(basicSignature);
    if (ends == null) {
      ends = new long[numberOfRepetitions];
      executionEnds.put(basicSignature, ends);
    }
    if (ends[extendedQuerySignature.repetition - 1] < timestamp) {
      ends[extendedQuerySignature.repetition - 1] = timestamp;
    }
  }

  @Override
  protected void processQueryCoordinatorEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    if (query.repetition != numberOfRepetitions) {
      return;
    }
    QuerySignature basicSignature = query.getBasicSignature();
    int numberOfSkippedValues = numberOfRepetitions / 10;
    long[][] measuredTimes = { parseStarts.get(basicSignature), parseEnds.get(basicSignature),
            sendQueryEnds.get(basicSignature), executionEnds.get(basicSignature) };
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < (measuredTimes.length - 1); i++) {
      long[] executionTimes = new long[measuredTimes[0].length];
      for (int j = 0; j < executionTimes.length; j++) {
        executionTimes[j] = measuredTimes[i + 1][j] - measuredTimes[i][j];
      }
      if (numberOfSkippedValues > 0) {
        Arrays.sort(executionTimes);
        executionTimes = Arrays.copyOfRange(executionTimes, numberOfSkippedValues,
                executionTimes.length - numberOfSkippedValues);
      }
      long averageTime = Utilities.computeArithmeticMean(executionTimes);
      sb.append("\t").append(averageTime);
    }
    writeLine(sb.toString());
  }

}
