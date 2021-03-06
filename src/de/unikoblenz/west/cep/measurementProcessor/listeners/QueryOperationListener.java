package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class QueryOperationListener extends QueryListener {

  private long queryCoordinatorStartTime;

  private final Map<QuerySignature, Map<Long, String>> operationId2operation;

  private boolean isQueryOpen;

  public QueryOperationListener() {
    super();
    operationId2operation = new HashMap<>();
  }

  protected Map<Long, String> getOperations(QuerySignature query) {
    return operationId2operation.get(query);
  }

  protected String getOperationName(QuerySignature query, long queryId) {
    return operationId2operation.get(query).get(queryId);
  }

  @Override
  public void processMeasurement(String... measurements) {
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if ((measurementType == MeasurementType.QUERY_COORDINATOR_START) && isQueryOpen) {
      ExtendedQuerySignature query = new ExtendedQuerySignature(
              Integer.parseInt(measurements[5]) - 1, currentQueryFileName, treeType,
              currentQueryRepetition);
      processQueryCoordinatorEnd(graphCoverStrategy, nHopReplication, numberOfChunks, query,
              Long.parseLong(measurements[4]));
    }
    super.processMeasurement(measurements);
    long timestamp = Long.parseLong(measurements[4]);
    String computer = measurements[0];
    // int index = computer.lastIndexOf(':');
    // if (index >= 0) {
    // computer = computer.substring(0, index);
    // }
    if (measurementType != null) {
      switch (measurementType) {
        case QUERY_COORDINATOR_START:
          queryCoordinatorStartTime = timestamp;
          isQueryOpen = true;
          break;
        case QUERY_COORDINATOR_PARSE_START:
          processQueryCoordinatorStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  queryCoordinatorStartTime);
          processQueryCoordinatorParseStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp);
          break;
        case QUERY_COORDINATOR_PARSE_END:
          processQueryCoordinatorParseEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp);
          break;
        case QUERY_COORDINATOR_QET_NODES:
          QuerySignature querySignature = new QuerySignature(currentQueryFileName, treeType);
          Map<Long, String> operationId2operation2 = operationId2operation.get(querySignature);
          if (operationId2operation2 == null) {
            operationId2operation2 = new HashMap<>();
            operationId2operation.put(querySignature, operationId2operation2);
          }
          for (int i = 5; i < measurements.length; i += 2) {
            operationId2operation2.put(Long.parseLong(measurements[i]),
                    measurements[i] + ":" + measurements[i + 1]);
          }
          break;
        case QUERY_COORDINATOR_SEND_QUERY_TO_SLAVE:
          processQueryCoordinatorSendQueryToSlaves(graphCoverStrategy, nHopReplication,
                  numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  computer, timestamp);
          break;
        case QUERY_SLAVE_QUERY_CREATION_START:
          processSlaveCreatesQueryStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  computer, new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp);
          break;
        case QUERY_SLAVE_QUERY_CREATION_END:
          processSlaveCreatesQueryEnd(graphCoverStrategy, nHopReplication, numberOfChunks, computer,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp);
          break;
        case QUERY_COORDINATOR_SEND_QUERY_START:
          processQueryCoordinatorSendQueryStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp);
          break;
        case QUERY_OPERATION_START:
          String operation = operationId2operation
                  .get(new QuerySignature(currentQueryFileName, treeType))
                  .get(Long.parseLong(measurements[6]));
          processQueryOperationStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  Long.parseLong(measurements[6]), operation, computer, timestamp);
          break;
        case QUERY_OPERATION_SENT_MAPPINGS_TO_SLAVE:
          operation = operationId2operation.get(new QuerySignature(currentQueryFileName, treeType))
                  .get(Long.parseLong(measurements[5]));
          long[] emittedValuesToOtherSlaves = new long[numberOfChunks];
          for (int i = 1; i < emittedValuesToOtherSlaves.length; i++) {
            emittedValuesToOtherSlaves[i] = Long.parseLong(measurements[6 + ((i - 1) * 2) + 1]);
          }
          processQueryOperationSentMappingsToOtherSlaves(graphCoverStrategy, nHopReplication,
                  numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[4]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  Long.parseLong(measurements[5]), operation, computer, emittedValuesToOtherSlaves);
          break;
        case QUERY_OPERATION_CLOSED:
          operation = operationId2operation.get(new QuerySignature(currentQueryFileName, treeType))
                  .get(Long.parseLong(measurements[6]));
          long[] emittedValues = new long[measurements.length - 9];
          for (int i = 9; i < measurements.length; i++) {
            emittedValues[i - 9] = Long.parseLong(measurements[i]);
          }
          processQueryOperationEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  Long.parseLong(measurements[6]), operation, computer, timestamp, emittedValues);
          break;
        case QUERY_COORDINATOR_SEND_QUERY_RESULTS_TO_CLIENT:
          processQueryResult(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp, Long.parseLong(measurements[6]), Long.parseLong(measurements[7]));
          break;
        case QUERY_COORDINATOR_END:
          processQueryCoordinatorEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp);
          isQueryOpen = false;
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processQueryCoordinatorStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature query,
          long queryCoordinatorStartTime);

  protected abstract void processQueryCoordinatorParseStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp);

  protected abstract void processQueryCoordinatorParseEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp);

  protected abstract void processQueryCoordinatorSendQueryToSlaves(
          CoverStrategyType graphCoverStrategy, int nHopReplication, int numberOfChunks,
          ExtendedQuerySignature extendedQuerySignature, String computer, long timestamp);

  protected abstract void processSlaveCreatesQueryStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, String computer,
          ExtendedQuerySignature extendedQuerySignature, long timestamp);

  protected abstract void processSlaveCreatesQueryEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, String computer,
          ExtendedQuerySignature extendedQuerySignature, long timestamp);

  protected abstract void processQueryCoordinatorSendQueryStart(
          CoverStrategyType graphCoverStrategy, int nHopReplication, int numberOfChunks,
          ExtendedQuerySignature extendedQuerySignature, long timestamp);

  protected abstract void processQueryOperationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long operationId, String operation, String computer, long timestamp);

  protected abstract void processQueryOperationSentMappingsToOtherSlaves(
          CoverStrategyType graphCoverStrategy, int nHopReplication, int numberOfChunks,
          ExtendedQuerySignature extendedQuerySignature, long operationId, String operation,
          String computer, long[] emittedValuesToOtherSlaves);

  /**
   * @param graphCoverStrategy
   * @param nHopReplication
   * @param numberOfChunks
   * @param extendedQuerySignature
   * @param operationId
   * @param operation
   * @param computer
   * @param timestamp
   * @param emittedMappings
   *          first index: number of mappings emitted to master; thereafter
   *          mappings emitted to slaves
   */
  protected abstract void processQueryOperationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long operationId, String operation, String computer, long timestamp,
          long[] emittedMappings);

  protected abstract void processQueryResult(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature query,
          long queryResultSentTime, long firstResultNumber, long lastResultNumber);

  protected abstract void processQueryCoordinatorEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp);

}
