package de.unikoblenz.west.cep.measurementProcessor;

import java.io.File;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public interface MeasurmentListener {

  public void setUp(File outputDirectory);

  public void processMeasurement(String... measurements);

  public void tearDown();

}
