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
public abstract class QueryMappingSentListener extends QueryMinListener {

  @Override
  public void processMeasurement(String... measurements) {
    super.processMeasurement(measurements);
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case QUERY_OPERATION_SENT_MAPPINGS_TO_SLAVE:
          assert treeType != null : Arrays.toString(measurements);
          int firstIndex = 6;
          int lastIndex = measurements.length - 2;
          long[] sentMappings = new long[(((lastIndex - firstIndex) + 1) / 2) + 2];
          for (int i = firstIndex; i <= (lastIndex - 1); i += 2) {
            sentMappings[Integer.parseInt(measurements[i])] = Long.parseLong(measurements[i + 1]);
          }
          processMappingSent(graphCoverStrategy, nHopReplication, numberOfChunks,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[4]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  Utilities.getComputerId(measurements), Integer.parseInt(measurements[5]),
                  sentMappings, Integer.parseInt(measurements[measurements.length - 1]));
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processMappingSent(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature query, int slaveId,
          int taskId, long[] sentMappings, int numberOfVariablesPerMapping);

}
