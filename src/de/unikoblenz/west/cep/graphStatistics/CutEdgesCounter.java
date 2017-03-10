package de.unikoblenz.west.cep.graphStatistics;

import org.rocksdb.Options;
import org.rocksdb.RocksDB;
import org.rocksdb.RocksDBException;
import org.rocksdb.WriteBatch;
import org.rocksdb.WriteOptions;

import de.uni_koblenz.west.koral.common.io.EncodedFileInputStream;
import de.uni_koblenz.west.koral.common.io.EncodingFileFormat;
import de.uni_koblenz.west.koral.common.io.Statement;
import de.uni_koblenz.west.koral.common.utils.NumberConversion;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileFilter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.Comparator;

/**
 * Counts the number of cut edges.
 * 
 * 
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class CutEdgesCounter {

  private File[] chunks;

  private long[][] numberOfOutgoingCutEdges;

  private long[][] numberOfIngoingCutEdges;

  public CutEdgesCounter() {
  }

  public void countCutEdges(File[] chunks) {
    this.chunks = chunks;
    numberOfOutgoingCutEdges = new long[chunks.length][chunks.length];
    numberOfIngoingCutEdges = new long[chunks.length][chunks.length];

    File workingDir = null;
    RocksDB map = null;
    try {
      workingDir = Files.createTempDirectory(CutEdgesCounter.class.getSimpleName()).toFile();
      Options options = new Options();
      options.setCreateIfMissing(true);
      options.setMaxOpenFiles(1000);
      options.setAllowOsBuffer(true);
      options.setWriteBufferSize(64 * 1024 * 1024);
      options.setTargetFileSizeBase(64 * 1024 * 1024);
      options.setArenaBlockSize(32 * 1024);
      map = RocksDB.open(options, workingDir + File.separator + "map");
      collectSubjectOwnership(map, chunks);
      map.compactRange();
      collectStatistics(map, chunks);
    } catch (IOException e) {
      throw new RuntimeException(e);
    } catch (RocksDBException e) {
      throw new RuntimeException(e);
    } finally {
      if (map != null) {
        map.close();
      }
      if (!delete(workingDir)) {
        System.out.println(
                "The directory " + workingDir.getAbsolutePath() + " could not be deleted.");
      }
      if ((workingDir != null) && workingDir.exists()) {
        workingDir.deleteOnExit();
      }
    }
  }

  private void collectSubjectOwnership(RocksDB map, File[] chunks) {
    System.out.println("Collecting subject ownership");
    try {
      WriteOptions writeOpts = new WriteOptions();
      WriteBatch writeBatch = new WriteBatch();
      int batchSize = 0;
      for (int chunkId = 0; chunkId < chunks.length; chunkId++) {
        System.out.println("\tprocessing " + chunks[chunkId].getName());
        byte[] id = NumberConversion.int2bytes(chunkId);
        try (EncodedFileInputStream in = new EncodedFileInputStream(EncodingFileFormat.EEE,
                chunks[chunkId]);) {
          for (Statement stmt : in) {
            byte[] subject = stmt.getSubject();
            writeBatch.put(subject, id);
            batchSize++;
            if (batchSize >= ((64 * 1024 * 1024) / (Integer.BYTES + Long.BYTES))) {
              map.write(writeOpts, writeBatch);
              batchSize = 0;
              writeBatch = new WriteBatch();
            }
          }
        } catch (IOException e) {
          throw new RuntimeException(e);
        }
      }
      if (batchSize > 0) {
        map.write(writeOpts, writeBatch);
        batchSize = 0;
        writeBatch = null;
      }
    } catch (RocksDBException e) {
      throw new RuntimeException(e);
    }
  }

  private void collectStatistics(RocksDB map, File[] chunks) {
    System.out.println("Collecting statistics");
    for (int chunkId = 0; chunkId < chunks.length; chunkId++) {
      try (EncodedFileInputStream in = new EncodedFileInputStream(EncodingFileFormat.EEE,
              chunks[chunkId]);) {
        System.out.println("\tprocessing " + chunks[chunkId].getName());
        for (Statement stmt : in) {
          byte[] object = stmt.getObject();
          byte[] chunkOwner = map.get(object);
          // chunkOwner==null -> this object does not occur as subject
          if ((chunkOwner != null)) {
            // this is a cut edge
            int otherChunkId = NumberConversion.bytes2int(chunkOwner);
            numberOfOutgoingCutEdges[chunkId][otherChunkId]++;
            numberOfIngoingCutEdges[otherChunkId][chunkId]++;
          }
        }
      } catch (IOException | RocksDBException e) {
        throw new RuntimeException(e);
      }
    }
  }

  private boolean delete(File workingDir) {
    if (!workingDir.exists()) {
      return true;
    } else if (workingDir.isFile()) {
      return workingDir.delete();
    } else {
      for (File subFile : workingDir.listFiles()) {
        delete(subFile);
      }
      return workingDir.delete();
    }
  }

  public File[] getChunks() {
    return chunks;
  }

  public long[][] getNumberOfOutgoingCutEdges() {
    return numberOfOutgoingCutEdges;
  }

  public long[][] getNumberOfIngoingCutEdges() {
    return numberOfIngoingCutEdges;
  }

  public static void main(String[] args) throws FileNotFoundException {
    boolean hasOutputFile = (args.length > 0) && args[0].equals("-o");
    if ((hasOutputFile && (args.length < 3)) || (!hasOutputFile && (args.length < 1))) {
      System.out.println("Usage: jave " + CutEdgesCounter.class.getName()
              + "[-o <outputFile.csv>] <FolderWithchunkXX.adj.gz>");
      return;
    }
    PrintStream out = System.out;
    if (hasOutputFile) {
      out = new PrintStream(new BufferedOutputStream(new FileOutputStream(new File(args[1]))));
      args = Arrays.copyOfRange(args, 2, args.length);
    }
    File[] chunks = new File(args[0]).listFiles(new FileFilter() {
      @Override
      public boolean accept(File pathname) {
        String simpleName = pathname.getName();
        return pathname.isFile() && simpleName.matches("chunk\\d+\\.adj\\.gz");
      }
    });
    Arrays.sort(chunks, new Comparator<File>() {
      @Override
      public int compare(File o1, File o2) {
        int o1Number = CutEdgesCounter.extractChunkNumber(o1.getName());
        int o2Number = CutEdgesCounter.extractChunkNumber(o2.getName());
        return o1Number - o2Number;
      }
    });
    CutEdgesCounter counter = new CutEdgesCounter();
    counter.countCutEdges(chunks);
    try {
      out.print("CHUNK_ID\tCHUNK_NAME");
      for (int i = 0; i < chunks.length; i++) {
        out.print("\tEDGES_TO_CHUNK_" + i + "\tEDGES_FROM_CHUNK_" + i);
      }
      out.println("\tTOTAL_CUT_OUT_EDGES\tTOTAL_CUT_IN_EDGES");
      for (int i = 0; i < chunks.length; i++) {
        String chunkName = counter.getChunks()[i].getName();
        out.print(CutEdgesCounter.extractChunkNumber(chunkName) + "\t" + chunkName);
        long totalCutOutEdges = 0;
        long totalCutInEdges = 0;
        long[] outEdges = counter.getNumberOfOutgoingCutEdges()[i];
        long[] inEdges = counter.getNumberOfIngoingCutEdges()[i];
        for (int j = 0; j < chunks.length; j++) {
          out.print("\t" + outEdges[j] + "\t" + inEdges[j]);
          if (i != j) {
            totalCutOutEdges += outEdges[j];
            totalCutInEdges += inEdges[j];
          }
        }
        out.println("\t" + totalCutOutEdges + "\t" + totalCutInEdges);
      }
    } finally {
      if (out != System.out) {
        out.close();
      }
    }
  }

  private static int extractChunkNumber(String name) {
    String numberString = name.substring(5, name.indexOf('.'));
    return Integer.parseInt(numberString);
  }

}
