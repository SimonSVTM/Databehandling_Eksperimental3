import numpy as np
from Calibration import Calibration as cal

def Cal_eff(x):
    return 0.67345816 * cal.channel_to_energy(x) ** (-0.81501324)

class CountNode:

    def __init__(self, val):
        self.left = None
        self.right = None
        self.value = val
        self.count = 1


    # Compare the new value with the parent node
    def insert(self, val):
        if val < self.value:
            if self.left:
                self.left.insert(val)
            else:
                self.left = CountNode(val)
        if val > self.value:
            if self.right:
                self.right.insert(val)
            else:
                self.right = CountNode(val)
        if val == self.value: self.count = self.count + 1

    def convertToList(self):
        lst = [np.array([]), np.array([]), np.array([])]
        if self:
            a = CountNode.convertToList(self.left)
            b = [np.array([self.value]), np.array([self.getCalibratedCount()]), np.array([self.getPoissonVar()])]
            c = CountNode.convertToList(self.right)
            lst[0] = np.concatenate((a[0], b[0], c[0]))
            lst[1] = np.concatenate((a[1], b[1], c[1]))
            lst[2] = np.concatenate((a[2], b[2], c[2]))

        return lst

    def getTotalCount(self):
        return self.left.getTotalCount() + self.count + self.right.getTotalCount()

    def setCount(self, count):
        self.count = count

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def getPoissonVar(self):
        sigma_a  = 0.00149674
        sigma_b = 0.00363211
        a = 0.67345816
        b = 0.81501324
        return self.count / Cal_eff(self.value) ** 2* ( 1 + self.count * ((sigma_a / a) ** 2 + (np.log(self.value) * sigma_b) **2) )

    def getCalibratedCount(self):
        return self.count / Cal_eff(self.value)


class TimeNode:
    maxVal = 0
    minVal = 0

    @staticmethod
    def setMinMax(min_val, max_val):
        TimeNode.maxVal = max_val
        TimeNode.minVal = min_val

    def __init__(self, val, time):
        self.left = None
        self.right = None
        self.value = val
        self.times = [time]

    # Compare the new value with the parent node
    def insert(self, val, time):
        # print(TimeNode.minVal, val, TimeNode.maxVal)
        if TimeNode.minVal < val < TimeNode.maxVal:
            if val < self.value:
                if self.left:
                    self.left.insert(val, time)
                else:
                    self.left = TimeNode(val, time)
            if val > self.value:
                if self.right:
                    self.right.insert(val, time)
                else:
                    self.right = TimeNode(val, time)
            if val == self.value: self.times.append(time)

    def convertToList(self):
        lst = [[], []]
        if self:
            a = TimeNode.convertToList(self.left)
            b = [[self.value], [self.times]]
            c = TimeNode.convertToList(self.right)
            lst[0] = a[0] + b[0] + c[0]
            lst[1] = a[1] + b[1] + c[1]

        return lst

    def toCountNode(self, time):
        cn = None
        if self:
            cn = CountNode(self.value)
            cn.setCount(len([t for t in self.times if t < time]))
            cn.setLeft(TimeNode.toCountNode(self.left, time))
            cn.setRight(TimeNode.toCountNode(self.right, time))

        return cn

    def getStateByTime(self, time):
        cn = self.toCountNode(time)
        return cn.convertToList()
