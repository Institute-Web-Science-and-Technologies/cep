package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class QueryTimesListener extends QueryListener {

  private long queryStartTime;

  private boolean hasProcessedQueryResults;

  @Override
  public void processMeasurement(String... measurements) {
    super.processMeasurement(measurements);
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case QUERY_MESSAGE_RECEIPTION:
          queryStartTime = Long.parseLong(measurements[4]);
          break;
        case QUERY_COORDINATOR_SEND_QUERY_RESULTS_TO_CLIENT:
          if (!hasProcessedQueryResults) {
            processQueryStart(graphCoverStrategy, nHopReplication,
                    new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                            currentQueryFileName, treeType, currentQueryRepetition),
                    queryStartTime);
          }
          processQueryResult(graphCoverStrategy, nHopReplication,
                  new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                          currentQueryFileName, treeType, currentQueryRepetition),
                  Long.parseLong(measurements[4]), Long.parseLong(measurements[6]),
                  Long.parseLong(measurements[7]));
          hasProcessedQueryResults = true;
          break;
        case QUERY_COORDINATOR_END:
          if (!hasProcessedQueryResults) {
            processQueryStart(graphCoverStrategy, nHopReplication,
                    new ExtendedQuerySignature(Integer.parseInt(measurements[5]),
                            currentQueryFileName, treeType, currentQueryRepetition),
                    queryStartTime);
          }
          hasProcessedQueryResults = false;
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processQueryStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, ExtendedQuerySignature query, long queryStartTime);

  protected abstract void processQueryResult(CoverStrategyType graphCoverStrategy,
          int nHopReplication, ExtendedQuerySignature query, long queryResultSentTime,
          long firstResultNumber, long lastResultNumber);

}
