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
import de.unikoblenz.west.cep.measurementProcessor.MeasurementListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class GraphStatisticsListener implements MeasurementListener {

  private CoverStrategyType graphCoverStrategy;

  private int nHopReplication;

  @Override
  public void processMeasurement(String... measurements) {
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case LOAD_GRAPH_START:
          graphCoverStrategy = CoverStrategyType.valueOf(measurements[5]);
          nHopReplication = Integer.parseInt(measurements[6]);
          break;
        case TOTAL_GRAPH_SIZE:
          processTotalGraphSizeBeforeReplication(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case INITIAL_CHUNK_SIZES:
          long[] graphChunkSizes = new long[measurements.length - 4];
          for (int i = 0; i < graphChunkSizes.length; i++) {
            graphChunkSizes[i] = Long.parseLong(measurements[4 + i]);
          }
          processGraphChunkSizesBeforeReplication(graphCoverStrategy, nHopReplication,
                  graphChunkSizes);
          break;
        case LOAD_GRAPH_REPLICATED_CHUNK_SIZES:
          long totalGraphSize = 0;
          graphChunkSizes = new long[measurements.length - 4];
          for (int i = 0; i < graphChunkSizes.length; i++) {
            graphChunkSizes[i] = Long.parseLong(measurements[4 + i]);
            totalGraphSize += graphChunkSizes[i];
          }
          processTotalGraphSizeAfterReplication(graphCoverStrategy, nHopReplication,
                  totalGraphSize);
          processGraphChunkSizesAfterReplication(graphCoverStrategy, nHopReplication,
                  graphChunkSizes);
          break;
        case LOAD_GRAPH_FINISHED:
          processLoadingFinished(graphCoverStrategy, nHopReplication);
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processTotalGraphSizeBeforeReplication(
          CoverStrategyType graphCoverStrategy, int nHopReplication, long totalGraphSize);

  protected abstract void processGraphChunkSizesBeforeReplication(
          CoverStrategyType graphCoverStrategy, int nHopReplication, long... graphChunkSizes);

  protected abstract void processTotalGraphSizeAfterReplication(
          CoverStrategyType graphCoverStrategy, int nHopReplication, long totalGraphSize);

  protected abstract void processGraphChunkSizesAfterReplication(
          CoverStrategyType graphCoverStrategy, int nHopReplication, long... graphChunkSizes);

  protected abstract void processLoadingFinished(CoverStrategyType graphCoverStrategy,
          int nHopReplication);

  @Override
  public void clear() {
  }

}
