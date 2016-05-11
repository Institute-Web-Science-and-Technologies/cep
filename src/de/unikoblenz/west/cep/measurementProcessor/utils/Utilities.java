package de.unikoblenz.west.cep.measurementProcessor.utils;

import de.uni_koblenz.west.koral.common.measurement.MeasurementType;

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

}
