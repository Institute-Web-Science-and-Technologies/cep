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
package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.util.Arrays;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class QueryPackageSentListener extends QueryMinListener {

  @Override
  public void processMeasurement(String... measurements) {
    super.processMeasurement(measurements);
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case SLAVE_SENT_MAPPING_BATCHES_TO_SLAVE:
          assert treeType != null : Arrays.toString(measurements);
          int firstIndex = 5;
          long[] sentMappings = new long[numberOfChunks];
          for (int i = firstIndex; (i - firstIndex) < sentMappings.length; i++) {
            sentMappings[i - firstIndex] = Long.parseLong(measurements[i]);
          }
          processPackageSent(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[4]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  Utilities.getComputerId(measurements), sentMappings);
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processPackageSent(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature query, int slaveId,
          long[] sentPackages);

}
