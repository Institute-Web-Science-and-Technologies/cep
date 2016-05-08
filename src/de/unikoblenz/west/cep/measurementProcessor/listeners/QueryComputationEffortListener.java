package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class QueryComputationEffortListener extends QueryListener {

  public QueryComputationEffortListener() {
    super();
  }

  public QueryComputationEffortListener(CoverStrategyType graphCoverStrategy) {
    super(graphCoverStrategy);
  }

  public QueryComputationEffortListener(CoverStrategyType graphCoverStrategy, int nHopReplication) {
    super(graphCoverStrategy, nHopReplication);
  }

  @Override
  public void processMeasurement(String... measurements) {
    super.processMeasurement(measurements);
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case QUERY_OPERATION_JOIN_NUMBER_OF_COMPARISONS:
          processComputationEffort(graphCoverStrategy, nHopReplication, currentQueryId,
                  currentQueryRepetition, treeType, Utilities.getComputerId(measurements),
                  Integer.parseInt(measurements[5]), Long.parseLong(measurements[6]));
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processComputationEffort(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int currentQueryId, int currentQueryRepetition,
          QueryExecutionTreeType treeType, int slaveId, int taskId, long numberOfComparisons);

}
