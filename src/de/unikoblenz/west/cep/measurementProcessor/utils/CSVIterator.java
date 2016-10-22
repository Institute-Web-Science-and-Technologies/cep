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
package de.unikoblenz.west.cep.measurementProcessor.utils;

import java.io.BufferedReader;
import java.io.Closeable;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.LineNumberReader;
import java.util.Arrays;
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

  private int currentQueryId;

  public CSVIterator(File csvFile, int bufferSize) {
    maxBufferSize = bufferSize;
    buffer = new TreeSet<>();
    currentQueryId = -1;
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
        if (measurement[0].equals("SERVER")) {
          // this is the CSV header
          continue;
        }
        MeasurmentWrapper wrapper = new MeasurmentWrapper(measurement, currentQueryId);
        if (wrapper.getQueryId() > currentQueryId) {
          currentQueryId = wrapper.getQueryId();
        }
        buffer.add(wrapper);
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

  private final int queryId;

  private final long timestamp;

  private final long id;

  private final int computerId;

  public final String[] measurement;

  public MeasurmentWrapper(String[] measurement, int previousQueryId) {
    this.measurement = measurement;
    timestamp = Long.parseLong(measurement[2]);
    id = Long.parseLong(measurement[1]);
    computerId = Utilities.getComputerId(measurement);
    switch (Utilities.getMeasurementType(measurement)) {
      case QUERY_COORDINATOR_END:
      case QUERY_COORDINATOR_PARSE_END:
      case QUERY_COORDINATOR_PARSE_START:
      case QUERY_COORDINATOR_SEND_QUERY_RESULTS_TO_CLIENT:
      case QUERY_COORDINATOR_SEND_QUERY_START:
      case QUERY_COORDINATOR_SEND_QUERY_TO_SLAVE:
      case QUERY_COORDINATOR_START:
      case QUERY_OPERATION_CLOSED:
      case QUERY_OPERATION_FINISH:
      case QUERY_OPERATION_START:
      case QUERY_SLAVE_QUERY_CREATION_END:
      case QUERY_SLAVE_QUERY_CREATION_START:
      case QUERY_SLAVE_QUERY_EXECUTION_ABORT:
      case QUERY_SLAVE_QUERY_EXECUTION_START:
        queryId = Integer.parseInt(measurement[5]);
        break;
      case QUERY_COORDINATOR_QET_NODES:
      case QUERY_OPERATION_JOIN_NUMBER_OF_COMPARISONS:
      case QUERY_OPERATION_SENT_FINISH_NOTIFICATIONS_TO_OTHER_SLAVES:
      case QUERY_OPERATION_SENT_MAPPINGS_TO_SLAVE:
        queryId = Integer.parseInt(measurement[4]);
        break;
      case QUERY_MESSAGE_RECEIPTION:
        queryId = previousQueryId == -1 ? -1 : previousQueryId + 1;
        break;
      default:
        queryId = -1;
    }
  }

  public int getQueryId() {
    return queryId;
  }

  @Override
  public int compareTo(MeasurmentWrapper o) {
    if (queryId == o.queryId) {
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
    } else if (queryId < o.queryId) {
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
    result = (prime * result) + Arrays.hashCode(measurement);
    result = (prime * result) + queryId;
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
    if (!Arrays.equals(measurement, other.measurement)) {
      return false;
    }
    if (queryId != other.queryId) {
      return false;
    }
    if (timestamp != other.timestamp) {
      return false;
    }
    return true;
  }

}
