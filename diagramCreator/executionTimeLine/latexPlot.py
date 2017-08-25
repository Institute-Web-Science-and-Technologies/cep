import matplotlib.pyplot as plt
import matplotlib
import math

SPINE_COLOR = 'gray'

def savefig(outputDir, filename):
  plt.savefig(outputDir+'/figure_{}.pgf'.format(filename))
  plt.savefig(outputDir+'/figure_{}.pdf'.format(filename))


def latexify(fig_width=None, fig_height=None, scale=None):
    """Set up matplotlib's RC params for LaTeX plotting.
    Call this before plotting a figure.

    Parameters
    ----------
    fig_width : float, optional, inches
    fig_height : float,  optional, inches
    scale : float, optional, ratio
    """

    # code adapted from http://www.scipy.org/Cookbook/Matplotlib/LaTeX_Examples

    # Width and max height in inches for IEEE journals taken from
    # computer.org/cms/Computer.org/Journal%20templates/transactions_art_guide.pdf

    fig_width_pt = 347.12354#222.0   # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27  # Convert pt to inch

    if fig_width is None:
        fig_width = fig_width_pt*inches_per_pt

    if fig_height is None:
        golden_mean = (math.sqrt(5)-1.0)/2.0    # Aesthetic ratio
        fig_height = fig_width*golden_mean # height in inches

    if scale is not None:
         fig_width = fig_width * scale
         fig_height = fig_height * scale

    fig_height_pt = 549.13828#622.0   # Get this from LaTeX using \the\textheight
    MAX_HEIGHT_INCHES = fig_height_pt*inches_per_pt #8.0
    if fig_height > MAX_HEIGHT_INCHES:
        print("WARNING: fig_height too large: " + str(fig_height) + 
              " so will reduce to " + str(MAX_HEIGHT_INCHES) + " inches.")
        fig_height = MAX_HEIGHT_INCHES

    params = {
      'backend': 'ps',
      "pgf.texsystem": "pdflatex",
      #'text.latex.preamble': ['\usepackage{gensymb}'],
      #'text.latex.preamble': [r'\usepackage{times}\fontfamily{ptm}\selectfont'],
      'axes.labelsize': 10, # fontsize for x and y labels (was 10)
      'axes.titlesize': 10,
      'font.size':       10, # was 10
      'legend.fontsize': 10, # was 10
      'xtick.labelsize': 10,
      'ytick.labelsize': 10,
      'figure.figsize': [fig_width,fig_height],
      'text.usetex': True,
      'text.latex.unicode': True,
      #'text.latex.preamble': ['\\usepackage{times}'],
      'pgf.preamble': ['\\usepackage{times}'],
      'font.family': 'serif',
      'font.serif': ['Times'],
      #'mathtext.rm': 'serif',
      #'mathtext.it': 'serif:italic',
      #'mathtext.bf': 'serif:bold',
      #'mathtext.fontset': 'custom'
    }

    matplotlib.rcParams.update(params)

def format_axes(ax):
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color(SPINE_COLOR)
        ax.spines[spine].set_linewidth(0.5)

    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_tick_params(direction='out', color=SPINE_COLOR)

    return ax
