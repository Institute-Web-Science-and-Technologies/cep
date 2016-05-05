package de.unikoblenz.west.cep.queryExecutor;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;

/**
 * A {@link Writer} that counts the number of received results.
 * 
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class ResultNumberWriter extends Writer {

  private long numberOfResults;

  private String outputFile;

  public ResultNumberWriter(String outputFile) {
    super();
    numberOfResults = 0;
    this.outputFile = outputFile;
  }

  @Override
  public void write(char[] cbuf, int off, int len) throws IOException {
    for (int i = off; (i < len) && (i < cbuf.length); i++) {
      if (cbuf[i] == '\n') {
        numberOfResults++;
      }
    }
  }

  @Override
  public void flush() throws IOException {
  }

  @Override
  public void close() throws IOException {
    if (outputFile != null) {
      try (Writer out = new BufferedWriter(
              new OutputStreamWriter(new FileOutputStream(outputFile), "UTF-8"));) {
        out.write(Long.toString(numberOfResults));
      }
      outputFile = null;
    }
  }

}
