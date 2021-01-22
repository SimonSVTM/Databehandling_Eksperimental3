import numpy as np
####################### STATISTICS #######################
class Statistics:

    '''
    Function gaussian_sum: Sum over n gaussians at some value x.
    Parameters:
    X | Float: Input parameter
    n | Positive Integer: Number of gaussians summed.
    *args | Tuple or List: Arguments passed in Altitude, Mean and Variance. Notice len(*args) == 3 * n.
    '''

    @staticmethod
    def gaussian_sum(X, *args):
        n = int(len(args) / 3)
        if n == 0: return 0
        if n < 0: raise ValueError("n must be postive.")
        if isinstance(args[0], list) or isinstance(args[0], np.ndarray): args = args[0]
        if len(args) != 3 * n: raise ValueError(
            "Number of arguments must be equal to three times the number of Gaussians.")

        return sum([Statistics.gaussian(X, args[3 * i], args[3 * i + 1], args[3 * i + 2]) for i in range(0, n)])

    '''
    Function gaussian: Returns the gaussian value for some value x.
    Parameters:
    X | float or array-like: Input
    A, mu, var | float: Amplitude, Mean and Variance parameters.
    '''

    @staticmethod
    def gaussian(X, A, mu, var):
        return abs(A) * np.exp(-(np.array(X) - mu) ** 2 / (2 * abs(var)))

    '''
    Function getPoissonVariance: Returns possion errors for normalized data.
    Parameters:
    data | [xdata, ydata, normalization factor]
    '''
    @staticmethod
    def getPoissonVariance(data, norm_factor):
        if len(data) != 2: raise ValueError("Length of data must be two: xData, yData")
        return data[1] * norm_factor  # var_(N * a) = var_N * a^2 = N * a^2 = n * a, with n normalized, var_N = N.

    @staticmethod
    def background(X, A, mu, var):
        return abs(A) * np.exp(-(np.array(X) - mu) ** 2 / (2 * abs(var)))
