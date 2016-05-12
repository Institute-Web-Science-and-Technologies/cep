package de.unikoblenz.west.cep.diagramCreator;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import java.io.BufferedReader;
import java.io.Closeable;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.LineNumberReader;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class DiagramCreator implements Closeable {

  private List<DiagramListener> listeners = new ArrayList<>();

  public void registerListener(DiagramListener listener) {
    listeners.add(listener);
  }

  private void createDiagrams(File inputFile, OutputFormat format, File outputDir) {
    if (!outputDir.exists()) {
      outputDir.mkdirs();
    }
    for (DiagramListener listener : listeners) {
      listener.setUp(format, outputDir);
    }
    try (LineNumberReader in = new LineNumberReader(
            new BufferedReader(new InputStreamReader(new FileInputStream(inputFile), "UTF-8")));) {
      for (String line = in.readLine(); line != null; line = in.readLine()) {
        if (in.getLineNumber() == 1) {
          // skip header
          continue;
        }
        String[] parts = line.split(Pattern.quote("\t"));
        for (DiagramListener listener : listeners) {
          listener.process(parts);
        }
      }
      for (DiagramListener listener : listeners) {
        listener.tearDown();
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }

  }

  public void removeAllListeners() {
    close();
    listeners = new ArrayList<>();
  }

  @Override
  public void close() {
    for (DiagramListener listener : listeners) {
      listener.close();
    }
  }

  // TODO add listeners here

  @SuppressWarnings("unchecked")
  private static Class<? extends DiagramListener>[] loadingTimeListeners = new Class[] {};

  @SuppressWarnings("unchecked")
  private static Class<? extends DiagramListener>[] dataTransferListeners = new Class[] {};

  @SuppressWarnings("unchecked")
  private static Class<? extends DiagramListener>[] computationalEffortListeners = new Class[] {};

  @SuppressWarnings("unchecked")
  private static Class<? extends DiagramListener>[] totalExecutionTimeListeners = new Class[] {};

  @SuppressWarnings("unchecked")
  private static Class<? extends DiagramListener>[] resultsOverTimeListeners = new Class[] {};

  public static void main(String[] args) throws ParseException {
    Options options = DiagramCreator.createCommandLineOptions();
    if (args.length == 0) {
      DiagramCreator.printUsage(options);
      return;
    }
    CommandLine line = DiagramCreator.parseCommandLineArgs(options, args);
    if (line.hasOption("h")) {
      DiagramCreator.printUsage(options);
      return;
    }

    File outputDir = new File(line.getOptionValue('o'));

    OutputFormat format = OutputFormat.valueOf(line.getOptionValue('f').toUpperCase());

    DiagramCreator diagramCreator = new DiagramCreator();
    try {
      if (line.hasOption("loadingTime")) {
        diagramCreator.removeAllListeners();
        DiagramCreator.registerListeners(diagramCreator, DiagramCreator.loadingTimeListeners);
        diagramCreator.createDiagrams(new File(line.getOptionValue("loadingTime")), format,
                outputDir);
      }

      if (line.hasOption("computationalEffortTime")) {
        diagramCreator.removeAllListeners();
        DiagramCreator.registerListeners(diagramCreator,
                DiagramCreator.computationalEffortListeners);
        diagramCreator.createDiagrams(new File(line.getOptionValue("computationalEffort")), format,
                outputDir);
      }

      if (line.hasOption("dataTransfer")) {
        diagramCreator.removeAllListeners();
        DiagramCreator.registerListeners(diagramCreator, DiagramCreator.dataTransferListeners);
        diagramCreator.createDiagrams(new File(line.getOptionValue("dataTransfer")), format,
                outputDir);
      }

      if (line.hasOption("totalExecutionTime")) {
        diagramCreator.removeAllListeners();
        DiagramCreator.registerListeners(diagramCreator,
                DiagramCreator.totalExecutionTimeListeners);
        diagramCreator.createDiagrams(new File(line.getOptionValue("totalExecutionTime")), format,
                outputDir);
      }

      if (line.hasOption("resultsOverTime")) {
        diagramCreator.removeAllListeners();
        DiagramCreator.registerListeners(diagramCreator, DiagramCreator.resultsOverTimeListeners);
        diagramCreator.createDiagrams(new File(line.getOptionValue("resultsOverTime")), format,
                outputDir);
      }
    } finally {
      diagramCreator.close();
    }
  }

  private static void registerListeners(DiagramCreator diagramCreator,
          Class<? extends DiagramListener>[] listeners) {
    for (Class<? extends DiagramListener> listenerClas : listeners) {
      try {
        DiagramListener listener = listenerClas.newInstance();
        diagramCreator.registerListener(listener);
      } catch (InstantiationException | IllegalAccessException e) {
        throw new RuntimeException(e);
      }
    }
  }

  private static Options createCommandLineOptions() {
    Option help = new Option("h", "help", false, "print this help message");
    help.setRequired(false);

    Option output = Option.builder("o").longOpt("output").hasArg().argName("dirctory")
            .desc("Directory where the diagrams are stored.").required(true).build();

    Option format = Option.builder("f").longOpt("format").hasArg().argName("diagramFormat")
            .desc("the format of the created diagram image. Possible valueas are "
                    + Arrays.toString(OutputFormat.values()))
            .required(true).build();

    Option loadingTimeFile = Option.builder("l").longOpt("loadingTime").hasArg()
            .argName("loadingTime.csv").desc("the loadingTime.csv to be processed").required(false)
            .build();

    Option computationalEffortFile = Option.builder("c").longOpt("computationalEffort").hasArg()
            .argName("computationalEffort.csv").desc("the computationalEffort.csv to be processed")
            .required(false).build();

    Option dataTransferFile = Option.builder("d").longOpt("dataTransfer").hasArg()
            .argName("dataTransfer.csv").desc("the dataTransfer.csv to be processed")
            .required(false).build();

    Option totalExecutionTimeFile = Option.builder("e").longOpt("totalExecutionTime").hasArg()
            .argName("totalExecutionTime.csv").desc("the totalExecutionTime.csv to be processed")
            .required(false).build();

    Option resultsOverTimeFile = Option.builder("r").longOpt("resultsOverTime").hasArg()
            .argName("resultsOverTime.csv").desc("the resultsOverTime.csv to be processed")
            .required(false).build();

    Options options = new Options();
    options.addOption(help);
    options.addOption(output);
    options.addOption(format);
    options.addOption(loadingTimeFile);
    options.addOption(computationalEffortFile);
    options.addOption(dataTransferFile);
    options.addOption(totalExecutionTimeFile);
    options.addOption(resultsOverTimeFile);
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
    formatter.printUsage(pw, 100, DiagramCreator.class.getName(), options);
    formatter.printOptions(pw, 100, options, 2, 2);
  }

}
