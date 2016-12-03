package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryOperationListener;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class QueryOperationOutput extends QueryOperationListener {

  private final Map<QuerySignature, Map<String, Map<String, Long>>> emittedOperationMappings;

  public QueryOperationOutput() {
    super();
    emittedOperationMappings = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "operationOutput.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\t(slave\toperation\temittedMappints)+";
  }

  @Override
  protected void processQueryCoordinatorStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature query,
          long queryCoordinatorStartTime) {
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
    if (extendedQuerySignature.repetition > 1) {
      return;
    }
    QuerySignature basicQuery = extendedQuerySignature.getBasicSignature();
    Map<String, Map<String, Long>> slaves = emittedOperationMappings.get(basicQuery);
    if (slaves == null) {
      slaves = new HashMap<>();
      emittedOperationMappings.put(basicQuery, slaves);
    }
    Map<String, Long> operations = slaves.get(computer);
    if (operations == null) {
      operations = new HashMap<>();
      slaves.put(computer, operations);
    }
    long emittedMappingsNumber = 0;
    for (int i = 0; i < emittedMappings.length; i++) {
      emittedMappingsNumber += emittedMappings[i];
    }
    operations.put(operation, emittedMappingsNumber);
  }

  @Override
  protected void processQueryResult(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, long queryResultSentTime,
          long firstResultNumber, long lastResultNumber) {
  }

  @Override
  protected void processQueryCoordinatorEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    StringBuilder sb = new StringBuilder();
    for (Entry<String, Map<String, Long>> slaves : emittedOperationMappings
            .get(query.getBasicSignature()).entrySet()) {
      for (Entry<String, Long> operations : slaves.getValue().entrySet()) {
        sb.append("\t").append(slaves.getKey()).append("\t").append(operations.getKey())
                .append("\t").append(operations.getValue());
      }
    }
    writeLine(sb.toString());
    emittedOperationMappings.remove(query.getBasicSignature());
  }

}
