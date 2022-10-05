import re
import time

import pandas as pd
from PySide6.QtCore import QObject, Signal

from app_functions import timeit
from features import Features


class CSVReadWorker(QObject):
    """
    CSV Reader Worker in a thread
    """
    readCompleted = Signal(pd.DataFrame, float)
    finished = Signal()

    def __init__(self, csvfile):
        super().__init__()
        self.csvfile = csvfile

    def run(self):
        time_start = time.time()

        df = pd.read_csv(self.csvfile)

        time_end = time.time()
        elapsed = (time_end - time_start)
        self.readCompleted.emit(df, elapsed)
        self.finished.emit()


class ParseFeaturesWorker(QObject):
    """
    Parse Feature Worker in a thread
    """
    parseCompleted = Signal(Features, float)
    finished = Signal()

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df

    def run(self):
        time_start = time.time()

        features = Features(self.df)

        time_end = time.time()
        elapsed = (time_end - time_start)
        self.parseCompleted.emit(features, elapsed)
        self.finished.emit()
