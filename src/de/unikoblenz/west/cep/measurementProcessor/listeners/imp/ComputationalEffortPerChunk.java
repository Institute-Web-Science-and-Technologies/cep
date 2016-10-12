package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;

import java.io.File;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class ComputationalEffortPerChunk extends ComputationalEffort {

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(
            outputDirectory.getAbsolutePath() + File.separator + "computationalEffortPerChunk.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\tcomputationalEffortPerChunk*";
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    if (numberOfComparisonsPerSlave == null) {
      return;
    }
    StringBuilder sb = new StringBuilder();
    for (long value : numberOfComparisonsPerSlave) {
      sb.append("\t").append(value);
    }
    writeLine(sb.toString());
    numberOfComparisonsPerSlave = null;
  }

}
