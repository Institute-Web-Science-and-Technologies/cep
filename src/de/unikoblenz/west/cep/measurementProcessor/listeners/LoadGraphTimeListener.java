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
          graphCoverStrategy = CoverStrategyType.valueOf(measurements[5]);
          nHopReplication = Integer.parseInt(measurements[6]);
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
        case LOAD_GRAPH_NHOP_REPLICATION_END:
          processGraphCoverCreationEnd(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_ENCODING_START:
          processDictionaryEncodingStart(graphCoverStrategy, nHopReplication,
                  Long.parseLong(measurements[4]));
          break;
        case LOAD_GRAPH_ENCODING_END:
          processDictionaryEncodingEnd(graphCoverStrategy, nHopReplication,
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

  protected abstract void processGraphCoverCreationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime);

  protected abstract void processGraphCoverCreationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime);

  protected abstract void processDictionaryEncodingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime);

  protected abstract void processDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
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
