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

  private long coverCreationTime;

  private long encodingTime;

  private long transferStartTime;

  private long transferEndTime;

  private long indexingStartTime;

  private long indexingEndTime;

  @Override
  public void setUp(File outputDirectory, Map<String, String> query2fileName,
          CoverStrategyType graphCoverStrategy, int nHopReplication) {
    File outputFile = new File(
            outputDirectory.getAbsolutePath() + File.separator + "loadingTime.csv");
    boolean existsOutputFile = outputFile.exists();
    try {
      output = new BufferedWriter(
              new OutputStreamWriter(new FileOutputStream(outputFile, true), "UTF-8"));
      if (!existsOutputFile) {
        output.write("cover\tnhop\tcoverCreationTime\tencodingTime\ttransferTime\tindexingTime");
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
  protected void processDictionaryEncodingStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long startTime) {
    encodingTime = startTime;
  }

  @Override
  protected void processDictionaryEncodingEnd(CoverStrategyType graphCoverStrategy,
          int nHopReplication, long endTime) {
    encodingTime = endTime - encodingTime;
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
      output.write("\n" + graphCoverStrategy + "\t" + nHopReplication + "\t" + coverCreationTime
              + "\t" + encodingTime + "\t" + (transferEndTime - transferStartTime) + "\t"
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
