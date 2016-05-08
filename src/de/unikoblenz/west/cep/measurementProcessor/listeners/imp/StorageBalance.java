package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.GraphStatisticsListener;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class StorageBalance extends GraphStatisticsListener {

  private Writer output;

  private long originalGraphSize;

  private long totalGraphCoverSize;

  private long[] chunkSizes;

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication) {
    File outputFile = new File(
            outputDirectory.getAbsolutePath() + File.separator + "storageBalance.csv");
    boolean existsOutputFile = outputFile.exists();
    try {
      output = new BufferedWriter(
              new OutputStreamWriter(new FileOutputStream(outputFile, true), "UTF-8"));
      if (!existsOutputFile) {
        output.write("cover\tn-hop\tredundancy\tentropy\tstandardDeviation");
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  protected void processTotalGraphSizeBeforeReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long totalGraphSize) {
    originalGraphSize = totalGraphSize;
    totalGraphCoverSize = totalGraphSize;
  }

  @Override
  protected void processGraphChunkSizesBeforeReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long... graphChunkSizes) {
    chunkSizes = graphChunkSizes;
  }

  @Override
  protected void processTotalGraphSizeAfterReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long totalGraphSize) {
    totalGraphCoverSize = totalGraphSize;
  }

  @Override
  protected void processGraphChunkSizesAfterReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long... graphChunkSizes) {
    chunkSizes = graphChunkSizes;
  }

  @Override
  protected void processLoadingFinished(CoverStrategyType graphCoverStrategy, int nHopReplication) {
    try {
      output.write("\n" + graphCoverStrategy + "\t" + nHopReplication + "\t"
              + computeRedundancy(totalGraphCoverSize, originalGraphSize) + "\t"
              + computeEntropy(chunkSizes, totalGraphCoverSize) + "\t"
              + computeStandardDeviation(chunkSizes, totalGraphCoverSize));
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  private double computeRedundancy(long totalGraphCoverSize, long originalGraphSize) {
    return totalGraphCoverSize / (double) originalGraphSize;
  }

  private double computeEntropy(long[] chunkSizes, long totalGraphCoverSize) {
    double result = 0;
    double log = Math.log(2);
    for (long chunkSize : chunkSizes) {
      double factor = chunkSize / (double) totalGraphCoverSize;
      result += factor * (Math.log(factor) / log);
    }
    return -result;
  }

  private double computeStandardDeviation(long[] chunkSizes, long totalGraphCoverSize) {
    double factor = totalGraphCoverSize / (double) chunkSizes.length;
    double summ = 0;
    for (long chunkSize : chunkSizes) {
      double difference = chunkSize - factor;
      summ += difference * difference;
    }
    return Math.sqrt(summ / chunkSizes.length);
  }

  @Override
  public void tearDown() {
    try {
      output.close();
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

}
