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
          CoverStrategyType graphCoverStrategy, int nHopReplication, int repetitions) {
    File outputFile = new File(
            outputDirectory.getAbsolutePath() + File.separator + "loadingTime.csv");
    boolean existsOutputFile = outputFile.exists();
    try {
      output = new BufferedWriter(
              new OutputStreamWriter(new FileOutputStream(outputFile, true), "UTF-8"));
      if (!existsOutputFile) {
        output.write(
                "cover\tnhop\tinitialEncodingTime\tcoverCreationTime\tfinalEncodingTime\tnHopReplicationTime\tstatisticCollectionTime\townershipAdjustmentTime\ttransferTime\tindexingTime");
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
    transferStartTime = Long.MAX_VALUE;
    transferEndTime = Long.MIN_VALUE;
    indexingStartTime = Long.MAX_VALUE;
    indexingEndTime = Long.MIN_VALUE;
  }

  @Override
  protected void processInitialDictionaryEncodingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime) {
    initialEncodingTime = startTime;
  }

  @Override
  protected void processInitialDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime) {
    initialEncodingTime = endTime - initialEncodingTime;
  }

  @Override
  protected void processGraphCoverCreationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime) {
    coverCreationTime = startTime;
  }

  @Override
  protected void processGraphCoverCreationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime) {
    coverCreationTime = endTime - coverCreationTime;
  }

  @Override
  protected void processFinalDictionaryEncodingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime) {
    finalEncodingTime = startTime;
  }

  @Override
  protected void processFinalDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime) {
    finalEncodingTime = endTime - finalEncodingTime;
  }

  @Override
  protected void processNHopReplicationStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime) {
    nHopReplicationTime = startTime;
  }

  @Override
  protected void processNHopReplicationEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime) {
    nHopReplicationTime = endTime - nHopReplicationTime;
  }

  @Override
  protected void processStatisticCollectionStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime) {
    statisticCollectionTime = startTime;
  }

  @Override
  protected void processStatisticCollectionEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime) {
    statisticCollectionTime = endTime - statisticCollectionTime;
  }

  @Override
  protected void processOwnershipAdjustmentStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime) {
    ownershipAdjustmentTime = startTime;
  }

  @Override
  protected void processOwnershipAdjustmentEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime) {
    ownershipAdjustmentTime = endTime - ownershipAdjustmentTime;
  }

  @Override
  protected void processChunkTransferToSlavesStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int slave, long startTime) {
    if (startTime < transferStartTime) {
      transferStartTime = startTime;
    }
  }

  @Override
  protected void processChunkTransferToSlavesEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int slave, long endTime) {
    if (transferEndTime < endTime) {
      transferEndTime = endTime;
    }
  }

  @Override
  protected void processIndexingStart(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int slave, long startTime) {
    if (startTime < indexingStartTime) {
      indexingStartTime = startTime;
    }
  }

  @Override
  protected void processIndexingEnd(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int slave, long endTime) {
    if (indexingEndTime < endTime) {
      indexingEndTime = endTime;
    }
  }

  @Override
  protected void processLoadingFinished(CoverStrategyType graphCoverStrategy, int nHopReplication) {
    try {
      output.write("\n" + graphCoverStrategy + "\t" + nHopReplication + "\t" + initialEncodingTime
              + "\t" + coverCreationTime + "\t" + finalEncodingTime + "\t" + nHopReplicationTime
              + "\t" + statisticCollectionTime + "\t" + ownershipAdjustmentTime + "\t"
              + (transferEndTime - transferStartTime) + "\t"
              + (indexingEndTime - indexingStartTime));
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
    transferStartTime = Long.MAX_VALUE;
    transferEndTime = Long.MIN_VALUE;
    indexingStartTime = Long.MAX_VALUE;
    indexingEndTime = Long.MIN_VALUE;
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
