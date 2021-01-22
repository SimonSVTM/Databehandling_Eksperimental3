# Version 2, 22-11-2020
# Author: Simon S. Villadsen
# Collaborators: Erik Steenberg, Esben J. Porat & Kasper Larsen.
import numpy as np
from os import listdir
from Nodes import CountNode as cnode
from Nodes import TimeNode as tnode


class Datarefactor:
    def __init__(self):
        pass

    '''
    Function getNpyData: This method retrives the data necesary for data analysis.

    Parameters:
    type | String : The type of the data. See function for more information.
    metatype | String : The metatype of the data. If for example you want to get calibration data for Cs, the metatype is 'Cs'.
    data_folder | String : The folder where the data is located. Can be absolute or relative path.

    Returns: List of times & List of channels.
    '''
    # For example if you want to load 'Cal_Am', the type is 'Calibration' and the metatype is 'Am'.
    # If a .txt file is not availiable in .npy format, the code creates the .npy file, and loads it afterwards.
    @staticmethod
    def getNpyData(type, metatype, data_folder):
        TYPE = {
            'Calibration': 'Cal',
            'Manganese': 'Mn56',
        }[type]

        search = TYPE + '_' + metatype
        result = []

        # Iteration through the source dictionary
        for f in listdir(data_folder):
            # Only accept .npy files and files matching the search name.

            if all(search[i] == f[i] for i in range(len(search))):
                print(f, search)
                result.append(data_folder + '/' + f)
        if len(result) == 0: raise FileNotFoundError("Could not retrive data.")

        texts = [file for file in result if file[-4:] == '.txt']
        if len(texts) != 1: raise ImportError("Multiple or no .txt files were found with that type and metatype.")
        text = texts[0]

        for file in result:
            if file[-4:] == '.npy':
                data = list(np.load(file))

                print('Loaded data: ' + file)
                return data    #Returns data, with factor 1.

        # Converts .mca to .npy and saves .npy:
        if text[-4:] == '.txt':
            data = np.loadtxt(text, skiprows= 4)
            data = data[::3]
            datax = np.array([x[0] for x in data])
            datay = np.array([x[1] for x in data])
            np.save(text[:-4], [datax, datay])
        else: raise TypeError('File found was not .txt format.')

        return Datarefactor.getNpyData(type, metatype, data_folder)

    '''
    Function convertToHistogram: This method counts occurences, and outputs as histogram data.
    
    Parameters:
    data | list of arrays : Data to be converted.
    column | int : Which column of the data, should be converted. Default column zero.
    '''
    @staticmethod
    def convertToHistogram(data, **kwargs):
        column = kwargs.get('column', 0)

        if (0 <= column < len(data)):
            ds = data[column]
            xmin = kwargs.get('xmin', ds[0])
            xmax = kwargs.get('xmax', ds[-1])
            root = cnode(ds[0])
            for d in ds:
                if xmin < d < xmax:
                    root.insert(d)
            return root.convertToList()
        else: raise ValueError("Column index given out of bounds.")

    @staticmethod
    def getTimeNode_root(data, xmin, xmax):
        tnode.setMinMax(xmin, xmax)
        times = data[0]
        channels = data[1]
        for i in range(len(channels)):
            if xmin < channels[i] < xmax:
                root = tnode(channels[i], times[i])
                break

        for i in range(len(channels)):
            root.insert(channels[i], times[i])
        return root










