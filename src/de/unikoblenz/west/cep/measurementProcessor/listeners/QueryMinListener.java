package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class QueryMinListener extends QueryListener {

  private long queryCoordinatorStartTime;

  private boolean hasProcessedQueryResults;

  private final Map<QuerySignature, long[]> queryStartTime;

  private final Map<QuerySignature, long[]> queryEndTime;

  public QueryMinListener() {
    queryStartTime = new HashMap<>();
    queryEndTime = new HashMap<>();
  }

  @Override
  public void processMeasurement(String... measurements) {
    super.processMeasurement(measurements);
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case QUERY_COORDINATOR_START:
          queryCoordinatorStartTime = Long.parseLong(measurements[4]);
          break;
        case QUERY_COORDINATOR_PARSE_START:
          processQueryStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  queryCoordinatorStartTime);
          break;
        case QUERY_COORDINATOR_SEND_QUERY_RESULTS_TO_CLIENT:
          ExtendedQuerySignature query = new ExtendedQuerySignature(
                  Integer.parseInt(measurements[5]), currentQueryFileName, treeType,
                  currentQueryRepetition);
          processQueryResult(graphCoverStrategy, nHopReplication, numberOfChunks, query,
                  Long.parseLong(measurements[4]), Long.parseLong(measurements[6]),
                  Long.parseLong(measurements[7]));
          hasProcessedQueryResults = true;
          break;
        case QUERY_COORDINATOR_END:
          query = new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                  currentQueryFileName, treeType, currentQueryRepetition);
          if (!hasProcessedQueryResults) {
            processQueryResult(graphCoverStrategy, nHopReplication, numberOfChunks, query,
                    Long.parseLong(measurements[4]), 0, 0);
          }
          hasProcessedQueryResults = false;
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  private void processQueryStart(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, long queryStartTime) {
    QuerySignature signature = query.getBasicSignature();
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

  private void processQueryResult(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, long queryResultSentTime,
          long firstResultNumber, long lastResultNumber) {
    QuerySignature signature = query.getBasicSignature();
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
  }

  @Override
  protected final void processQueryFinish(ExtendedQuerySignature query) {
    if (query.repetition >= numberOfRepetitions) {
      QuerySignature signature = query.getBasicSignature();
      int minIndex = 0;
      long minExecutionTime = Long.MAX_VALUE;
      long[] endTimes = queryEndTime.get(signature);
      long[] startTime = queryStartTime.get(signature);
      for (int i = 0; i < endTimes.length; i++) {
        long exTime = endTimes[i] - startTime[i];
        if (exTime < minExecutionTime) {
          minIndex = i;
          minExecutionTime = exTime;
        }
      }
      processQueryFinish(query, minIndex);
    }
  }

  protected abstract void processQueryFinish(ExtendedQuerySignature query, int minRepetitionIndex);

}
