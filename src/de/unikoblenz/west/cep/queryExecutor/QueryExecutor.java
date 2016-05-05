package de.unikoblenz.west.cep.queryExecutor;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;

import de.uni_koblenz.west.koral.client.KoralClient;
import de.uni_koblenz.west.koral.common.config.impl.Configuration;
import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileFilter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.zip.GZIPOutputStream;

/**
 * Executes a set of Queries.
 * 
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class QueryExecutor {

  public void executeQueries(File queryInput, File outputDir, String masterIp,
          int numberOfRepetitions) {
    if (!masterIp.contains(":")) {
      masterIp += ":" + Configuration.DEFAULT_CLIENT_PORT;
    }
    if ((outputDir != null) && !outputDir.exists()) {
      outputDir.mkdirs();
    }
    for (QueryExecutionTreeType treeType : QueryExecutionTreeType.values()) {
      for (int currentRepetition = 0; currentRepetition < numberOfRepetitions; currentRepetition++) {
        if (queryInput.isDirectory()) {
          for (File queryFile : queryInput.listFiles(new FileFilter() {

            @Override
            public boolean accept(File pathname) {
              return pathname.isFile() && pathname.getName().endsWith(".sparql");
            }

          })) {
            executeQuery(queryFile, outputDir, masterIp, treeType, currentRepetition);
          }
        } else {
          executeQuery(queryInput, outputDir, masterIp, treeType, currentRepetition);
        }
        try {
          Thread.sleep(500);
        } catch (InterruptedException e) {
        }
      }
    }
  }

  private void executeQuery(File queryFile, File outputDir, String masterIp,
          QueryExecutionTreeType treeType, int currentRepetition) {
    try (Writer outputWriter = (currentRepetition == 0)
            && (outputDir != null)
                    ? new BufferedWriter(new OutputStreamWriter(
                            new GZIPOutputStream(new FileOutputStream(outputDir.getAbsolutePath()
                                    + File.separator + queryFile.getName() + "_result.csv.gz")),
                            "UTF-8"))
                    : new NullWriter()) {

      KoralClient client = new KoralClient();
      for (int connectionAttempt = 0; connectionAttempt < 100; connectionAttempt++) {
        if (client.startUp(masterIp)) {
          break;
        }
      }
      client.processQueryFromFile(queryFile, outputWriter, treeType, false);
      client.shutDown();
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  public static void main(String[] args) throws ParseException {
    Options options = QueryExecutor.createCommandLineOptions();
    if (args.length == 0) {
      QueryExecutor.printUsage(options);
      return;
    }
    CommandLine line = QueryExecutor.parseCommandLineArgs(options, args);
    if (line.hasOption("h")) {
      QueryExecutor.printUsage(options);
      return;
    }

    File queryInput = new File(line.getOptionValue('i'));
    File outputDir = null;
    if (line.hasOption('o')) {
      outputDir = new File(line.getOptionValue('o'));
    }
    String masterIp = line.getOptionValue('m');

    int repetitions = Integer.parseInt(line.getOptionValue('r'));

    QueryExecutor queryExecutor = new QueryExecutor();
    queryExecutor.executeQueries(queryInput, outputDir, masterIp, repetitions);
  }

  private static Options createCommandLineOptions() {
    Option help = new Option("h", "help", false, "print this help message");
    help.setRequired(false);

    Option input = Option.builder("i").longOpt("input").hasArg().argName("fileOrDirctory")
            .desc("File or directory that contains the queries").required(true).build();

    Option output = Option.builder("o").longOpt("output").hasArg().argName("dirctory")
            .desc("Directory where the query results are stored.").required(false).build();

    Option koralMasterIP = Option.builder("m").longOpt("master").hasArg().argName("ip:port")
            .desc("IP an port of the Koral master. If port is not specified the default port is used.")
            .required(true).build();

    Option repetitions = Option.builder("r").longOpt("repetitions").hasArg().argName("int")
            .desc("The frequency how often the query execution should be repeated.").required(true)
            .build();

    Options options = new Options();
    options.addOption(help);
    options.addOption(input);
    options.addOption(output);
    options.addOption(koralMasterIP);
    options.addOption(repetitions);
    return options;
  }

  private static CommandLine parseCommandLineArgs(Options options, String[] args)
          throws ParseException {
    CommandLineParser parser = new DefaultParser();
    return parser.parse(options, args);
  }

  protected static void printUsage(Options options) {
    HelpFormatter formatter = new HelpFormatter();
    formatter.printHelp("java " + QueryExecutor.class.getName()
            + " [-h] -i <fileOrDirctory> [-o <directory>] -m <ip:port> -r <int>", options);
  }

}
