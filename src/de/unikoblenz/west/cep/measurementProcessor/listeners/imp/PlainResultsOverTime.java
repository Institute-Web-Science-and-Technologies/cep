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

import java.io.File;
import java.util.LinkedList;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class PlainResultsOverTime extends ResultsOverTime {

  public PlainResultsOverTime() {
    super();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(
            outputDirectory.getAbsolutePath() + File.separator + "plainResultsOverTime.csv");
  }

  @Override
  protected void processQueryStart(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, long queryStartTime) {
  }

  @Override
  protected void processQueryCoordinatorSendQueryStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
    queryStartTime = timestamp;
    sequenceOfResults = new LinkedList<>();
  }

}
