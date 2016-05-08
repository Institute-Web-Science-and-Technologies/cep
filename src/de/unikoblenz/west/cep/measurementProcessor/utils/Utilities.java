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

}
