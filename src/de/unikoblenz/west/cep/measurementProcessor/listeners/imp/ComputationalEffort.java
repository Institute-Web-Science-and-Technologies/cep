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
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryComputationEffortListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.io.File;
import java.util.Arrays;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class ComputationalEffort extends QueryComputationEffortListener {

  protected long[] numberOfComparisonsPerSlave;

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "computationalEffort.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine()
            + "\ttotalComputationalEffort\tentropy\tstandardDeviation\tGiniCoefficient";
  }

  @Override
  protected void processComputationEffort(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, int slaveId, int taskId,
          long numberOfComparisons) {
    while (slaveId > numberOfChunks) {
      slaveId -= numberOfChunks;
    }
    slaveId -= 1;
    if (numberOfComparisonsPerSlave == null) {
      numberOfComparisonsPerSlave = new long[slaveId + 1];
    } else if (numberOfComparisonsPerSlave.length <= slaveId) {
      numberOfComparisonsPerSlave = Arrays.copyOf(numberOfComparisonsPerSlave, slaveId + 1);
    }
    numberOfComparisonsPerSlave[slaveId] += numberOfComparisons;
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    if (numberOfComparisonsPerSlave == null) {
      return;
    }
    long totalNumberOfcomputations = 0;
    for (long value : numberOfComparisonsPerSlave) {
      totalNumberOfcomputations += value;
    }
    writeLine("\t" + totalNumberOfcomputations + "\t"
            + Utilities.computeEntropy(numberOfComparisonsPerSlave, totalNumberOfcomputations)
            + "\t"
            + Utilities.computeStandardDeviation(numberOfComparisonsPerSlave,
                    totalNumberOfcomputations)
            + "\t" + Utilities.computeGiniCoefficient(numberOfComparisonsPerSlave));
    numberOfComparisonsPerSlave = null;
  }

}
