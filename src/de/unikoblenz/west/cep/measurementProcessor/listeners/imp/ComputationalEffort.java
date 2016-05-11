package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryComputationEffortListener;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.io.File;
import java.util.Arrays;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class ComputationalEffort extends QueryComputationEffortListener {

  private long[] numberOfComparisonsPerSlave;

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "computationalEffort.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\ttotalComputationalEffort\tentropy\tstandardDeviation";
  }

  @Override
  protected void processComputationEffort(CoverStrategyType graphCoverStrategy, int nHopReplication,
          ExtendedQuerySignature query, int slaveId, int taskId, long numberOfComparisons) {
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
            + "\t" + Utilities.computeStandardDeviation(numberOfComparisonsPerSlave,
                    totalNumberOfcomputations));
    numberOfComparisonsPerSlave = null;
  }

}
