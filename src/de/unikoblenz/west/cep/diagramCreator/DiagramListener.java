package de.unikoblenz.west.cep.diagramCreator;

import java.io.Closeable;
import java.io.File;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public interface DiagramListener extends Closeable {

  public void setUp(OutputFormat format, File outputDir);

  public void process(String[] parts);

  public void tearDown();

  @Override
  public void close();

}
