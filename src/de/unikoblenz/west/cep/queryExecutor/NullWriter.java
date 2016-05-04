package de.unikoblenz.west.cep.queryExecutor;

import java.io.IOException;
import java.io.Writer;

/**
 * A {@link Writer} that discards all output.
 * 
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class NullWriter extends Writer {

  @Override
  public void write(char[] cbuf, int off, int len) throws IOException {
  }

  @Override
  public void flush() throws IOException {
  }

  @Override
  public void close() throws IOException {
  }

}
