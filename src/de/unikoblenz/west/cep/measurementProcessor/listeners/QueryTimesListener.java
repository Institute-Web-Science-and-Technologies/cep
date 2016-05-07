package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.MeasurmentListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public abstract class QueryTimesListener implements MeasurmentListener {

  private final Map<String, Integer> queryIdMap;

  private int nextQueryId;

  private final Map<Integer, Integer> queryRepetition;

  private CoverStrategyType graphCoverStrategy;

  private int nHopReplication;

  private QueryExecutionTreeType treeType;

  private int currentQueryId;

  private int currentQueryRepetition;

  private long queryStartTime;

  private boolean hasProcessedQueryResults;

  public QueryTimesListener() {
    queryIdMap = new HashMap<>();
    queryRepetition = new HashMap<>();
  }

  public QueryTimesListener(CoverStrategyType graphCoverStrategy) {
    this(graphCoverStrategy, 0);
  }

  public QueryTimesListener(CoverStrategyType graphCoverStrategy, int nHopReplication) {
    this();
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
        case QUERY_MESSAGE_RECEIPTION:
          queryStartTime = Long.parseLong(measurements[4]);
          break;
        case QUERY_COORDINATOR_SEND_QUERY_RESULTS_TO_CLIENT:
          if (!hasProcessedQueryResults) {
            processQueryStart(graphCoverStrategy, nHopReplication, currentQueryId,
                    this.currentQueryRepetition, treeType, queryStartTime);
          }
          processQueryResult(graphCoverStrategy, nHopReplication, currentQueryId,
                  this.currentQueryRepetition, treeType, Long.parseLong(measurements[4]),
                  Long.parseLong(measurements[6]), Long.parseLong(measurements[7]));
          hasProcessedQueryResults = true;
          break;
        case QUERY_COORDINATOR_END:
          if (!hasProcessedQueryResults) {
            processQueryStart(graphCoverStrategy, nHopReplication, currentQueryId,
                    this.currentQueryRepetition, treeType, queryStartTime);
          }
          processQueryStart(graphCoverStrategy, nHopReplication, currentQueryId,
                  this.currentQueryRepetition, treeType, Long.parseLong(measurements[4]));
          currentQueryId = -1;
          currentQueryRepetition = -1;
          queryStartTime = -1;
          treeType = null;
          hasProcessedQueryResults = false;
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processQuery(String queryString, int queryId);

  protected abstract void processQueryStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int currentQueryId, int currentQueryRepetition,
          QueryExecutionTreeType treeType, long queryStartTime);

  protected abstract void processQueryResult(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int currentQueryId, int currentQueryRepetition,
          QueryExecutionTreeType treeType, long queryResultSentTime, long firstResultNumber,
          long lastResultNumber);

  protected abstract void processQueryEnd(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int currentQueryId, int currentQueryRepetition, QueryExecutionTreeType treeType,
          long queryEndTime);

}
