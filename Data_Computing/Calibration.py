
####################### CALIBRATION #######################
class Calibration:
    # Calibration Function.
    @staticmethod
    def channel_to_energy(X):
        params = Calibration.getCalibParams()
        return params[0] * X + params[1]

    @staticmethod
    def getCalibParams():
        return [0.7375794152678393, 0.8623567575598811]

    # Calibrates x-axis of data.
    @staticmethod
    def getCalibratedData(data, isCalibrated):
        data_cal = data.copy()
        if isCalibrated:
            data_cal[0] = Calibration.channel_to_energy(data_cal[0])
        return data_cal

    # Generalization of calibration of parameters
    # cal_offset | Integer: Offset of cal_map, default 0.
    @staticmethod
    def getCalibratedParams(params, cal_map, **kwargs):
        cal_offset = kwargs.get('cal_offset', 0)
        repeat = len(cal_map) - cal_offset
        i = 0
        while (i < len(params)):
            if i < cal_offset: f = cal_map[i]
            else: f = cal_map[cal_offset + ((i - cal_offset) % repeat)]
            params[i] = f(params[i])
            i += 1

        return params

    @staticmethod
    def getLinearCalMap():
        return [lambda x: x / Calibration.getCalibParams()[0], lambda x: x]

    @staticmethod
    def getGaussianCalMap():
        return [lambda x: x, lambda x: Calibration.channel_to_energy(x), lambda x: Calibration.getCalibParams()[0] ** 2 * x]



