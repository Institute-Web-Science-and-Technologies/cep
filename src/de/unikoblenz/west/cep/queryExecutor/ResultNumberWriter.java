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
