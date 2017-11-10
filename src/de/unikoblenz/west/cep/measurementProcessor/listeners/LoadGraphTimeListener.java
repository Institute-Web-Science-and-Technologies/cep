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

import java.io.File;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class LoadGraphTimeListener implements MeasurementListener {

  private CoverStrategyType graphCoverStrategy;

  private int nHopReplication;

  private int numberOfChunks;

  private int numberOfTriples;

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication, int repetitions,
          int numberOfChunks, int numberOfTriples) {
    this.numberOfChunks = numberOfChunks;
    this.numberOfTriples = numberOfTriples;
  }

  @Override
  public void processMeasurement(String... measurements) {
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case LOAD_GRAPH_START:
          initialize(measurements);
          break;
        case LOAD_GRAPH_INITIAL_ENCODING_START:
          processInitialDictionaryEncodingStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_INITIAL_ENCODING_END:
          processInitialDictionaryEncodingEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_COVER_CREATION_START:
          processGraphCoverCreationStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_COVER_CREATION_END:
          processGraphCoverCreationEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_FINAL_ENCODING_START:
          processFinalDictionaryEncodingStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_FINAL_ENCODING_END:
          processFinalDictionaryEncodingEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_NHOP_REPLICATION_START:
          processNHopReplicationStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_NHOP_REPLICATION_END:
          processNHopReplicationEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_COLLECTING_STATISTICS_START:
          processStatisticCollectionStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_COLLECTING_STATISTICS_END:
          processStatisticCollectionEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_ADJUSTING_OWNERSHIP_START:
          processOwnershipAdjustmentStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_ADJUSTING_OWNERSHIP_END:
          processOwnershipAdjustmentEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_FILE_TRANSFER_TO_SLAVES_START:
          processChunkTransferToSlavesStart(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Utilities.getComputerId(measurements),
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_FILE_TRANSFER_TO_SLAVES_END:
          processChunkTransferToSlavesEnd(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples, Utilities.getComputerId(measurements),
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_STORING_TRIPLES_START:
          processIndexingStart(graphCoverStrategy, nHopReplication, numberOfChunks, numberOfTriples,
                  Utilities.getComputerId(measurements), Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_STORING_TRIPLES_END:
          processIndexingEnd(graphCoverStrategy, nHopReplication, numberOfChunks, numberOfTriples,
                  Utilities.getComputerId(measurements), Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_FINISHED:
          processLoadingFinished(graphCoverStrategy, nHopReplication, numberOfChunks,
                  numberOfTriples);
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected void initialize(String[] measurements) {
    graphCoverStrategy = CoverStrategyType.valueOf(measurements[5]);
    nHopReplication = Integer.parseInt(measurements[6]);
  }

  protected abstract void processInitialDictionaryEncodingStart(
          CoverStrategyType graphCoverStrategy, int nHopReplication, int numberOfChunks,
          int numberOfTriples, long startTime);

  protected abstract void processInitialDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime);

  protected abstract void processGraphCoverCreationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime);

  protected abstract void processGraphCoverCreationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime);

  protected abstract void processFinalDictionaryEncodingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime);

  protected abstract void processFinalDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime);

  protected abstract void processNHopReplicationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime);

  protected abstract void processNHopReplicationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime);

  protected abstract void processStatisticCollectionStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime);

  protected abstract void processStatisticCollectionEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime);

  protected abstract void processOwnershipAdjustmentStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime);

  protected abstract void processOwnershipAdjustmentEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime);

  protected abstract void processChunkTransferToSlavesStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, int slave, long startTime);

  protected abstract void processChunkTransferToSlavesEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, int slave, long endTime);

  protected abstract void processIndexingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, int slave, long startTime);

  protected abstract void processIndexingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, int slave, long endTime);

  protected abstract void processLoadingFinished(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples);

  @Override
  public void clear() {
  }

}
