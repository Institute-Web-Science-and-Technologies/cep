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
package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class QuerySignature {

  public final String queryFileName;

  public final QueryExecutionTreeType treeType;

  public QuerySignature(String queryFileName, QueryExecutionTreeType treeType) {
    super();
    this.queryFileName = queryFileName;
    this.treeType = treeType;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = (prime * result) + ((queryFileName == null) ? 0 : queryFileName.hashCode());
    result = (prime * result) + ((treeType == null) ? 0 : treeType.hashCode());
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
    QuerySignature other = (QuerySignature) obj;
    if (queryFileName == null) {
      if (other.queryFileName != null) {
        return false;
      }
    } else if (!queryFileName.equals(other.queryFileName)) {
      return false;
    }
    if (treeType != other.treeType) {
      return false;
    }
    return true;
  }

  @Override
  public String toString() {
    return "QuerySignature [queryFileName=" + queryFileName + ", treeType=" + treeType + "]";
  }

}
