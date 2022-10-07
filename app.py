#!/usr/bin/env python
# coding: utf-8
import os
import sys
import pandas as pd
import warnings

from pathlib import Path
from PySide6.QtCore import (
    Qt,
    QThread,
)
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QStatusBar,
    QStyle,
    QTabWidget,
)

from app_functions import timeit, getAppLogger
from app_thread import CSVReadWorker, ParseFeaturesWorker
from app_widgets import WorkInProgress, LogConsole, VBoxLayout
from dcp_creator_toolbar import DCPCreatorToolBar
from dcp_sensor_selection import DCPSensorSelection
from dcp_stats_selection import DCPStats
from dcp_step_value_setting import DCPStepValueSetting
from dcp_summary import DCPSummary
from features import Features
from ui_controller import UIController

warnings.simplefilter('ignore', FutureWarning)


class DCPCreator(QMainWindow):
    """DCP creator with the CSV file exported from the fleet analysis tool
    """
    __version__ = '0.0.1'
    __version_minor__ = '20221006'

    # UI components
    console: LogConsole = None
    tab: QTabWidget = None
    toolbar: DCPCreatorToolBar = None
    statusbar: QStatusBar = None
    controller: UIController = None

    features: Features = None
    page = dict()

    # directory location
    opendir: str = None

    # thread instances
    reader: CSVReadWorker = None
    parser: ParseFeaturesWorker = None
    thread_reader: QThread = None
    thread_parser: QThread = None

    # progressbar
    progress_reader: WorkInProgress = None
    progress_parser: WorkInProgress = None

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(1000, 600)
        self.setWindowTitle('DCP Creator')
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        )

    def button_open_clicked(self):
        """Action for 'Open' button clicked.
        """
        # only at the first time to open
        if self.opendir is None:
            self.opendir = str(Path.home())
        selection = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select CSV file',
            dir=self.opendir,
            filter='Zip File (*.zip);; CSV File (*.csv)'
        )
        csvfile = selection[0]
        if len(csvfile) > 0:
            # remember directory location
            self.opendir = os.path.dirname(csvfile)
            self.console.insertIn('reading %s.' % csvfile)
            self.read_csv(csvfile)

    def read_csv(self, csvfile: str):
        """Read CSV file in a thread.

        Parameters
        ----------
        csvfile: str
        """
        if not os.path.exists(csvfile):
            return pd.DataFrame()
        # _____________________________________________________________________
        # Prep. Threading
        self.reader = CSVReadWorker(csvfile)
        self.thread_reader = QThread(self)
        self.reader.moveToThread(self.thread_reader)
        # Controller
        self.thread_reader.started.connect(self.reader.run)
        self.reader.finished.connect(self.thread_reader.quit)
        self.reader.finished.connect(self.reader.deleteLater)
        self.thread_reader.finished.connect(self.thread_reader.deleteLater)
        self.reader.readCompleted.connect(self.read_csv_completed)
        # Start Threading
        self.thread_reader.start()
        self.progress_reader = WorkInProgress(self, 'Reading ...')
        self.progress_reader.show()

    def read_csv_completed(self, df: pd.DataFrame, elapsed: float):
        """Event handler when thread of read_csv is completed.

        Parameters
        ----------
        df: pd.DataFrame
        """
        self.progress_reader.cancel()
        self.console.insertCompleted(elapsed)
        self.console.insertIn('Parsing data.')
        self.parse_features(df)

    def parse_features(self, df: pd.DataFrame):
        """Parser for exported summary statistics (feature) in dataframe.

        Parameters
        ----------
        df: pd.DataFrame
        """
        # _____________________________________________________________________
        # Prep. Threading
        self.parser = ParseFeaturesWorker(df)
        self.thread_parser = QThread(self)
        self.parser.moveToThread(self.thread_reader)
        # Controller
        self.thread_parser.started.connect(self.parser.run)
        self.parser.finished.connect(self.thread_parser.quit)
        self.parser.finished.connect(self.parser.deleteLater)
        self.thread_parser.finished.connect(self.thread_parser.deleteLater)
        self.parser.parseCompleted.connect(self.parse_features_completed)
        # Start Threading
        self.thread_parser.start()
        self.progress_parser = WorkInProgress(self, 'Parsing ...')
        self.progress_parser.show()

    def parse_features_completed(self, features: Features, elapsed: float):
        """Event handler when thread of parse_feature is completed.

        Parameters
        ----------
        features: Features
        """
        self.progress_parser.cancel()
        # Log
        self.console.insertCompleted(elapsed)
        self.console.insertOut(features.getLogDfShape())
        self.console.insertOut(features.getLogStep())
        self.console.insertOut(features.getLogStat())
        #
        self.features = features
        self.main_ui()

    def button_save_clicked(self):
        """Action for 'Save' button clicked.
        """
        if self.controller is None:
            print('There is no data!')
            return
        selection = QFileDialog.getSaveFileName(
            parent=self,
            caption='Specify name of JSON file to save',
            dir='dcp.json',
            filter='JSON File (*.json)'
        )
        jsonfile = selection[0]
        if len(jsonfile) > 0:
            self.controller.saveJSON4DCP(jsonfile)

    def closeEvent(self, event):
        """Close event handling.

        Parameters
        ----------
        event: QCloseEvent
        """
        print('Exiting application ...')
        event.accept()

    def init_ui(self):
        """Initialize UI
        """
        # _____________________________________________________________________
        # Toolbar
        self.toolbar = DCPCreatorToolBar()
        self.toolbar.openClicked.connect(self.button_open_clicked)
        self.toolbar.saveClicked.connect(self.button_save_clicked)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        # _____________________________________________________________________
        # Statusbar
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        self.console = LogConsole()
        statusbar.addWidget(self.console, stretch=1)

    def main_ui(self):
        """Main UI
        """
        # remove central widget if exists.
        self.takeCentralWidget()
        # make new tab widget
        self.tab = tab = QTabWidget()
        self.setCentralWidget(tab)
        # page creation to be added to tab
        page = {
            'summary': DCPSummary(self.features),
            'sensors': DCPSensorSelection(self.features),
            'recipe': DCPStepValueSetting(self.features),
            'stats': DCPStats(self.features)
        }
        # tab creation
        self.tab.addTab(page['summary'], 'Summary')
        self.tab.addTab(page['sensors'], 'Sensor Selection')
        self.tab.addTab(page['recipe'], 'Setting Data')
        self.tab.addTab(page['stats'], 'Summary Stats')
        # _____________________________________________________________________
        # for tab click event
        self.tab.currentChanged.connect(self.tab_changed)
        # _____________________________________________________________________
        # Controller for tab and other UI interaction
        self.controller = UIController(page)

    def tab_changed(self):
        """Event handler for tab changed
        """
        tab: QTabWidget = self.sender()
        idx = tab.currentIndex()
        if idx == 0:
            self.controller.updateFeatures()
        print('current tab', idx)


def main():
    """Main Event Loop
    """
    app: QApplication = QApplication(sys.argv)
    ex = DCPCreator()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
