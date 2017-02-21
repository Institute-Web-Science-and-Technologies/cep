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
public class ChunkSizes extends GraphStatisticsListener {

  private Writer output;

  private long[] chunkSizes;

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication, int repetitions,
          int numberOfChunks, int numberOfTriples) {
    super.setUp(outputDirectory, query2fileName, graphCoverStrategy, nHopReplication, repetitions,
            numberOfChunks, numberOfTriples);
    File outputFile = new File(
            outputDirectory.getAbsolutePath() + File.separator + "chunkSizes.csv");
    boolean existsOutputFile = outputFile.exists();
    try {
      output = new BufferedWriter(
              new OutputStreamWriter(new FileOutputStream(outputFile, true), "UTF-8"));
      if (!existsOutputFile) {
        output.write("cover\tnumberOfChunks\tnumberOfTriples\tn-hop\tchunkSizes*");
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  protected void processTotalGraphSizeBeforeReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long totalGraphSize) {
  }

  @Override
  protected void processGraphChunkSizesBeforeReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long... graphChunkSizes) {
    processGraphChunkSizesAfterReplication(graphCoverStrategy, nHopReplication, numberOfChunks,
            numberOfTriples, graphChunkSizes);
  }

  @Override
  protected void processTotalGraphSizeAfterReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long totalGraphSize) {
  }

  @Override
  protected void processGraphChunkSizesAfterReplication(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long... graphChunkSizes) {
    chunkSizes = graphChunkSizes;
  }

  @Override
  protected void processLoadingFinished(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, int numberOfTriples) {
    try {
      StringBuilder sb = new StringBuilder();
      for (long value : chunkSizes) {
        sb.append("\t").append(value);
      }
      output.write("\n" + graphCoverStrategy + "\t" + numberOfChunks + "\t" + numberOfTriples + "\t"
              + nHopReplication + sb.toString());
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
