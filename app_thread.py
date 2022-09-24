import pandas as pd
from PySide6.QtCore import QObject, Signal

from app_functions import timeit


class CSVReader(QObject):
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
