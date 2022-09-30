import re

import pandas as pd
from PySide6.QtCore import QObject, Signal

from app_functions import timeit
from features import Features


class CSVReadWorker(QObject):
    """
    CSV Reader Worker in a thread
    """
    readCompleted = Signal(pd.DataFrame)
    finished = Signal()

    def __init__(self, csvfile):
        super().__init__()
        self.csvfile = csvfile

    @timeit
    def run(self):
        df = pd.read_csv(self.csvfile)
        self.readCompleted.emit(df)
        self.finished.emit()


class ParseFeaturesWorker(QObject):
    """
    Parse Feature Worker in a thread
    """
    parseCompleted = Signal(Features)
    finished = Signal()

    def __init__(self, df: pd.DataFrame):
        super().__init__()
        self.df = df

    @timeit
    def run(self):
        features = Features(self.df)
        self.parseCompleted.emit(features)
        self.finished.emit()
