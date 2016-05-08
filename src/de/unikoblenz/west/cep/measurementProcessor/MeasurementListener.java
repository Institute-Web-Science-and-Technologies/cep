package de.unikoblenz.west.cep.measurementProcessor;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;

import java.io.File;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public interface MeasurementListener {

  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication);

  public void processMeasurement(String... measurements);

  public void tearDown();

}
