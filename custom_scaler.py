from enum import Enum

from sklearn.preprocessing import StandardScaler

class Scale(Enum):
    NONE = 0
    MEAN_SIGMA = 1
    MEDIAN_IQR = 2
    TARGET_TOLERANCE = 3

class CustomScaler(StandardScaler):
    pass