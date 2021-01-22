import numpy as np

####################### Data Processiong_Algorithms #######################

class data_processing_algorithms:

    # Removes zeros, used in getNormalizedNpyData
    @staticmethod
    def noZeros(array1, array2):
        return data_processing_algorithms.reduce(array1, array2, lambda x: 0 < x)


    # Trims data, used in getGaussianFit
    @staticmethod
    def trim(array1, array2, xmin, xmax):
        return data_processing_algorithms.reduce(array1, array2, lambda x: xmin < x < xmax)

    #Reduce array based on other array, and a boolean function.
    @staticmethod
    def reduce(array1, array2, bool_func):
        if len(array1) != len(array2): raise ValueError('Arrays must be same size.')
        return np.array([array1[i] for i in range(len(array2)) if bool_func(array2[i])])

    #Binary Search
    @staticmethod
    def binary_search(arr, x, low):
        high = len(arr)
        while low < high:
            if high == low + 1:
                return high - 1
            mid = int((high + low) / 2)
            if x == arr[mid]:
                return mid
            elif x < arr[mid]:
                high = mid
            else:
                low = mid

    # Compares data0 and data1 by pairing their y - values for given x-values.
    @staticmethod
    def compare_data(data0, var0, data1, var1):
        data_compared = [[], [], []]
        index = 0
        for i in range(len(data0[0])):
            channel = data0[0][i]
            low = index
            index = data_processing_algorithms.binary_search(data1[0], channel, low)
            if index < len(data1[0]):
                data_compared[0].append(channel)
                data_compared[1].append([data1[1][index], data0[1][i]])
                data_compared[2].append([var1[index], var0[i]])
        data_compared = [np.array(data_compared[0]), np.array(data_compared[1]), np.array(data_compared[2])]
        return data_compared




