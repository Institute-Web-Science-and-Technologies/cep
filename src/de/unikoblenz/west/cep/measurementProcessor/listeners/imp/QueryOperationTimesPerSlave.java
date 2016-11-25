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
import java.util.Map.Entry;
import java.util.Set;
import java.util.TreeMap;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class QueryOperationTimesPerSlave extends QueryOperationListener {

  private final Map<QuerySignature, Map<String, Map<String, long[]>>> operationExecutionTimesPerSlaveAndQuery;

  public QueryOperationTimesPerSlave() {
    super();
    operationExecutionTimesPerSlaveAndQuery = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(
            outputDirectory.getAbsolutePath() + File.separator + "operationTimesPerSlave.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\t(slave\toperation\texecutionTime)+";
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
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    Map<String, Map<String, long[]>> operationExecutionTimesPerSlave = operationExecutionTimesPerSlaveAndQuery
            .get(basicSignature);
    if (operationExecutionTimesPerSlave == null) {
      operationExecutionTimesPerSlave = new TreeMap<>();
      operationExecutionTimesPerSlaveAndQuery.put(basicSignature, operationExecutionTimesPerSlave);
    }
    Map<String, long[]> operationsOfSlave = operationExecutionTimesPerSlave.get(computer);
    if (operationsOfSlave == null) {
      operationsOfSlave = new HashMap<>();
      operationExecutionTimesPerSlave.put(computer, operationsOfSlave);
    }
    long[] operationTimes = operationsOfSlave.get(operation);
    if (operationTimes == null) {
      operationTimes = new long[numberOfRepetitions];
      operationsOfSlave.put(operation, operationTimes);
    }
    operationTimes[extendedQuerySignature.repetition - 1] = timestamp;
  }

  @Override
  protected void processQueryOperationEnd(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature extendedQuerySignature, String operation,
          String computer, long timestamp) {
    long[] operationTimes = operationExecutionTimesPerSlaveAndQuery
            .get(extendedQuerySignature.getBasicSignature()).get(computer).get(operation);
    operationTimes[extendedQuerySignature.repetition - 1] = timestamp
            - operationTimes[extendedQuerySignature.repetition - 1];
  }

  @Override
  protected void processQueryCoordinatorEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    class Element implements Comparable<Element> {
      private final long executionTime;
      private final String operation;

      public Element(String operation, long executionTime) {
        this.executionTime = executionTime;
        this.operation = operation;
      }

      @Override
      public int compareTo(Element o) {
        long value = executionTime - o.executionTime;
        return value == 0 ? 0 : value < 0 ? -1 : 1;
      }

    }
    StringBuilder sb = new StringBuilder();
    Map<String, Map<String, long[]>> perQuery = operationExecutionTimesPerSlaveAndQuery
            .get(query.getBasicSignature());
    for (Entry<String, Map<String, long[]>> slaveEntry : perQuery.entrySet()) {
      Set<Entry<String, long[]>> entrySet = slaveEntry.getValue().entrySet();
      Element[] elements = new Element[entrySet.size()];
      int next = 0;
      for (Entry<String, long[]> operationEntry : entrySet) {
        long[] repetitions = operationEntry.getValue();
        int numberOfSkippedValues = numberOfRepetitions / 10;
        if (numberOfSkippedValues > 0) {
          Arrays.sort(repetitions);
          repetitions = Arrays.copyOfRange(repetitions, numberOfSkippedValues,
                  repetitions.length - numberOfSkippedValues);
        }
        long averageExecutionTime = Utilities.computeArithmeticMean(repetitions);
        elements[next++] = new Element(operationEntry.getKey(), averageExecutionTime);
      }
      Arrays.sort(elements);
      for (Element element : elements) {
        sb.append("\t").append(slaveEntry.getKey()).append("\t").append(element.operation)
                .append("\t").append(element.executionTime);
      }
    }
    writeLine(sb.toString());
    operationExecutionTimesPerSlaveAndQuery.remove(query.getBasicSignature());
  }

}
