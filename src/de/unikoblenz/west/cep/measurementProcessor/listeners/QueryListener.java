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

  protected int currentQueryId;

  private Writer output;

  protected int numberOfRepetitions;

  public QueryListener() {
    queryRepetition = new HashMap<>();
  }

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication, int repetitions) {
    this.graphCoverStrategy = graphCoverStrategy;
    this.nHopReplication = nHopReplication;
    numberOfRepetitions = repetitions;
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
          currentQueryId = Integer.parseInt(measurements[5]);
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

  private void performFinishTasks() {
    if (currentQueryFileName != null) {
      processQueryFinish(new ExtendedQuerySignature(currentQueryId, currentQueryFileName, treeType,
              currentQueryRepetition));
    }
    currentQueryFileName = null;
    currentQueryRepetition = -1;
    treeType = null;
  }

  protected abstract void processQueryFinish(ExtendedQuerySignature query);

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
