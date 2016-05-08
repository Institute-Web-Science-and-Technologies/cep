package de.unikoblenz.west.cep.measurementProcessor.utils;

import java.io.BufferedReader;
import java.io.Closeable;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.LineNumberReader;
import java.util.Iterator;
import java.util.SortedSet;
import java.util.TreeSet;
import java.util.regex.Pattern;
import java.util.zip.GZIPInputStream;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class CSVIterator
        implements Iterable<String[]>, Iterator<String[]>, Closeable, AutoCloseable {

  private final LineNumberReader reader;

  private final int maxBufferSize;

  private final SortedSet<MeasurmentWrapper> buffer;

  private String[] next;

  public CSVIterator(File csvFile, int bufferSize) {
    maxBufferSize = bufferSize;
    buffer = new TreeSet<>();
    boolean isGZip = csvFile.getName().endsWith(".gz");
    try {
      reader = new LineNumberReader(new BufferedReader(
              new InputStreamReader(isGZip ? new GZIPInputStream(new FileInputStream(csvFile))
                      : new FileInputStream(csvFile), "UTF-8")));
      fillBuffer();
      next = getNext();
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public boolean hasNext() {
    return next != null;
  }

  @Override
  public String[] next() {
    String[] nextElement = next;
    next = getNext();
    return nextElement;
  }

  private String[] getNext() {
    if (buffer.isEmpty()) {
      return null;
    }
    MeasurmentWrapper measurement = buffer.first();
    buffer.remove(measurement);
    fillBuffer();
    return measurement.measurement;
  }

  private void fillBuffer() {
    try {
      while (buffer.size() < maxBufferSize) {
        String line = reader.readLine();
        if (line == null) {
          break;
        }
        if (line.trim().isEmpty()) {
          continue;
        }
        String[] measurement = line.split(Pattern.quote("\t"));
        if ((reader.getLineNumber() == 1) && measurement[0].equals("SERVER")) {
          // this is the CSV header
          continue;
        }
        buffer.add(new MeasurmentWrapper(measurement));
      }
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public Iterator<String[]> iterator() {
    return this;
  }

  @Override
  public void close() {
    try {
      reader.close();
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

}

class MeasurmentWrapper implements Comparable<MeasurmentWrapper> {

  private final long timestamp;

  private final long id;

  private final int computerId;

  public final String[] measurement;

  public MeasurmentWrapper(String[] measurement) {
    this.measurement = measurement;
    timestamp = Long.parseLong(measurement[2]);
    id = Long.parseLong(measurement[1]);
    computerId = Utilities.getComputerId(measurement);
  }

  @Override
  public int compareTo(MeasurmentWrapper o) {
    if (timestamp == o.timestamp) {
      if ((computerId == 0) && (o.computerId != 0)) {
        return 1;
      } else if ((o.computerId == 0) && (computerId != 0)) {
        return -1;
      } else if (computerId == o.computerId) {
        if (id == o.id) {
          return 0;
        } else if (id < o.id) {
          return -1;
        } else {
          return 1;
        }
      } else {
        return computerId - o.computerId;
      }
    } else if (timestamp < o.timestamp) {
      return -1;
    } else {
      return 1;
    }
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = (prime * result) + computerId;
    result = (prime * result) + (int) (id ^ (id >>> 32));
    result = (prime * result) + (int) (timestamp ^ (timestamp >>> 32));
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    MeasurmentWrapper other = (MeasurmentWrapper) obj;
    if (computerId != other.computerId) {
      return false;
    }
    if (id != other.id) {
      return false;
    }
    if (timestamp != other.timestamp) {
      return false;
    }
    return true;
  }

}
