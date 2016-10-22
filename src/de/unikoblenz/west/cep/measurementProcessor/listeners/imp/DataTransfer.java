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

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
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
          ExtendedQuerySignature query, int slaveId, int taskId, long[] sentMappings,
          int numberOfVariablesPerMapping) {
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
  protected void processQueryFinish(ExtendedQuerySignature query) {
    if (currentQueryRepetition == 1) {
      writeLine("\t" + totalDataTransfer);
      totalDataTransfer = 0;
    }
  }

}
