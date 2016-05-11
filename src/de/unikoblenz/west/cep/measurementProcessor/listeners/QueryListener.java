package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;
import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.MeasurementListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

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

  private Writer output;

  public QueryListener() {
    queryRepetition = new HashMap<>();
  }

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication) {
    this.graphCoverStrategy = graphCoverStrategy;
    this.nHopReplication = nHopReplication;
    this.query2fileName = query2fileName;
    File outputFile = getOutputFile(outputDirectory);
    boolean existsOutputFile = outputFile.exists();
    try {
      output = new BufferedWriter(
              new OutputStreamWriter(new FileOutputStream(outputFile, true), "UTF-8"));
      if (!existsOutputFile) {
        output.write(getHeadLine());
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  protected String getHeadLine() {
    return "cover\tnhop\ttreeType\tqueryFile\tjoinPattern\tnumberOfJoins\tnumberOfDataSources\tselectivity";
  }

  protected abstract File getOutputFile(File outputDirectory);

  @Override
  public void processMeasurement(String... measurements) {
    MeasurementType measurementType = Utilities.getMeasurementType(measurements);
    if (measurementType != null) {
      switch (measurementType) {
        case QUERY_COORDINATOR_START:
          performFinishTasks();
          String queryString = measurements[6];
          currentQueryFileName = query2fileName.get(queryString);
          if (currentQueryFileName == null) {
            throw new RuntimeException("unknown query " + queryString);
          }
          break;
        case QUERY_COORDINATOR_PARSE_START:
          treeType = QueryExecutionTreeType.valueOf(measurements[7]);
          Integer currentQueryRepetition = queryRepetition
                  .get(currentQueryFileName + "\n" + treeType);
          if (currentQueryRepetition == null) {
            currentQueryRepetition = Integer.valueOf(1);
            queryRepetition.put(currentQueryFileName + "\n" + treeType, currentQueryRepetition);
          } else {
            currentQueryRepetition = currentQueryRepetition + 1;
            queryRepetition.put(currentQueryFileName + "\n" + treeType, currentQueryRepetition);
          }
          this.currentQueryRepetition = currentQueryRepetition;
          break;
        default:
          // all other types are not required
          break;
      }
    }
  }

  protected void performFinishTasks() {
    if (currentQueryFileName != null) {
      processQueryFinish(currentQueryFileName, currentQueryRepetition);
    }
    currentQueryFileName = null;
    currentQueryRepetition = -1;
    treeType = null;
  }

  protected abstract void processQueryFinish(String query, int currentQueryRepetition);

  protected void writeLine(String line) {
    if (!line.startsWith("\t")) {
      line = "\t" + line;
    }
    String[] parts = currentQueryFileName.split(Pattern.quote("-"));
    try {
      output.write("\n" + graphCoverStrategy + "\t" + nHopReplication + "\t" + treeType + "\t"
              + currentQueryFileName + "\t" + parts[1] + "\t" + parts[2] + "\t" + parts[3] + "\t"
              + parts[4] + line);
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public void tearDown() {
    performFinishTasks();
    try {
      if (output != null) {
        output.close();
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

}
