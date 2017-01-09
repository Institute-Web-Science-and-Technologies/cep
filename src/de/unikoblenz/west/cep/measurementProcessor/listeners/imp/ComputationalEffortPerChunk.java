/*
 * This file is part of CEP.
 *
 * CEP is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * CEP is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Leser General Public License
 * along with CEP.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright 2016 Daniel Janke
 */
package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class ComputationalEffortPerChunk extends ComputationalEffort {

  private final Map<QuerySignature, String[]> allSlaveIds;

  public ComputationalEffortPerChunk() {
    allSlaveIds = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(
            outputDirectory.getAbsolutePath() + File.separator + "computationalEffortPerChunk.csv");
  }

  @Override
  protected String getHeadLine() {
    return "cover\tnumberOfChunks\tnhop\ttreeType\tqueryFile\tjoinPattern\tnumberOfJoins\tnumberOfDataSources\tselectivity"
            + "\t(slaveId\tcomputationalEffortPerChunk)*";
  }

  @Override
  protected void processComputationEffort(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, int slaveId, String slaveName,
          int taskId, long numberOfComparisons) {
    super.processComputationEffort(graphCoverStrategy, nHopReplication, numberOfChunks, query,
            slaveId, slaveName, taskId, numberOfComparisons);
    while (slaveId > numberOfChunks) {
      slaveId -= numberOfChunks;
    }
    slaveId -= 1;
    String[] slaveIds = allSlaveIds.get(query.getBasicSignature());
    if (slaveIds == null) {
      slaveIds = new String[slaveId + 1];
      allSlaveIds.put(query.getBasicSignature(), slaveIds);
    } else if (slaveIds.length <= slaveId) {
      slaveIds = Arrays.copyOf(slaveIds, slaveId + 1);
      allSlaveIds.put(query.getBasicSignature(), slaveIds);
    }
    slaveIds[slaveId] = slaveName;
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query, int minRepitition) {
    QuerySignature basicSignature = query.getBasicSignature();
    long[][] numberOfComparisonsPerSlave = numberOfComparisonsPerSlaves.get(basicSignature);
    String[] slaveIds = allSlaveIds.get(basicSignature);
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < numberOfComparisonsPerSlave[minRepitition].length; i++) {
      sb.append("\t").append(slaveIds[i]).append("\t")
              .append(numberOfComparisonsPerSlave[minRepitition][i]);
    }
    writeLine(sb.toString());
  }

}
