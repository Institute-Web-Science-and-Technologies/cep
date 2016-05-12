package de.unikoblenz.west.cep.diagramCreator;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public enum OutputFormat {

  PNG("image/png"), GIF("image/gif"), JPEG("image/jpeg"), EPS("application/postscript"), PDF(
          "application/pdf"), SVG("image/svg+xml");

  public final String mimeType;

  private OutputFormat(String mimeType) {
    this.mimeType = mimeType;
  }
}
