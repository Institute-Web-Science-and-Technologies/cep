package playground;

import de.unikoblenz.west.cep.measurementProcessor.utils.CSVIterator;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class CSVSorter {

  public static void main(String[] args) {
    if (args.length != 2) {
      System.out.println("Path to a CSV file is missing or output path is missing");
      return;
    }
    try (BufferedWriter writer = new BufferedWriter(new FileWriter(args[1]));) {
      CSVIterator iterator = new CSVIterator(new File(args[0]), 1000);
      String lineDelim = "";
      for (String[] measurements : iterator) {
        writer.write(lineDelim);
        String columnDelim = "";
        for (String measurement : measurements) {
          writer.write(columnDelim);
          writer.write(measurement);
          columnDelim = "\t";
        }
        lineDelim = "\n";
      }
      iterator.close();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

}
