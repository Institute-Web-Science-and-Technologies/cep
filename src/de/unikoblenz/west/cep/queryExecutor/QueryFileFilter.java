package de.unikoblenz.west.cep.queryExecutor;

import java.io.File;
import java.io.FileFilter;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class QueryFileFilter implements FileFilter {

  @Override
  public boolean accept(File pathname) {
    return pathname.isFile() && pathname.getName().endsWith(".sparql");
  }

}
