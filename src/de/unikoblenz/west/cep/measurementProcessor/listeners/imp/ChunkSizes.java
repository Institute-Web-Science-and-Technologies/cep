package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.GraphStatisticsListener;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.Arrays;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class ChunkSizes extends GraphStatisticsListener {

  private Writer output;

  private long[] chunkSizes;

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication, int repetitions) {
    File outputFile = new File(
            outputDirectory.getAbsolutePath() + File.separator + "chunkSizes.csv");
    boolean existsOutputFile = outputFile.exists();
    try {
      output = new BufferedWriter(
              new OutputStreamWriter(new FileOutputStream(outputFile, true), "UTF-8"));
      if (!existsOutputFile) {
        output.write("cover\tn-hop\tchunkSizes*");
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  protected void processTotalGraphSizeBeforeReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long totalGraphSize) {
  }

  @Override
  protected void processGraphChunkSizesBeforeReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long... graphChunkSizes) {
    processGraphChunkSizesAfterReplication(graphCoverStrategy, nHopReplication, graphChunkSizes);
  }

  @Override
  protected void processTotalGraphSizeAfterReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long totalGraphSize) {
  }

  @Override
  protected void processGraphChunkSizesAfterReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long... graphChunkSizes) {
    chunkSizes = graphChunkSizes;
    Arrays.sort(chunkSizes);
    long[] revers = new long[chunkSizes.length];
    for (int i = chunkSizes.length - 1, j = 0; i >= 0; i--, j++) {
      revers[j] = chunkSizes[i];
    }
    chunkSizes = revers;
  }

  @Override
  protected void processLoadingFinished(CoverStrategyType graphCoverStrategy, int nHopReplication) {
    try {
      StringBuilder sb = new StringBuilder();
      for (long value : chunkSizes) {
        sb.append("\t").append(value);
      }
      output.write("\n" + graphCoverStrategy + "\t" + nHopReplication + sb.toString());
    } catch (IOException e) {
      throw new RuntimeException(e);
    }

  }

  @Override
  public void tearDown() {
    try {
      if (output != null) {
        output.close();
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

}
