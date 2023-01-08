import os
import time
import zipfile

import pandas as pd
from PySide6.QtCore import QObject, Signal, QThread, QEventLoop

from app_widgets import WorkInProgress


class ReadCSV(QObject):
    readCompleted = Signal(pd.DataFrame)

    def __init__(self):
        super().__init__()
        self.event_loop = None
        self.progress_reader = None
        self.thread_reader = None
        self.reader = None

    def read(self, csvfile: str):
        """Read CSV file in a thread.

        Parameters
        ----------
        csvfile: str
        """
        # check if csvfile exists
        if not os.path.exists(csvfile):
            return pd.DataFrame()
        # check contents of csvfile if the file is zip file
        ext = os.path.splitext(csvfile)[1]
        if ext == '.zip':
            zip_f = zipfile.ZipFile(csvfile)
            list_file = zip_f.namelist()
            zip_f.close()
            for name_file in list_file:
                print('- %s' % name_file)
            if len(list_file) > 1:
                return
        # _____________________________________________________________________
        # Prep. Threading
        self.reader = CSVReadWorker(csvfile)
        self.thread_reader = QThread(parent=self)
        self.reader.moveToThread(self.thread_reader)
        # Controller
        self.thread_reader.started.connect(self.reader.run)
        self.reader.finished.connect(self.thread_reader.quit)
        self.reader.finished.connect(self.reader.deleteLater)
        self.thread_reader.finished.connect(self.thread_reader.deleteLater)
        self.reader.readCompleted.connect(self.read_csv_completed)
        # Start Threading
        self.thread_reader.start()
        self.progress_reader = WorkInProgress('Reading ...')
        self.progress_reader.show()
        # Event Loop
        self.event_loop = QEventLoop()
        self.event_loop.exec()

    def read_csv_completed(self, df: pd.DataFrame, elapsed: float):
        """Event handler when thread of read_csv is completed.

        Parameters
        ----------
        df: pd.DataFrame
        elapsed: elapsed seconds to read
        """
        self.progress_reader.cancel()
        self.readCompleted.emit(df)
        self.event_loop.quit()
        print('elapsed %f sec' % elapsed)


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
