from Calibration import Calibration as cal
from Statistics import Statistics as stat
from Fitter import Fitter as fit
import numpy as np

####################### PLOT TYPES #######################

class PlotterTypes:



    '''
    Function plotAsLine: Plot data as Line.
    Parameters:
    ax, data: See plotAsHistogram.
    line_color | String: Color of the line.
    '''

    @staticmethod
    def plotAsLine(ax, data, **kwargs):
        line_color = kwargs.get('line_color', 'k')
        isCalibrated = kwargs.get('isCalibrated', False)
        label = kwargs.get('label', '')
        data_cal = cal.getCalibratedData(data, isCalibrated)
        ax.plot(data_cal[0], data_cal[1], color = line_color, label = label) # A line plot

    @staticmethod
    def plotGaussianWithLine(ax, popt, **kwargs):
        line_color = kwargs.get('line_color', 'k')
        label = kwargs.get('label', '')
        xmin = kwargs.get('xmin', 0)
        xmax = kwargs.get('xmax', 100)
        xs = np.linspace(xmin, xmax, int((xmax - xmin) * 100))
        ax.plot(xs, popt[0] * xs + popt[1] +  stat.gaussian(xs, popt[2], popt[3], popt[4]), color=line_color, label=label)  # A line plot
    '''
    Function plotWithError: Plot as points with errorbars.
    Parameters:
    ax | line2D object : The pyplot object the data will be plotted in. Get from startPlot().
    data | [np.array(...), np.array(...), ...]: Data to be plotted. 
    var | Array: The variance array of the y-data. Notice len(var) == len(y)
    marker_color | String: Color of error bars and points.
    marker_size | Integer: Size of marker.
    isCalibrated | Boolean: If data should be calibrated when plotted.
    Returns: The unchanged 'var' parameter.
    '''

    @staticmethod
    def plotErrorbars(ax, data, var, **kwargs):
        marker_color = kwargs.get('marker_color', 'k')
        marker_size = kwargs.get('marker_size', 5)
        isCalibrated = kwargs.get('isCalibrated', False)
        label = kwargs.get('label', '')

        data_cal = cal.getCalibratedData(data, isCalibrated)

        ax.errorbar(data_cal[0], data_cal[1], yerr = np.sqrt(var), color=marker_color, marker = 'o', linestyle = 'none', markersize = marker_size, label = label)
        return var


    '''
    Function plotWithPoissonError: Plot as points with errorbars.
    Parameters:
    ax, data: See plotErrorbars.
    var | Array: The variance array of the y-data. Notice len(var) == len(y)
    Others: See plotErrorbars
    Returns: The poisson distributed 'var' parameter.
    '''

    @staticmethod
    def plotPoissonErrorbars(ax, data, **kwargs):
        norm_factor = kwargs.get('norm_factor', 1)
        var = stat.getPoissonVariance(data, norm_factor)
        PlotterTypes.plotErrorbars(ax, data, var, **kwargs)
        return var


    '''
    Function plotGaussianFit: Fits n gaussians to some data points, given the unceartainties on them.
    
    Input parameters:
    ax | line2D object : The pyplot object the data will be plotted in. Get from startPlot().
    data | [np.array(...), np.array(...), ...]: Data to be plotted. 
    var | Array: The variance array of the y-data. Notice len(var) == len(y)
    guess | Array: Guess - parameters for gaussian fit. Notice len(guess) = 3 * n
    
    Returns: Fitted parameters for gaussians, and the covariance matrix.
    '''
    @staticmethod
    def plotGaussianFit(ax, data, var, guess, **kwargs):
        isCalibrated = kwargs.get('isCalibrated', False)
        if isCalibrated: return PlotterTypes.plotFit(ax, data, var, lambda X, *args: stat.gaussian_sum(X, *args), guess, cal_map = getGaussianCalMap(), **kwargs)
        return PlotterTypes.plotFit(ax, data, var, lambda X, *args: stat.gaussian_sum(X, *args), guess, **kwargs)



    '''
    Function plotLinearFit: Fits line to some data points, given the unceartainties on them.
    
    Input parameters:
    ax | line2D object : The pyplot object the data will be plotted in. Get from startPlot().
    data | [np.array(...), np.array(...), ...]: Data to be plotted. 
    var | Array: The variance array of the y-data. Notice len(var) == len(y)
    guess | Array [a, b]: Guess - parameters for linear fit
    
    Returns: Fitted parameters for line, and the covariance matrix.
    '''

    @staticmethod
    def plotLinearFit(ax, data, var, guess, **kwargs):
        isCalibrated = kwargs.get('isCalibrated', False)
        if isCalibrated: return PlotterTypes.plotFit(ax, data, var, lambda X, a, b: a * X + b, guess, cal_map = cal.getLinearCalMap(), **kwargs)
        return PlotterTypes.plotFit(ax, data, var, lambda X, a, b: a * X + b, guess, **kwargs)


    '''
    Function plotGaussianFit: Fits n gaussians to some data points, given the unceartainties on them.
    
    Input parameters:
    data | [x, y, ...], with x and y being array: Data to be fitted.
    ax | line2D object : The pyplot object the data will be plotted in. Get from startPlot().
    var | Array: The variance array of the y-data. Notice len(var) == len(y)
    fit_color | String: color of pitted line.
    xmin, xmax | Integers: Minimum and maximum x-value for plot.
    guess | Array: Guess - parameters for fit. 
    cal_map | Map: Calibration map of fit parameters. Default, no calibration.
    cal_offset | Integer: Offset of cal_map, default 0.
    
    Returns: Fitted parameters for gaussians, and the covariance matrix.
    '''
    @staticmethod
    def plotFit(ax, data, vars, model, guess, **kwargs):
        xmin = kwargs.get('xmin', data[0][0])
        xmax = kwargs.get('xmax', data[0][-1])
        fit_color = kwargs.get('fit_color', 'k')
        label = kwargs.get('label', '')

        popt, pcov = fit.getFit(data, vars, model, guess, xmin = xmin, xmax = xmax)

        xs = np.linspace(xmin, xmax, 1000)
        if 'cal_map' in kwargs:
            xs = cal.channel_to_energy(xs)
            popt = cal.getCalibratedParams(popt, **kwargs)
        ys = model(xs, *popt)

        print("Fit Parameters: ", popt)
        print("Fit Uncertainties (NEVER CALIBRATED): ", np.sqrt(np.diag(pcov)))

        ax.plot(xs, ys, color=fit_color, label = label)
        return popt, pcov
