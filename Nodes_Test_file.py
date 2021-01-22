from Data_Computing import Datarefactor as data_refactor
from Data_Computing import PlotterLayout as plot_layout
from Data_Computing import PlotterTypes as plotter_types

import numpy as np


xmin = 1420
xmax = 1520
ymin = -1e4
ymax = 3e5

# Gaussian parameters y = exp(-(mu - x)^2 / (2 * a))
mu = 1460.29
var = 14.632

N = 5000
# Two [Times, Channels] random datasets:
channels_at_time1 = list(zip(*[(i + np.random.normal(0, 1), np.floor(np.random.normal(mu, np.sqrt(var)))) for i in range(N)]))
channels_at_time2 = list(zip(*[(i + np.random.normal(0, 1), np.floor(np.random.normal(mu + 20, np.sqrt(var)))) for i in range(N)]))

timeNode_root1 = data_refactor.getTimeNode_root(channels_at_time1, xmin, xmax)
timeNode_root2 = data_refactor.getTimeNode_root(channels_at_time2, xmin, xmax)

def plot_gaussian_sim(ax, timeNode_root, label, color):
    # Get state at final time N:
    hist_data = timeNode_root.getStateByTime(N)
    # Get state at quarter final time N / 4:
    hist_data_q = timeNode_root.getStateByTime(N / 4)

    # Assumed poisson distributed:
    vars = hist_data[1]
    plotter_types.plotErrorbars(ax, hist_data, vars, marker_size=2, marker_color=color, label = label)
    vars_q = hist_data_q[1]
    plotter_types.plotErrorbars(ax, hist_data_q, vars_q, marker_size=2, marker_color=color)


ax = plot_layout.start_plot(10, 6)


plot_gaussian_sim(ax, timeNode_root1, "Random Sample 1", "r")
plot_gaussian_sim(ax, timeNode_root2, "Random Sample 2", "b")


plot_layout.setup_plot(ax, xlabel='Energy [keV]', ylabel='Count', hasLegend=True, yaxis_sciNotation=True,
                           xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)






plot_layout.show_plot()


