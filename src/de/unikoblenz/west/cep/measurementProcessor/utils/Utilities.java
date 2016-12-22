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

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;

import java.util.Arrays;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class Utilities {

  public static MeasurementType getMeasurementType(String... measurements) {
    try {
      return MeasurementType.valueOf(measurements[3]);
    } catch (IllegalArgumentException e) {
      // this is an unknown measurement type
      return null;
    }
  }

  public static int getComputerId(String... measurements) {
    String computerId = measurements[0];
    int index = computerId.indexOf(':');
    if (index >= 0) {
      computerId = computerId.substring(0, index);
    }
    if (!computerId.startsWith("slave")) {
      return 0;
    } else {
      return Integer.parseInt(computerId.split("slave[0]*")[1]);
    }
  }

  public static double computeEntropy(long[] individualValues, long totalSize) {
    double result = 0;
    double log = Math.log(2);
    for (long value : individualValues) {
      if (value == 0) {
        continue;
      }
      double factor = value / (double) totalSize;
      result += factor * (Math.log(factor) / log);
    }
    return result == 0 ? result : -result;
  }

  public static double computeStandardDeviation(long[] individualValues, long totalSize) {
    double factor = totalSize / (double) individualValues.length;
    double summ = 0;
    for (long value : individualValues) {
      double difference = value - factor;
      summ += difference * difference;
    }
    return Math.sqrt(summ / individualValues.length);
  }

  public static long computeArithmeticMean(long[] values) {
    long sum = 0;
    for (long value : values) {
      sum += value;
    }
    return sum / values.length;
  }

  /**
   * 
   * Gini-coefficient=\frac{n}{n-1}*(\frac{2*\sum\limits_{i=1}^{n}i*y_i}{n*\sum\limits_{i=1}^{n}y_i}-\frac{n+1}{n})
   * <br>
   * the smaller the value the more equal is the distribution. Values [0,1] are
   * possible
   * 
   * @param values
   * @return
   */
  public static double computeGiniCoefficient(long[] values) {
    long[] sortedValues = Arrays.copyOf(values, values.length);
    Arrays.sort(sortedValues);
    long numerator = 0;
    long denominator = 0;
    for (int i = 0; i < sortedValues.length; i++) {
      numerator += (i + 1) * sortedValues[i];
      denominator += sortedValues[i];
    }
    numerator *= 2;
    denominator *= sortedValues.length;
    double fraction = (numerator / (double) denominator)
            - ((sortedValues.length + 1) / (double) sortedValues.length);
    fraction *= sortedValues.length / (double) (sortedValues.length - 1);
    return fraction;
  }

  public static long min(long... values) {
    long min = Long.MAX_VALUE;
    for (long value : values) {
      if (value < min) {
        min = value;
      }
    }
    return min;
  }

}
