from DPA import data_processing_algorithms as data_processing_algorithms
from scipy.optimize import curve_fit
import numpy as np

####################### FITTING AND TESTING #######################

class Fitter:

    '''
    Function getFit: Fits model to data.

    Input parameters:
    data | [x, y, ...], with x and y being array: Data to be fitted.
    var | Array: The variance array of the y-data. Notice len(var) == len(y)
    xmin, xmax | Integers: Minimum and maximum x-value for fit.
    guess | Array: Guess - parameters

    Returns: Fitted parameters for the model, and the covariance matrix.
    '''
    @staticmethod
    def getFit(data, vars, model, guess, **kwargs):
        xmin = kwargs.get('xmin', data[0][0])
        xmax = kwargs.get('xmax', data[0][-1])
        data = data.copy()
        if len(data[1]) != len(vars): raise ValueError("Length of variance array does not match length of y-data.")
        vars     = data_processing_algorithms.trim(vars, data[0], xmin, xmax)
        data[1] = data_processing_algorithms.trim(data[1], data[0], xmin, xmax)
        data[0] = data_processing_algorithms.trim(data[0], data[0], xmin, xmax)

        data[1] = data_processing_algorithms.noZeros(data[1], vars)
        data[0] = data_processing_algorithms.noZeros(data[0], vars)
        vars     = data_processing_algorithms.noZeros(vars, vars)

        if data[0] == [] or data[1] == []:
            raise Exception('Tried to fit with empty data: [xmin,xmax] lies outside x-value for the data points.')
        popt, pcov =  curve_fit(model, data[0], data[1], p0=guess, sigma=np.sqrt(vars), absolute_sigma=True)
        return popt, pcov

