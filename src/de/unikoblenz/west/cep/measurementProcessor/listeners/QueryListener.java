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

  private Map<String, String> query2fileName;

  /**
   * maps query file names to number of repetitions
   */
  private final Map<String, Integer> queryRepetition;

  protected CoverStrategyType graphCoverStrategy;

  protected int nHopReplication;

  protected QueryExecutionTreeType treeType;

  protected String currentQueryFileName;

  protected int currentQueryRepetition;

  public QueryListener() {
    queryRepetition = new HashMap<>();
  }

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication) {
    this.graphCoverStrategy = graphCoverStrategy;
    this.nHopReplication = nHopReplication;
    this.query2fileName = query2fileName;
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
          currentQueryFileName = query2fileName.get(queryString);
          if (currentQueryFileName == null) {
            throw new RuntimeException("unknown query " + queryString);
          }
          Integer currentQueryRepetition = queryRepetition.get(currentQueryFileName);
          if (currentQueryRepetition == null) {
            currentQueryRepetition = Integer.valueOf(1);
            queryRepetition.put(currentQueryFileName, currentQueryRepetition);
          } else {
            currentQueryRepetition = currentQueryRepetition + 1;
            queryRepetition.put(currentQueryFileName, currentQueryRepetition);
          }
          this.currentQueryRepetition = currentQueryRepetition;
          break;
        case QUERY_COORDINATOR_PARSE_START:
          treeType = QueryExecutionTreeType.valueOf(measurements[7]);
          break;
        case QUERY_COORDINATOR_END:
          processQueryFinish(currentQueryFileName);
          currentQueryFileName = null;
          currentQueryRepetition = -1;
          treeType = null;
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected abstract void processQueryFinish(String query);

}
