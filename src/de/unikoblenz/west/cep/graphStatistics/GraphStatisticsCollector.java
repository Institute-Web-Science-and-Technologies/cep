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
package de.unikoblenz.west.cep.graphStatistics;

import org.apache.jena.graph.Node;
import org.apache.jena.iri.IRI;
import org.apache.jena.riot.system.IRIResolver;

import de.uni_koblenz.west.koral.common.utils.RDFFileIterator;
import de.uni_koblenz.west.koral.master.dictionary.Dictionary;
import de.uni_koblenz.west.koral.master.dictionary.impl.RocksDBDictionary;
import de.uni_koblenz.west.koral.master.utils.DeSerializer;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.regex.Pattern;

/**
 * Collects statistics about the dataset graph.
 * 
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class GraphStatisticsCollector implements AutoCloseable {

  private long numberOfTriples;

  private long numberOfGraphs;

  private boolean requiresDefaultGraph;

  private final Dictionary graphDictionary;

  private long numberOfSubjects;

  private final Dictionary subjectDictionary;

  private long numberOfProperties;

  private final Dictionary propertyDictionary;

  private long numberOfObjects;

  private final Dictionary objectDictionary;

  private final File workingDir;

  public GraphStatisticsCollector(File tmpDir) {
    workingDir = new File(tmpDir.getAbsolutePath() + File.separator + getClass().getSimpleName());
    if (!workingDir.exists()) {
      workingDir.mkdirs();
    }
    graphDictionary = new RocksDBDictionary(
            workingDir.getAbsolutePath() + File.separator + "graphDictionary",
            RocksDBDictionary.DEFAULT_MAX_BATCH_SIZE, 250);
    subjectDictionary = new RocksDBDictionary(
            workingDir.getAbsolutePath() + File.separator + "subjectDictionary",
            RocksDBDictionary.DEFAULT_MAX_BATCH_SIZE, 250);
    propertyDictionary = new RocksDBDictionary(
            workingDir.getAbsolutePath() + File.separator + "propertyDictionary",
            RocksDBDictionary.DEFAULT_MAX_BATCH_SIZE, 250);
    objectDictionary = new RocksDBDictionary(
            workingDir.getAbsolutePath() + File.separator + "objectDictionary",
            RocksDBDictionary.DEFAULT_MAX_BATCH_SIZE, 250);
    requiresDefaultGraph = false;
  }

  private void processGraphFile(File dataset) {
    try (RDFFileIterator iter = new RDFFileIterator(dataset, false, null)) {
      for (Node[] statement : iter) {
        numberOfTriples++;
        numberOfSubjects = count(subjectDictionary, statement[0], numberOfSubjects);
        numberOfProperties = count(propertyDictionary, statement[1], numberOfProperties);
        numberOfObjects = count(objectDictionary, statement[2], numberOfObjects);
        if (statement.length > 3) {
          numberOfGraphs = count(graphDictionary, getTopLevelDomain(statement[3]), numberOfGraphs);
        } else {
          requiresDefaultGraph = true;
        }
        if ((numberOfTriples % 1_000_000) == 0) {
          System.out.println("processed " + numberOfTriples + " triples");
        }
      }
    }
  }

  private long count(Dictionary dictionary, Node node, long oldCount) {
    String serializedNode = DeSerializer.serializeNode(node);
    return count(dictionary, serializedNode, oldCount);
  }

  private long count(Dictionary dictionary, String serializedNode, long oldCount) {
    long nextId = dictionary.encode(serializedNode, true);
    if (nextId > oldCount) {
      return nextId;
    } else {
      return oldCount;
    }
  }

  private String getTopLevelDomain(Node node) {
    String iriStr = DeSerializer.serializeNode(node);
    if (iriStr.startsWith("<")) {
      iriStr = iriStr.substring(1);
      if (iriStr.endsWith(">")) {
        iriStr = iriStr.substring(0, iriStr.length() - 1);
      }
    }
    IRI iri = IRIResolver.parseIRI(iriStr);
    String host = iri.getRawHost();
    String[] hostParts = null;
    if (host != null) {
      hostParts = host.split(Pattern.quote("."));
    } else {
      return iriStr;
    }
    StringBuilder sb = new StringBuilder();
    sb.append("http://");
    int startIndex = 0;
    for (startIndex = hostParts.length - 1; startIndex > 0; startIndex--) {
      if (hostParts[startIndex].length() > 3) {
        break;
      }
    }
    String delim = "";
    for (int i = startIndex; i < hostParts.length; i++) {
      sb.append(delim).append(hostParts[i]);
      delim = ".";
    }
    sb.append("/");
    return sb.toString();
  }

  public long getNumberOfTriples() {
    return numberOfTriples;
  }

  public long getNumberOfGraphs() {
    return requiresDefaultGraph ? numberOfGraphs + 1 : numberOfGraphs;
  }

  public long getNumberOfSubjects() {
    return numberOfSubjects;
  }

  public long getNumberOfProperties() {
    return numberOfProperties;
  }

  public long getNumberOfObjects() {
    return numberOfObjects;
  }

  @Override
  public void close() {
    graphDictionary.close();
    subjectDictionary.close();
    propertyDictionary.close();
    objectDictionary.close();
    if (!delete(workingDir)) {
      System.out
              .println("The directory " + workingDir.getAbsolutePath() + " could not be deleted.");
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

  public static void main(String[] args) throws IOException {
    boolean hasOutputFile = args[0].equals("-o");
    if ((args.length == 0) || (hasOutputFile && (args.length <= 2))) {
      System.out.println("Usage: java " + GraphStatisticsCollector.class.getName()
              + " [-o outputFile] <GraphFileOrFolder>+");
      return;
    }
    File tmpDir = Files.createTempDirectory(GraphStatisticsCollector.class.getSimpleName())
            .toFile();
    try (GraphStatisticsCollector collector = new GraphStatisticsCollector(tmpDir);) {
      for (int i = hasOutputFile ? 2 : 0; i < args.length; i++) {
        collector.processGraphFile(new File(args[i]));
      }
      PrintStream out = System.out;
      try {
        if (hasOutputFile) {
          out = new PrintStream(new BufferedOutputStream(new FileOutputStream(args[1])));
        } else {
          out.println("#################################################################");
        }
        out.println("Statistics for: "
                + Arrays.toString(hasOutputFile ? Arrays.copyOfRange(args, 2, args.length) : args));
        out.println("number of triples: " + collector.getNumberOfTriples());
        out.println("number of graphs: " + collector.getNumberOfGraphs());
        out.println("number of subjects: " + collector.getNumberOfSubjects());
        out.println("number of properties: " + collector.getNumberOfProperties());
        out.println("number of objects: " + collector.getNumberOfObjects());
      } finally {
        out.flush();
        if (out != System.out) {
          out.close();
        }
      }
      tmpDir.deleteOnExit();
    }
  }

}
