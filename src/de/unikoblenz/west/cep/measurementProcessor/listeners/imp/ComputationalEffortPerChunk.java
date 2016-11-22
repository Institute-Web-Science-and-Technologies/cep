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

import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;

import java.io.File;
import java.util.Arrays;

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
    Arrays.sort(numberOfComparisonsPerSlave);
    long[] newComps = new long[numberOfComparisonsPerSlave.length];
    for (int i = numberOfComparisonsPerSlave.length - 1; i >= 0; i--) {
      newComps[(newComps.length - 1) - i] = numberOfComparisonsPerSlave[i];
    }
    numberOfComparisonsPerSlave = newComps;

    StringBuilder sb = new StringBuilder();
    for (long value : numberOfComparisonsPerSlave) {
      sb.append("\t").append(value);
    }
    writeLine(sb.toString());
    numberOfComparisonsPerSlave = null;
  }

}
