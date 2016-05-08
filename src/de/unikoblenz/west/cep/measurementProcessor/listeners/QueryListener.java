package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.MeasurementListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class QueryListener implements MeasurementListener {

  private final Map<String, Integer> queryIdMap;

  private int nextQueryId;

  private final Map<Integer, Integer> queryRepetition;

  protected CoverStrategyType graphCoverStrategy;

  protected int nHopReplication;

  protected QueryExecutionTreeType treeType;

  protected int currentQueryId;

  protected int currentQueryRepetition;

  public QueryListener() {
    queryIdMap = new HashMap<>();
    queryRepetition = new HashMap<>();
  }

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication) {
    this.graphCoverStrategy = graphCoverStrategy;
    this.nHopReplication = nHopReplication;
  }

  @Override
  public void processMeasurement(String... measurements) {
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case LOAD_GRAPH_START:
          graphCoverStrategy = CoverStrategyType.valueOf(measurements[5]);
          nHopReplication = Integer.parseInt(measurements[6]);
          break;
        case QUERY_COORDINATOR_START:
          String queryString = measurements[6];
          Integer queryId = queryIdMap.get(queryString);
          Integer currentQueryRepetition = null;
          if (queryId == null) {
            queryId = Integer.valueOf(nextQueryId++);
            queryIdMap.put(queryString, queryId);
            currentQueryRepetition = Integer.valueOf(1);
            queryRepetition.put(queryId, currentQueryRepetition);
          } else {
            currentQueryRepetition = queryRepetition.get(queryId) + 1;
            queryRepetition.put(queryId, currentQueryRepetition);
          }
          currentQueryId = queryId;
          this.currentQueryRepetition = currentQueryRepetition;
          processQuery(queryString, queryId);
          break;
        case QUERY_COORDINATOR_PARSE_START:
          treeType = QueryExecutionTreeType.valueOf(measurements[7]);
          break;
        case QUERY_COORDINATOR_END:
          processQueryFinish(currentQueryId);
          currentQueryId = -1;
          currentQueryRepetition = -1;
          treeType = null;
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processQuery(String queryString, int queryId);

  protected abstract void processQueryFinish(int queryId);

}
