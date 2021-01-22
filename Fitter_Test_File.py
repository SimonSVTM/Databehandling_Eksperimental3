from Data_Computing import Datarefactor as data_refactor
from Data_Computing import PlotterLayout as plot_layout
from Data_Computing import PlotterTypes as plotter_types
from Data_Computing import Statistics as statistics
from Data_Computing import Fitter as fitter
from Calibration import Calibration as calib
import numpy as np

xmin = 1400
xmax = 1520
ymin = 0.35e6
ymax = 1.5e6

# Linear parameters y = a * x + b
a = 868.056
b = -737588.156

# Gaussian parameters y = A * exp(-(mu - x)^2 / (2 * a))
A = 865182
mu = 1460.29
var = 14.632

# Normal distributed error on data points:
point_var = (A / 20) ** 2

# Number of data points:
num_points = 100

# Linear function
def model1(x, a, b):
    return a * x + b


# Gaussian plus linear function
def model2(x, a, b, A, mu, var):
    return statistics.gaussian(x, A, mu, var) + model1(x, a, b)


# Random uncertainty on each point:
rand_norm_dist = np.random.normal(0, np.sqrt(point_var), num_points)

xs = np.linspace(xmin, xmax, num_points)


def plot_linear_simulation_fit():
    norm_lin = model1(xs, a, b) + rand_norm_dist
    vars = np.repeat(point_var, num_points)
    plotter_types.plotErrorbars(ax, [xs, norm_lin], vars, marker_size=3, label="Randomly generated")

    plotter_types.plotFit(ax, data=[xs, norm_lin], vars=vars, model=model1, guess=[a, b],
                          fit_color='darkred')


def plot_gauss_plus_linear_simulation_fit():
    norm_lin = model2(xs, a, b, A, mu, var) + rand_norm_dist
    vars = np.repeat(point_var, num_points)
    plotter_types.plotErrorbars(ax, [xs, norm_lin], vars, marker_size=3, label="Randomly generated")

    popt, pcov = plotter_types.plotFit(ax, data=[xs, norm_lin], vars=vars, model=model2, guess=[a, b, A, mu, var],
                                       fit_color='darkred')
    a_new = popt[0]
    b_new = popt[1]
    plotter_types.plotAsLine(ax, [xs, a_new * xs + b_new], line_color='red')


ax = plot_layout.start_plot(7, 4)
print("\n Line fit:")
plot_linear_simulation_fit()
plot_layout.setup_plot(ax, xlabel='Energy [keV]', ylabel='Count', hasLegend=True, yaxis_sciNotation=True, xmin=xmin,
                       xmax=xmax, ymin=ymin, ymax=ymax)

ax = plot_layout.start_plot(7, 4)

print("\n Line and Gaussian fit:")
plot_gauss_plus_linear_simulation_fit()
plot_layout.setup_plot(ax, xlabel='Energy [keV]', ylabel='Count', hasLegend=True, yaxis_sciNotation=True, xmin=xmin,
                       xmax=xmax, ymin=ymin, ymax=ymax)
plot_layout.show_plot()
