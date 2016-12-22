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
import de.unikoblenz.west.cep.measurementProcessor.listeners.QuerySignature;
import de.unikoblenz.west.cep.measurementProcessor.listeners.QueryTimesListener;
import de.unikoblenz.west.cep.measurementProcessor.utils.Utilities;

import java.io.File;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class OverallQueryExecutionTime extends QueryTimesListener {

  private final Map<QuerySignature, long[]> query2repetitiontimes;

  private long queryStartTime;

  private long totalQueryExecutionTime;

  public OverallQueryExecutionTime() {
    super();
    query2repetitiontimes = new HashMap<>();
  }

  @Override
  protected File getOutputFile(File outputDirectory) {
    return new File(outputDirectory.getAbsolutePath() + File.separator + "totalExecutionTime.csv");
  }

  @Override
  protected String getHeadLine() {
    return super.getHeadLine() + "\ttotalExecutionTime";
  }

  @Override
  protected void processQueryStart(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, long queryStartTime) {
    this.queryStartTime = queryStartTime;
  }

  @Override
  protected void processQueryCoordinatorSendQueryStart(CoverStrategyType graphCoverStrategy,
          int nHopReplication, int numberOfChunks, ExtendedQuerySignature extendedQuerySignature,
          long timestamp) {
  }

  @Override
  protected void processQueryResult(CoverStrategyType graphCoverStrategy, int nHopReplication,
          int numberOfChunks, ExtendedQuerySignature query, long queryResultSentTime,
          long firstResultNumber, long lastResultNumber) {
    long executionTime = queryResultSentTime - queryStartTime;
    if (executionTime > totalQueryExecutionTime) {
      totalQueryExecutionTime = executionTime;
    }
  }

  @Override
  protected void processQueryFinish(ExtendedQuerySignature query) {
    QuerySignature basicSignature = query.getBasicSignature();
    long[] repetitions = query2repetitiontimes.get(basicSignature);
    if (repetitions == null) {
      repetitions = new long[numberOfRepetitions];
      query2repetitiontimes.put(basicSignature, repetitions);
    }
    repetitions[query.repetition - 1] = totalQueryExecutionTime;
    if (query.repetition == numberOfRepetitions) {
      query2repetitiontimes.remove(basicSignature);
      writeLine("\t" + Utilities.min(repetitions));
    }
    queryStartTime = 0;
    totalQueryExecutionTime = 0;
  }

}
