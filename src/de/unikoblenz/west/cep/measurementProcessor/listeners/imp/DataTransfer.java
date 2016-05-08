package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryMappingSentListener;

import java.io.File;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class DataTransfer extends QueryMappingSentListener {

  private long totalDataTransfer;

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "dataTransfer.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\tdataTransfer";
  }

  @Override
  protected void processMappingSent(CoverStrategyType graphCoverStrategy, int nHopReplication,
          String query, int currentQueryRepetition, QueryExecutionTreeType treeType, int slaveId,
          int taskId, long[] sentMappings, int numberOfVariablesPerMapping) {
    if (numberOfVariablesPerMapping == 0) {
      numberOfVariablesPerMapping = 1;
    }
    for (int i = 1; i < sentMappings.length; i++) {
      // ignore master=0
      if (i == slaveId) {
        continue;
      }
      totalDataTransfer += sentMappings[i] * numberOfVariablesPerMapping;
    }
  }

  @Override
  protected void processQueryFinish(String query, int currentQueryRepetition) {
    if (currentQueryRepetition == 1) {
      writeLine("\t" + totalDataTransfer);
      totalDataTransfer = 0;
    }
  }

}
