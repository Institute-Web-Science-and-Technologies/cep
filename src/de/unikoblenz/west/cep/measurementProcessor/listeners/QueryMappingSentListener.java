package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class QueryMappingSentListener extends QueryListener {

  public QueryMappingSentListener() {
    super();
  }

  public QueryMappingSentListener(CoverStrategyType graphCoverStrategy) {
    super(graphCoverStrategy);
  }

  public QueryMappingSentListener(CoverStrategyType graphCoverStrategy, int nHopReplication) {
    super(graphCoverStrategy, nHopReplication);
  }

  @Override
  public void processMeasurement(String... measurements) {
    super.processMeasurement(measurements);
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case QUERY_OPERATION_SENT_MAPPINGS_TO_SLAVE:
          int firstIndex = 6;
          int lastIndex = measurements.length - 2;
          long[] sentMappings = new long[((lastIndex - firstIndex) + 1) / 2];
          for (int i = firstIndex; i <= (lastIndex - 1); i += 2) {
            sentMappings[Integer.parseInt(measurements[i])] = Long.parseLong(measurements[i + 1]);
          }
          processMappingSent(graphCoverStrategy, nHopReplication, currentQueryId,
                  currentQueryRepetition, treeType, Utilities.getComputerId(measurements),
                  Integer.parseInt(measurements[5]), sentMappings,
                  Integer.parseInt(measurements[measurements.length - 1]));
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processMappingSent(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int currentQueryId, int currentQueryRepetition,
          QueryExecutionTreeType treeType, int slaveId, int taskId, long[] sentMappings,
          int numberOfVariablesPerMapping);

}
