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
package de.unikoblenz.west.cep.measurementProcessor.listeners.imp;

import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.measurementProcessor.listeners.ExtendedQuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryPackageSentListener;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class PackageTransfer extends QueryPackageSentListener {

  private final Map<QuerySignature, long[]> totalPackageTransfer;

  public PackageTransfer() {
    totalPackageTransfer = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "packageTransfer.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\ttransferredPackages";
  }

  @Override
  protected void processPackageSent(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, int slaveId, long[] sentPackages) {
    QuerySignature basicSignature = query.getBasicSignature();
    long[] packageTransfer = totalPackageTransfer.get(basicSignature);
    if (packageTransfer == null) {
      packageTransfer = new long[numberOfRepetitions];
      totalPackageTransfer.put(basicSignature, packageTransfer);
    }
    if (packageTransfer.length < query.repetition) {
      packageTransfer = Arrays.copyOf(packageTransfer, query.repetition);
      totalPackageTransfer.put(basicSignature, packageTransfer);
    }
    for (int i = 0; i < sentPackages.length; i++) {
      packageTransfer[query.repetition - 1] += sentPackages[i];
    }
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query, int minRepetition) {
    if ((minRepetition == 0)
            && ((numberOfTriples == 1_000_000_000) || (numberOfTriples == 500_000_000))) {
      // TODO manual adjust since first measurement does not contain this type
      // of measurement
      minRepetition = totalPackageTransfer.get(query.getBasicSignature()).length - 1;
      while ((minRepetition > 0)
              && (totalPackageTransfer.get(query.getBasicSignature())[minRepetition] == 0)) {
        minRepetition--;
      }
    }
    writeLine("\t" + totalPackageTransfer.get(query.getBasicSignature())[minRepetition]);
  }

}
