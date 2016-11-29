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

  public QueryOperationListener() {
    super();
    operationId2operation = new HashMap<>();
  }

  @Override
  public void processMeasurement(String... measurements) {
    super.processMeasurement(measurements);
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    long timestamp = Long.parseLong(measurements[4]);
    String computer = measurements[0];
    int index = computer.lastIndexOf(':');
    if (index >= 0) {
      computer = computer.substring(0, index);
    }
    if (measurementType != null) {
      switch (measurementType) {
        case QUERY_COORDINATOR_START:
          queryCoordinatorStartTime = timestamp;
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
                  numberOfChunks, new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp);
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
                  operation, computer, timestamp);
          break;
        case QUERY_OPERATION_CLOSED:
          operation = operationId2operation.get(new QuerySignature(currentQueryFileName, treeType))
                  .get(Long.parseLong(measurements[6]));
          processQueryOperationEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[6]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  operation, computer, timestamp);
          break;
        case QUERY_COORDINATOR_END:
          processQueryCoordinatorEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  timestamp);
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
          ExtendedQuerySignature extendedQuerySignature, long timestamp);

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
          String operation, String computer, long timestamp);

  protected abstract void processQueryOperationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          String operation, String computer, long timestamp);

  protected abstract void processQueryCoordinatorEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp);

}
