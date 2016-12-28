package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryOperationListener;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.TreeMap;
import java.util.regex.Pattern;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class QueryOperationTimesPerSlave extends QueryOperationListener {

  private final Map<QuerySignature, long[]> startTimeOfExecution;

  private final Map<QuerySignature, Map<String, Map<String, long[][]>>> operationExecutionTimesPerSlaveAndQuery;

  private final Map<QuerySignature, long[]> query2starttimes;

  private final Map<QuerySignature, long[]> query2endtimes;

  public QueryOperationTimesPerSlave() {
    super();
    operationExecutionTimesPerSlaveAndQuery = new HashMap<>();
    startTimeOfExecution = new HashMap<>();
    query2starttimes = new HashMap<>();
    query2endtimes = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(
            outputDirectory.getAbsolutePath() + File.separator + "operationTimesPerSlave.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\t(slave\toperation\tstartTime\texecutionTime)+\tqueryEndTime";
  }

  @Override
  protected void processQueryCoordinatorStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature query,
          long queryCoordinatorStartTime) {
    QuerySignature basicSignature = query.getBasicSignature();
    long[] startTime = startTimeOfExecution.get(basicSignature);
    if (startTime != null) {
      if (startTime.length < query.repetition) {
        startTime = Arrays.copyOf(startTime, query.repetition);
        startTimeOfExecution.put(basicSignature, startTime);
      }
      startTime[query.repetition - 1] = 0;
    }
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
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    long[] executionTimes = startTimeOfExecution.get(basicSignature);
    if (executionTimes == null) {
      executionTimes = new long[numberOfRepetitions];
      startTimeOfExecution.put(basicSignature, executionTimes);
    } else if (executionTimes.length < extendedQuerySignature.repetition) {
      executionTimes = Arrays.copyOf(executionTimes, extendedQuerySignature.repetition);
      startTimeOfExecution.put(basicSignature, executionTimes);
    }
    if (executionTimes[extendedQuerySignature.repetition - 1] == 0) {
      executionTimes[extendedQuerySignature.repetition - 1] = timestamp;
    } else {
      executionTimes[extendedQuerySignature.repetition
              - 1] = executionTimes[extendedQuerySignature.repetition - 1] - timestamp;
      Map<String, Map<String, long[][]>> opsPerSlave = operationExecutionTimesPerSlaveAndQuery
              .get(basicSignature);
      if (opsPerSlave != null) {
        for (Entry<String, Map<String, long[][]>> slaves : opsPerSlave.entrySet()) {
          Map<String, long[][]> ops = slaves.getValue();
          if (ops != null) {
            for (Entry<String, long[][]> op : ops.entrySet()) {
              long[][] opTimes = op.getValue();
              if ((opTimes != null) && (opTimes[1] != null)) {
                if (opTimes[1].length < extendedQuerySignature.repetition) {
                  opTimes[1] = Arrays.copyOf(opTimes[1], extendedQuerySignature.repetition);
                }
                opTimes[1][extendedQuerySignature.repetition
                        - 1] = executionTimes[extendedQuerySignature.repetition - 1];
              }
            }
          }
        }
      }
    }
    long[] startTimes = query2starttimes.get(basicSignature);
    if (startTimes == null) {
      startTimes = new long[numberOfRepetitions];
      query2starttimes.put(basicSignature, startTimes);
    } else if (startTimes.length < extendedQuerySignature.repetition) {
      startTimes = Arrays.copyOf(startTimes, extendedQuerySignature.repetition);
      query2starttimes.put(basicSignature, startTimes);
    }
    startTimes[extendedQuerySignature.repetition - 1] = timestamp;
  }

  @Override
  protected void processQueryOperationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          String operation, String computer, long timestamp) {
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    Map<String, Map<String, long[][]>> operationExecutionTimesPerSlave = operationExecutionTimesPerSlaveAndQuery
            .get(basicSignature);
    if (operationExecutionTimesPerSlave == null) {
      operationExecutionTimesPerSlave = new TreeMap<>();
      operationExecutionTimesPerSlaveAndQuery.put(basicSignature, operationExecutionTimesPerSlave);
    }
    Map<String, long[][]> operationsOfSlave = operationExecutionTimesPerSlave.get(computer);
    if (operationsOfSlave == null) {
      operationsOfSlave = new HashMap<>();
      operationExecutionTimesPerSlave.put(computer, operationsOfSlave);
    }
    long[][] operationTimes = operationsOfSlave.get(operation);
    if (operationTimes == null) {
      operationTimes = new long[2][numberOfRepetitions];
      operationsOfSlave.put(operation, operationTimes);
    }
    if (operationTimes[0].length < extendedQuerySignature.repetition) {
      operationTimes[0] = Arrays.copyOf(operationTimes[0], extendedQuerySignature.repetition);
    }
    operationTimes[0][extendedQuerySignature.repetition - 1] = timestamp;
    long[] startTimes = startTimeOfExecution.get(basicSignature);
    if (startTimes == null) {
      startTimes = new long[numberOfRepetitions];
      startTimeOfExecution.put(basicSignature, startTimes);
    } else if (startTimes.length < extendedQuerySignature.repetition) {
      startTimes = Arrays.copyOf(startTimes, extendedQuerySignature.repetition);
      startTimeOfExecution.put(basicSignature, startTimes);
    }
    if (operationTimes[1].length < extendedQuerySignature.repetition) {
      operationTimes[1] = Arrays.copyOf(operationTimes[1], extendedQuerySignature.repetition);
    }
    operationTimes[1][extendedQuerySignature.repetition - 1] = timestamp
            - startTimes[extendedQuerySignature.repetition - 1];
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
    long[][] operationTimes = operationExecutionTimesPerSlaveAndQuery
            .get(extendedQuerySignature.getBasicSignature()).get(computer).get(operation);
    if (operationTimes[0].length < extendedQuerySignature.repetition) {
      operationTimes[0] = Arrays.copyOf(operationTimes[0], extendedQuerySignature.repetition);
    }
    operationTimes[0][extendedQuerySignature.repetition - 1] = timestamp
            - operationTimes[0][extendedQuerySignature.repetition - 1];
  }

  @Override
  protected void processQueryResult(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature extendedQuerySignature, long timestamp,
          long firstResultNumber, long lastResultNumber) {
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    long[] endTimes = query2endtimes.get(basicSignature);
    if (endTimes == null) {
      endTimes = new long[numberOfRepetitions];
      query2endtimes.put(basicSignature, endTimes);
    } else if (endTimes.length < extendedQuerySignature.repetition) {
      endTimes = Arrays.copyOf(endTimes, extendedQuerySignature.repetition);
      query2endtimes.put(basicSignature, endTimes);
    }
    if (timestamp > endTimes[extendedQuerySignature.repetition - 1]) {
      endTimes[extendedQuerySignature.repetition - 1] = timestamp;
    }
  }

  @Override
  protected void processQueryCoordinatorEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    long[] endTimes = query2endtimes.get(basicSignature);
    if (endTimes == null) {
      endTimes = new long[numberOfRepetitions];
      query2endtimes.put(basicSignature, endTimes);
    } else if (endTimes.length < extendedQuerySignature.repetition) {
      endTimes = Arrays.copyOf(endTimes, extendedQuerySignature.repetition);
      query2endtimes.put(basicSignature, endTimes);
    }
    if (endTimes[extendedQuerySignature.repetition - 1] > 0) {
      endTimes[extendedQuerySignature.repetition - 1] = timestamp;
    }
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    if (query.repetition < numberOfRepetitions) {
      return;
    }
    class Element implements Comparable<Element> {
      private final int operatorId;
      private final long executionTime;
      private final long startTime;
      private final String operation;

      public Element(String operation, long startTime, long executionTime) {
        this.executionTime = executionTime;
        this.startTime = startTime;
        this.operation = operation;
        operatorId = Integer.parseInt(operation.split(Pattern.quote(":"))[0]);
      }

      @Override
      public int compareTo(Element o) {
        return operatorId - o.operatorId;
        // long value = executionTime - o.executionTime;
        // return value == 0 ? 0 : value < 0 ? -1 : 1;
      }

    }
    StringBuilder sb = new StringBuilder();
    Map<String, Map<String, long[][]>> perQuery = operationExecutionTimesPerSlaveAndQuery
            .get(query.getBasicSignature());
    int minIndex = 0;
    long minExecutionTime = Long.MAX_VALUE;
    long[] startTimes = query2starttimes.get(query.getBasicSignature());
    long[] endTimes = query2endtimes.get(query.getBasicSignature());
    for (int i = 0; i < startTimes.length; i++) {
      long executionTime = endTimes[i] - startTimes[i];
      if (executionTime < minExecutionTime) {
        minIndex = i;
        minExecutionTime = executionTime;
      }
    }
    for (Entry<String, Map<String, long[][]>> slaveEntry : perQuery.entrySet()) {
      Set<Entry<String, long[][]>> entrySet = slaveEntry.getValue().entrySet();
      Element[] elements = new Element[entrySet.size()];
      int next = 0;
      for (Entry<String, long[][]> operationEntry : entrySet) {
        long[][] repetitions = operationEntry.getValue();
        long averageExecutionTime = repetitions[0][minIndex];
        long averageStartTime = repetitions[1][minIndex];
        if (averageStartTime >= 1420070400000L/* 1.1.2015 */) {
          // this match operation had nothing to process
          averageStartTime = 0;
        }
        if (averageExecutionTime >= 31536000000L/* =1year */) {
          averageExecutionTime = -1000;
        }
        elements[next++] = new Element(operationEntry.getKey(), averageStartTime,
                averageExecutionTime);
      }
      Arrays.sort(elements);
      for (Element element : elements) {
        sb.append("\t").append(slaveEntry.getKey()).append("\t").append(element.operation)
                .append("\t").append(element.startTime).append("\t").append(element.executionTime);
      }
    }
    sb.append("\t").append(minExecutionTime);
    writeLine(sb.toString());
    operationExecutionTimesPerSlaveAndQuery.remove(query.getBasicSignature());
  }

}
