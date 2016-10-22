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
