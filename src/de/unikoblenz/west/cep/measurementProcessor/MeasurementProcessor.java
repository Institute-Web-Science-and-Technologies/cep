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
package de.unikoblenz.west.cep.measurementProcessor;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.jena.query.ARQ;
import org.apache.jena.query.QueryFactory;

import de.uni_koblenz.west.koral.common.measurement.MeasurementCollector;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.ChunkSizes;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.ComputationalEffort;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.ComputationalEffortPerChunk;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.DataTransfer;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.LoadTime;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.OverallQueryExecutionTime;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.PackageTransfer;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.PlainResultsOverTime;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.QueryExecutionTimeline;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.QueryOperationInput;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.QueryOperationOutput;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.QueryOperationTimesPerSlave;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.ResultsOverTime;
import de.unikoblenz.west.cep.measurementProcessor.listeners.imp.StorageBalance;
import de.unikoblenz.west.cep.measurementProcessor.utils.CSVIterator;
import de.unikoblenz.west.cep.queryExecutor.QueryFileFilter;

import java.io.BufferedReader;
import java.io.Closeable;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class MeasurementProcessor implements Closeable {

  private final List<MeasurementListener> listeners = new ArrayList<>();

  public void registerListener(MeasurementListener listener) {
    listeners.add(listener);
  }

  public void processLoadMeasurement(File inputFile, int numberOfChunks, int numberOfTriples,
          File outputDir) {
    ensureOutputDir(outputDir);
    for (MeasurementListener listener : listeners) {
      listener.setUp(outputDir, null, null, 0, 1, numberOfChunks, numberOfTriples);
    }
    processNextMeasurements(inputFile);
  }

  public void processQueryMeasurement(File queryDir, File inputFile, CoverStrategyType cover,
          int nhop, int repetitions, int numberOfChunks, int numberOfTriples, File outputDir) {
    try {
      ensureOutputDir(outputDir);
      Map<String, String> query2fileName = generateQuery2fileNameMap(queryDir);
      for (MeasurementListener listener : listeners) {
        listener.setUp(outputDir, query2fileName, cover, nhop, repetitions, numberOfChunks,
                numberOfTriples);
      }
      processNextMeasurements(inputFile);
    } catch (Exception e) {
      clear();
      throw e;
    }
  }

  private void ensureOutputDir(File outputDir) {
    if (!outputDir.exists()) {
      outputDir.mkdirs();
    }
  }

  private Map<String, String> generateQuery2fileNameMap(File queryDir) {
    Map<String, String> query2fileName = new HashMap<>();
    for (File queryFile : queryDir.listFiles(new QueryFileFilter())) {
      try {
        // workaround for bug in Jena ARQ
        ARQ.init();
        String queryString = QueryFactory.create(readQueryFromFile(queryFile)).serialize()
                .replace(MeasurementCollector.columnSeparator, " ")
                .replace(MeasurementCollector.rowSeparator, " ");
        query2fileName.put(queryString, queryFile.getName());
      } catch (IOException e) {
        throw new RuntimeException(e);
      }
    }
    return query2fileName;
  }

  private String readQueryFromFile(File queryFile) throws FileNotFoundException, IOException {
    try (BufferedReader br = new BufferedReader(new FileReader(queryFile));) {
      StringBuilder sb = new StringBuilder();
      String delim = "";
      for (String line = br.readLine(); line != null; line = br.readLine()) {
        sb.append(delim);
        sb.append(line);
        delim = "\n";
      }
      return sb.toString();
    }
  }

  public void processNextMeasurements(File inputFile) {
    try (CSVIterator iterator = new CSVIterator(inputFile, 1000);) {
      for (String[] measurement : iterator) {
        for (MeasurementListener listener : listeners) {
          listener.processMeasurement(measurement);
        }
      }
    }
  }

  public void clear() {
    for (MeasurementListener listener : listeners) {
      listener.clear();
    }
  }

  @Override
  public void close() {
    for (MeasurementListener listener : listeners) {
      listener.tearDown();
    }
  }

  @SuppressWarnings("unchecked")
  public static Class<? extends MeasurementListener>[] loadListeners = new Class[] {
          StorageBalance.class, LoadTime.class, ChunkSizes.class };

  @SuppressWarnings("unchecked")
  public static Class<? extends MeasurementListener>[] queryListeners = new Class[] {
          DataTransfer.class, ComputationalEffort.class, OverallQueryExecutionTime.class,
          ResultsOverTime.class, ComputationalEffortPerChunk.class,
          QueryOperationTimesPerSlave.class, QueryExecutionTimeline.class,
          QueryOperationOutput.class, QueryOperationInput.class, PlainResultsOverTime.class,
          PackageTransfer.class };

  public static void main(String[] args) throws ParseException {
    Options options = MeasurementProcessor.createCommandLineOptions();
    if (args.length == 0) {
      MeasurementProcessor.printUsage(options);
      return;
    }
    CommandLine line = MeasurementProcessor.parseCommandLineArgs(options, args);
    if (line.hasOption("h")) {
      MeasurementProcessor.printUsage(options);
      return;
    }

    File outputDir = new File(line.getOptionValue('o'));

    int numberOfChunks = Integer.parseInt(line.getOptionValue('C'));

    int numberOfTriples = Integer.parseInt(line.getOptionValue('T'));

    MeasurementProcessor measurementProcessor = new MeasurementProcessor();
    try {
      if (line.hasOption('l')) {
        MeasurementProcessor.registerListeners(measurementProcessor,
                MeasurementProcessor.loadListeners);
        File inputFile = new File(line.getOptionValue('l'));
        measurementProcessor.processLoadMeasurement(inputFile, numberOfChunks, numberOfTriples,
                outputDir);

      } else if (line.hasOption('q')) {
        MeasurementProcessor.registerListeners(measurementProcessor,
                MeasurementProcessor.queryListeners);
        File inputFile = new File(line.getOptionValue('q'));
        CoverStrategyType cover = null;
        if (line.hasOption('c')) {
          cover = CoverStrategyType.valueOf(line.getOptionValue('c'));
        } else {
          throw new RuntimeException("Loading a querying file requires the option -c.");
        }

        int nhop = 0;
        if (line.hasOption('n')) {
          nhop = Integer.parseInt(line.getOptionValue('n'));
        }

        int repetitions = 0;
        if (line.hasOption('r')) {
          repetitions = Integer.parseInt(line.getOptionValue('r'));
        } else {
          throw new RuntimeException("Loading a querying file requires the option -r.");
        }

        File queryDir = null;
        if (line.hasOption('Q')) {
          queryDir = new File(line.getOptionValue('Q'));
        } else {
          throw new RuntimeException("Loading a querying file requires the option -Q.");
        }

        measurementProcessor.processQueryMeasurement(queryDir, inputFile, cover, nhop, repetitions,
                numberOfChunks, numberOfTriples, outputDir);

      } else {
        throw new RuntimeException("Option -l or -q is required.");
      }
    } finally {
      measurementProcessor.close();
    }
  }

  public static void registerListeners(MeasurementProcessor measurementProcessor,
          Class<? extends MeasurementListener>[] listeners) {
    for (Class<? extends MeasurementListener> listenerClas : listeners) {
      try {
        MeasurementListener listener = listenerClas.getDeclaredConstructor().newInstance();
        measurementProcessor.registerListener(listener);
      } catch (InstantiationException | IllegalAccessException | IllegalArgumentException
              | InvocationTargetException | NoSuchMethodException | SecurityException e) {
        throw new RuntimeException(e);
      }
    }
  }

  private static Options createCommandLineOptions() {
    Option help = new Option("h", "help", false, "print this help message");
    help.setRequired(false);

    Option output = Option.builder("o").longOpt("output").hasArg().argName("dirctory")
            .desc("Directory where the statistical information is stored.").required(true).build();

    Option loadFile = Option.builder("l").longOpt("loadFile").hasArg().argName("loadFile")
            .desc("csv file with measurements of loading").required(false).build();

    Option queryFile = Option.builder("q").longOpt("queryFile").hasArg().argName("queryFile")
            .desc("csv file with measurements of querying").required(false).build();

    Option cover = Option.builder("c").longOpt("cover").hasArg().argName("coverStrategy")
            .desc("the graph cover strategy used during querying. Possible valueas are "
                    + Arrays.toString(CoverStrategyType.values()))
            .required(false).build();

    Option nhop = Option.builder("n").longOpt("nhop").hasArg().argName("int")
            .desc("the used n-hop replication. Default is 0, i.e., noh n-hop replication")
            .required(false).build();

    Option repetitions = Option.builder("r").longOpt("repetitions").hasArg().argName("int")
            .desc("the number of performed repetitions").required(false).build();

    Option numberOfChunks = Option.builder("C").longOpt("numberOfChunks").hasArg().argName("int")
            .desc("the number of chunks").required(true).build();

    Option numberOfTriples = Option.builder("T").longOpt("numberOfTriples").hasArg().argName("int")
            .desc("the number of triples").required(true).build();

    Option queryFiles = Option.builder("Q").longOpt("queryFiles").hasArg().argName("directory")
            .desc("the directory that contains the query").required(false).build();

    Options options = new Options();
    options.addOption(help);
    options.addOption(output);
    options.addOption(loadFile);
    options.addOption(queryFile);
    options.addOption(cover);
    options.addOption(nhop);
    options.addOption(repetitions);
    options.addOption(numberOfChunks);
    options.addOption(numberOfTriples);
    options.addOption(queryFiles);
    return options;
  }

  private static CommandLine parseCommandLineArgs(Options options, String[] args)
          throws ParseException {
    CommandLineParser parser = new DefaultParser();
    return parser.parse(options, args);
  }

  protected static void printUsage(Options options) {
    HelpFormatter formatter = new HelpFormatter();
    PrintWriter pw = new PrintWriter(System.out, true);
    formatter.printUsage(pw, 100, MeasurementProcessor.class.getName(), options);
    formatter.printOptions(pw, 100, options, 2, 2);
  }

}
