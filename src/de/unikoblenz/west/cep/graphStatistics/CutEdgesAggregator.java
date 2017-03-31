package de.unikoblenz.west.cep.graphStatistics;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.LineNumberReader;
import java.io.Writer;
import java.util.regex.Pattern;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class CutEdgesAggregator implements AutoCloseable {

  private Writer output;

  public void initialize(File outputFile) throws IOException {
    if ((outputFile.getParentFile() != null) && !outputFile.getParentFile().exists()) {
      outputFile.getParentFile().mkdirs();
    }
    output = new BufferedWriter(new FileWriter(outputFile));
    output.write("COVER_STRATEGY\tCHUNK_SIZE\tDATASET_SIZE\tCUT_EDGES");
  }

  public void processFile(File inputFile, CoverStrategyType cover, int numberOfChunks,
          long datasteSize) throws FileNotFoundException, IOException {
    long numberOfCutEdges = 0;
    try (LineNumberReader input = new LineNumberReader(
            new BufferedReader(new FileReader(inputFile)));) {
      for (String line = input.readLine(); line != null; line = input.readLine()) {
        String[] columns = line.split(Pattern.quote("\t"));
        if (!columns[0].matches("\\d+")) {
          continue;
        }
        numberOfCutEdges += Long.parseLong(columns[columns.length - 2]);
      }
    }
    output.write(
            "\n" + cover + "\t" + numberOfChunks + "\t" + datasteSize + "\t" + numberOfCutEdges);
  }

  @Override
  public void close() throws IOException {
    if (output != null) {
      output.close();
    }
  }

}
