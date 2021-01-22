import matplotlib.pyplot as plt
####################### PLOTTING LAYOUT #######################

class PlotterLayout:
    '''
    Function startPlot: Begin a new plot session, with width X height window size.
    Parameters:
    width, height | Positive Integers: Width and height of the plot window.
    Returns: ax, the plotting object that can be plotted on.
    '''

    @staticmethod
    def start_plot(width, height):
        if width <= 0 or height <= 0: raise ValueError('Height and width of plot must be positve')
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif', size=16)
        fig, ax = plt.subplots(1, 1, figsize=(width, height))
        plt.subplots_adjust(left=0.11, bottom=0.15, right=0.95, top=0.9)
        return ax


    ''' 
    Function setup_plot: Setup plot window
    Parameters:
    xmax, xmax, ymin, ymax | Positive Integer: The maximal x-value and y-value for the axis.
    title | String: title of the plot.
    xlabel, ylabel | String: Label on x- and y- axis.
    logarithmic_scale | Boolean: True if the yaxis should be logarithmic.
    '''

    @staticmethod
    def setup_plot(ax, **kwargs):
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()

        xmin = kwargs.get('xmin', x0)
        xmax = kwargs.get('xmax', x1)
        ymin = kwargs.get('ymin', y0)
        ymax = kwargs.get('ymax', y1)
        xlabel = kwargs.get('xlabel', 'x-axis')
        ylabel = kwargs.get('ylabel', 'y-axis')
        title = kwargs.get('title', '')
        hasLegend = kwargs.get('hasLegend', False)
        log_scale = kwargs.get('log_scale', False)
        yaxis_sciNotation = kwargs.get('yaxis_sciNotation', False)
        if log_scale: plt.yscale('log')
        else: plt.yscale('linear')
        plt.title(title)
        if yaxis_sciNotation:
            plt.ticklabel_format(axis='y', style='sci', scilimits=(6, 6))

        plt.xlim(xmin, xmax)
        plt.ylim(ymin, ymax)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)


        if hasLegend: ax.legend()


    #Shows all plots. Shall only be used in the last non-empty line of your code.
    @staticmethod
    def show_plot(): plt.show()
