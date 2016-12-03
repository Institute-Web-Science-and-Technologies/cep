package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryOperationListener;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;

import java.io.File;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class QueryOperationInput extends QueryOperationListener {

  private final Map<QuerySignature, Map<String, Map<String, long[]>>> emittedOperationMappings;

  private final Map<QuerySignature, Map<String, String>> parentOperations;

  private final Map<QuerySignature, Map<Integer, String>> slaveIds;

  public QueryOperationInput() {
    super();
    emittedOperationMappings = new HashMap<>();
    parentOperations = new HashMap<>();
    slaveIds = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "operationInput.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\t(slave\toperation\treceivedMappints)+";
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
    if (extendedQuerySignature.repetition > 1) {
      return;
    }
    QuerySignature basicSignature = extendedQuerySignature.getBasicSignature();
    Map<Integer, String> slaveIds = this.slaveIds.get(basicSignature);
    if (slaveIds == null) {
      slaveIds = new HashMap<>();
      slaveIds.put(0, "master");
      this.slaveIds.put(basicSignature, slaveIds);
    }
    if (slaveIds.containsValue(computer)) {
      return;
    }
    long[] emittedValues = emittedOperationMappings.get(basicSignature).get(computer)
            .get(operation);
    int i = 1;
    for (i = 1; i < emittedValuesToOtherSlaves.length; i++) {
      if (emittedValues[i] != emittedValuesToOtherSlaves[i]) {
        slaveIds.put(i, computer);
        return;
      }
    }
    slaveIds.put(i, computer);
  }

  @Override
  protected void processQueryOperationEnd(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature extendedQuerySignature, String operation,
          String computer, long timestamp, long[] emittedMappings) {
    if (extendedQuerySignature.repetition > 1) {
      return;
    }
    QuerySignature basicQuery = extendedQuerySignature.getBasicSignature();
    Map<String, Map<String, long[]>> slaves = emittedOperationMappings.get(basicQuery);
    if (slaves == null) {
      slaves = new HashMap<>();
      emittedOperationMappings.put(basicQuery, slaves);
    }
    Map<String, long[]> operations = slaves.get(computer);
    if (operations == null) {
      operations = new HashMap<>();
      slaves.put(computer, operations);
    }
    operations.put(operation, emittedMappings);
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
    QuerySignature basicSignature = query.getBasicSignature();
    Map<Integer, String> slaveIds = this.slaveIds.get(basicSignature);
    Map<String, Map<String, long[]>> emittedMappings = emittedOperationMappings.get(basicSignature);
    Map<String, Map<String, Long>> receivedMappings = new HashMap<>();
    for (Entry<String, Map<String, long[]>> slaves : emittedMappings.entrySet()) {
      for (Entry<String, long[]> operations : slaves.getValue().entrySet()) {
        String parentOperation = getParentOperation(basicSignature, operations.getKey());
        if ((parentOperation == null) || parentOperation.contains("slice")) {
          parentOperation = "query coordinator";
        }
        long[] emittedMaps = operations.getValue();
        for (int i = parentOperation.equals("query coordinator") ? 0
                : 1; i < (parentOperation.equals("query coordinator") ? 1
                        : emittedMaps.length); i++) {
          String targetSlave = slaveIds.get(i);
          if (targetSlave == null) {
            targetSlave = guessSlave(slaveIds, i);
            slaveIds.put(i, targetSlave);
          }
          Map<String, Long> targetOps = receivedMappings.get(targetSlave);
          if (targetOps == null) {
            targetOps = new HashMap<>();
            receivedMappings.put(targetSlave, targetOps);
          }
          Long number = targetOps.get(parentOperation);
          if (number == null) {
            number = 0L;
          }
          number = number + emittedMaps[i];
          targetOps.put(parentOperation, number);
        }
      }
    }

    StringBuilder sb = new StringBuilder();
    for (Entry<String, Map<String, Long>> slaves : receivedMappings.entrySet()) {
      for (Entry<String, Long> operations : slaves.getValue().entrySet()) {
        sb.append("\t").append(slaves.getKey()).append("\t").append(operations.getKey())
                .append("\t").append(operations.getValue());
      }
    }
    writeLine(sb.toString());
    emittedOperationMappings.remove(basicSignature);
  }

  private String guessSlave(Map<Integer, String> slaveIds, int id) {
    if (slaveIds.isEmpty()) {
      String slaveName = "slave" + id;
      return slaveName;
    }
    String[] ids = new String[numberOfChunks + 1];
    int closestId = Integer.MAX_VALUE;
    for (Entry<Integer, String> slaveId : slaveIds.entrySet()) {
      ids[slaveId.getKey()] = slaveId.getValue();
      if ((Math.abs(id - slaveId.getKey()) < Math.abs(id - closestId)) && (slaveId.getKey() > 0)) {
        closestId = slaveId.getKey();
      }
    }
    // extract number of slave
    String[] nameAndPort = ids[closestId].split(Pattern.quote(":"));
    Matcher matcher = Pattern.compile("\\d+$").matcher(nameAndPort[0]);
    if (matcher.find()) {
      String prefix = nameAndPort[0].substring(0, matcher.start());
      String suffix = nameAndPort[0].substring(matcher.start(), matcher.end());
      int slaveId = 0;
      for (char c : suffix.toCharArray()) {
        slaveId *= 10;
        slaveId += Integer.parseUnsignedInt(Character.toString(c));
      }
      slaveId += id - closestId;
      String newSuffix = Integer.toString(slaveId);
      while (newSuffix.length() < suffix.length()) {
        newSuffix = "0" + newSuffix;
      }
      return prefix + newSuffix + (nameAndPort.length > 1 ? nameAndPort[1] : "");
    } else {
      return "slave" + id;
    }
  }

  private String getParentOperation(QuerySignature query, String operation) {
    Map<String, String> parents = parentOperations.get(query);
    if (parents == null) {
      parents = new HashMap<>();
      parentOperations.put(query, parents);
    }
    if (parents.containsKey(operation)) {
      return parents.get(operation);
    } else {
      String[] idAndString = operation.split(Pattern.quote(":"));
      long operationId = Long.parseLong(idAndString[0]);
      Map<Long, String> operations = getOperations(query);
      for (String op : operations.values()) {
        if (isParent(operationId, op)) {
          parents.put(operation, op);
          return op;
        }
      }
      parents.put(operation, null);
      return null;
    }
  }

  private boolean isParent(long operationId, String operation) {
    String[] idAndString = operation.split(Pattern.quote(":"));
    String[] nameAndRest = idAndString[1].split(Pattern.quote("("));
    String paramString = nameAndRest[1].substring(0, nameAndRest[1].length() - 1);
    String[] params = paramString.split(Pattern.quote(","));
    String id = Long.toString(operationId);
    for (String param : params) {
      if (param.equals(id)) {
        return true;
      }
    }
    return false;
  }

}
