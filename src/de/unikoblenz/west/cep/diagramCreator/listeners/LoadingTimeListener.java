package de.unikoblenz.west.cep.diagramCreator.listeners;

import de.erichseifert.gral.data.DataSource;
import de.erichseifert.gral.data.DataTable;
import de.erichseifert.gral.graphics.Insets2D;
import de.erichseifert.gral.io.data.DataWriter;
import de.erichseifert.gral.io.data.DataWriterFactory;
import de.erichseifert.gral.io.plots.DrawableWriter;
import de.erichseifert.gral.io.plots.DrawableWriterFactory;
import de.erichseifert.gral.plots.BarPlot;
import de.erichseifert.gral.plots.BarPlot.BarRenderer;
import de.erichseifert.gral.plots.Plot;
import de.erichseifert.gral.plots.XYPlot;
import de.uni_koblenz.west.koral.master.graph_cover_creator.CoverStrategyType;
import de.unikoblenz.west.cep.diagramCreator.DiagramListener;
import de.unikoblenz.west.cep.diagramCreator.OutputFormat;

import java.awt.Color;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

/**
 * @author Daniel Janke &lt;danijankATuni-koblenz.de&gt;
 *
 */
public class LoadingTimeListener implements DiagramListener {

  private OutputFormat outputFormat;

  private int width;

  private int height;

  private String outputDataFilePrefix;

  private DataTable dataTable;

  @SuppressWarnings("unchecked")
  @Override
  public void setUp(OutputFormat format, int width, int height, File outputDir) {
    outputDataFilePrefix = outputDir.getAbsolutePath() + File.separator + "loadingTime";
    outputFormat = format;
    this.width = width;
    this.height = height;
    dataTable = new DataTable(String.class, Long.class);
    // TODO Auto-generated method stub

  }

  @Override
  public void process(String[] parts) {
    process(CoverStrategyType.valueOf(parts[0]), Integer.parseInt(parts[1]),
            Long.parseLong(parts[2]), Long.parseLong(parts[3]), Long.parseLong(parts[4]),
            Long.parseLong(parts[5]));
  }

  protected void process(CoverStrategyType cover, int nHopReplication, long coverCreationTime,
          long encodingTime, long transferTime, long indexingTime) {
    dataTable.add((nHopReplication > 0 ? nHopReplication + "_HOP_" : "") + cover.name(),
            coverCreationTime);
  }

  @Override
  public void tearDown() {
    writeData(dataTable, outputDataFilePrefix + ".csv");
    BarPlot plot = new BarPlot(dataTable);
    double insetsTop = 20.0, insetsLeft = 60.0, insetsBottom = 60.0, insetsRight = 40.0;
    plot.setInsets(new Insets2D.Double(insetsTop, insetsLeft, insetsBottom, insetsRight));
    plot.setBarWidth(0.75);
    plot.setLegendVisible(true);
    plot.getAxisRenderer(XYPlot.AXIS_X).setTicksVisible(false);

    BarRenderer barRenderer = (BarRenderer) plot.getPointRenderers(dataTable).get(0);
    barRenderer.setColor(Color.LIGHT_GRAY);
    // TODO Auto-generated method stub
    drawPlot(plot, new File(outputDataFilePrefix + "." + outputFormat.toString().toLowerCase()),
            width, height);
  }

  private void writeData(DataSource data, String filename) {
    DataWriterFactory factory = DataWriterFactory.getInstance();
    DataWriter writer = factory.get("text/tab-separated-values");
    try (FileOutputStream dataStream = new FileOutputStream(filename);) {
      writer.write(data, dataStream);
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
  }

  private void drawPlot(Plot plot, File outputFile, int width, int height) {
    DrawableWriter wr = DrawableWriterFactory.getInstance().get(outputFormat.mimeType);
    try (OutputStream out = new BufferedOutputStream(new FileOutputStream(outputFile));) {
      wr.write(plot, out, width, height);
    } catch (IOException e) {
      throw new RuntimeException();
    }
  }

  @Override
  public void close() {
    // TODO Auto-generated method stub

  }

}
