package de.unikoblenz.west.cep.measurementProcessor.listeners;

import de.uni_koblenz.west.koral.common.query.parser.QueryExecutionTreeType;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class ExtendedQuerySignature extends QuerySignature {

  public final int queryId;

  public final int repetition;

  public ExtendedQuerySignature(int queryId, String queryFilename, QueryExecutionTreeType treeType,
          int repetition) {
    super(queryFilename, treeType);
    this.queryId = queryId;
    this.repetition = repetition;
  }

  public QuerySignature getBasicSignature() {
    return new QuerySignature(queryFileName, treeType);
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = (prime * result) + queryId;
    result = (prime * result) + ((queryFileName == null) ? 0 : queryFileName.hashCode());
    result = (prime * result) + repetition;
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
    ExtendedQuerySignature other = (ExtendedQuerySignature) obj;
    if (queryId != other.queryId) {
      return false;
    }
    if (queryFileName == null) {
      if (other.queryFileName != null) {
        return false;
      }
    } else if (!queryFileName.equals(other.queryFileName)) {
      return false;
    }
    if (repetition != other.repetition) {
      return false;
    }
    if (treeType != other.treeType) {
      return false;
    }
    return true;
  }

  @Override
  public String toString() {
    return "QuerySignature [queryId=" + queryId + ", queryFile=" + queryFileName + ", treeType="
            + treeType + ", repetition=" + repetition + "]";
  }

}
