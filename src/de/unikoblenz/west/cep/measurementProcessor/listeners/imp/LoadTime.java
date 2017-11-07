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
import de.unikoblenz.west.cep.measurementProcessor.listeners.LoadGraphTimeListener;

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
public class LoadTime extends LoadGraphTimeListener {

  private Writer output;

  private long initialEncodingTime;

  private long coverCreationTime;

  private long finalEncodingStartTime;

  private long finalEncodingTime;

  private long nHopReplicationTime;

  private long statisticCollectionTime;

  private long ownershipAdjustmentTime;

  private long transferStartTime;

  private long transferEndTime;

  private long indexingStartTime;

  private long indexingEndTime;

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication, int repetitions,
          int numberOfChunks, int numberOfTriples) {
    super.setUp(outputDirectory, query2fileName, graphCoverStrategy, nHopReplication, repetitions,
            numberOfChunks, numberOfTriples);
    File outputFile = new File(
            outputDirectory.getAbsolutePath() + File.separator + "loadingTime.csv");
    boolean existsOutputFile = outputFile.exists();
    try {
      output = new BufferedWriter(
              new OutputStreamWriter(new FileOutputStream(outputFile, true), "UTF-8"));
      if (!existsOutputFile) {
        output.write(
                "cover\tnumberOfChunks\tnumberOfTriples\tnhop\tinitialEncodingTime\tcoverCreationTime\tfinalEncodingTime\tnHopReplicationTime\tstatisticCollectionTime\townershipAdjustmentTime\ttransferTime\tindexingTime");
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  protected void initialize(String[] measurements) {
    super.initialize(measurements);
    transferStartTime = Long.MAX_VALUE;
    transferEndTime = Long.MIN_VALUE;
    indexingStartTime = Long.MAX_VALUE;
    indexingEndTime = Long.MIN_VALUE;
  }

  @Override
  protected void processInitialDictionaryEncodingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime) {
    initialEncodingTime = startTime;
  }

  @Override
  protected void processInitialDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime) {
    initialEncodingTime = endTime - initialEncodingTime;
  }

  @Override
  protected void processGraphCoverCreationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime) {
    coverCreationTime = startTime;
  }

  @Override
  protected void processGraphCoverCreationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime) {
    coverCreationTime = endTime - coverCreationTime;
  }

  @Override
  protected void processFinalDictionaryEncodingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime) {
    finalEncodingStartTime = startTime;
  }

  @Override
  protected void processFinalDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime) {
    finalEncodingTime += endTime - finalEncodingStartTime;
  }

  @Override
  protected void processNHopReplicationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime) {
    nHopReplicationTime = startTime;
  }

  @Override
  protected void processNHopReplicationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime) {
    nHopReplicationTime = endTime - nHopReplicationTime;
  }

  @Override
  protected void processStatisticCollectionStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime) {
    statisticCollectionTime = startTime;
  }

  @Override
  protected void processStatisticCollectionEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime) {
    statisticCollectionTime = endTime - statisticCollectionTime;
  }

  @Override
  protected void processOwnershipAdjustmentStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long startTime) {
    ownershipAdjustmentTime = startTime;
  }

  @Override
  protected void processOwnershipAdjustmentEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, long endTime) {
    ownershipAdjustmentTime = endTime - ownershipAdjustmentTime;
  }

  @Override
  protected void processChunkTransferToSlavesStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, int slave, long startTime) {
    if (startTime < transferStartTime) {
      transferStartTime = startTime;
    }
  }

  @Override
  protected void processChunkTransferToSlavesEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, int numberOfTriples, int slave, long endTime) {
    if (transferEndTime < endTime) {
      transferEndTime = endTime;
    }
  }

  @Override
  protected void processIndexingStart(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, int numberOfTriples, int slave, long startTime) {
    if (startTime < indexingStartTime) {
      indexingStartTime = startTime;
    }
  }

  @Override
  protected void processIndexingEnd(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, int numberOfTriples, int slave, long endTime) {
    if (indexingEndTime < endTime) {
      indexingEndTime = endTime;
    }
  }

  @Override
  protected void processLoadingFinished(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, int numberOfTriples) {
    try {
      output.write("\n" + graphCoverStrategy + "\t" + numberOfChunks + "\t" + numberOfTriples + "\t"
              + nHopReplication + "\t" + initialEncodingTime + "\t" + coverCreationTime + "\t"
              + finalEncodingTime + "\t" + nHopReplicationTime + "\t" + statisticCollectionTime
              + "\t" + ownershipAdjustmentTime + "\t" + (transferEndTime - transferStartTime) + "\t"
              + (indexingEndTime - indexingStartTime));
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
