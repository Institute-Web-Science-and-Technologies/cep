package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.MeasurementListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class LoadGraphTimeListener implements MeasurementListener {

  private CoverStrategyType graphCoverStrategy;

  private int nHopReplication;

  @Override
  public void processMeasurement(String... measurements) {
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case LOAD_GRAPH_START:
          initialize(measurements);
          break;
        case LOAD_GRAPH_INITIAL_ENCODING_START:
          processInitialDictionaryEncodingStart(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_INITIAL_ENCODING_END:
          processInitialDictionaryEncodingEnd(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_COVER_CREATION_START:
          processGraphCoverCreationStart(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_COVER_CREATION_END:
          if (nHopReplication == 0) {
            processGraphCoverCreationEnd(graphCoverStrategy, nHopReplication,
                    Long.parseLong(measurements[4]));
          }
          break;
        case LOAD_GRAPH_FINAL_ENCODING_START:
          processFinalDictionaryEncodingStart(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_FINAL_ENCODING_END:
          processFinalDictionaryEncodingEnd(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_NHOP_REPLICATION_START:
          processNHopReplicationStart(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_NHOP_REPLICATION_END:
          processNHopReplicationEnd(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_COLLECTING_STATISTICS_START:
          processStatisticCollectionStart(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_COLLECTING_STATISTICS_END:
          processStatisticCollectionEnd(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_ADJUSTING_OWNERSHIP_START:
          processOwnershipAdjustmentStart(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_ADJUSTING_OWNERSHIP_END:
          processOwnershipAdjustmentEnd(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_FILE_TRANSFER_TO_SLAVES_START:
          processChunkTransferToSlavesStart(graphCoverStrategy, nHopReplication,
                  Utilities.getComputerId(measurements), Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_FILE_TRANSFER_TO_SLAVES_END:
          processChunkTransferToSlavesEnd(graphCoverStrategy, nHopReplication,
                  Utilities.getComputerId(measurements), Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_STORING_TRIPLES_START:
          processIndexingStart(graphCoverStrategy, nHopReplication,
                  Utilities.getComputerId(measurements), Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_STORING_TRIPLES_END:
          processIndexingEnd(graphCoverStrategy, nHopReplication,
                  Utilities.getComputerId(measurements), Long.parseLong(measurements[4]));
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

  protected void initialize(String[] measurements) {
    graphCoverStrategy = CoverStrategyType.valueOf(measurements[5]);
    nHopReplication = Integer.parseInt(measurements[6]);
  }

  protected abstract void processInitialDictionaryEncodingStart(
          CoverStrategyType graphCoverStrategy, int nHopReplication, long startTime);

  protected abstract void processInitialDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime);

  protected abstract void processGraphCoverCreationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime);

  protected abstract void processGraphCoverCreationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime);

  protected abstract void processFinalDictionaryEncodingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime);

  protected abstract void processFinalDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime);

  protected abstract void processNHopReplicationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime);

  protected abstract void processNHopReplicationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime);

  protected abstract void processStatisticCollectionStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime);

  protected abstract void processStatisticCollectionEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime);

  protected abstract void processOwnershipAdjustmentStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime);

  protected abstract void processOwnershipAdjustmentEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime);

  protected abstract void processChunkTransferToSlavesStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int slave, long startTime);

  protected abstract void processChunkTransferToSlavesEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int slave, long endTime);

  protected abstract void processIndexingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int slave, long startTime);

  protected abstract void processIndexingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int slave, long endTime);

  protected abstract void processLoadingFinished(CoverStrategyType graphCoverStrategy,
          int nHopReplication);

}
