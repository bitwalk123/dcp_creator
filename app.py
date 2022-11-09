#!/usr/bin/env python
# coding: utf-8
import json
import os
import sys
import zipfile
from collections import OrderedDict

import PySide6
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

from app_thread import CSVReadWorker, ParseFeaturesWorker
from app_widgets import WorkInProgress, LogConsole, DialogWarn, OptionWindow
from app_toolbar import DCPCreatorToolBar
from dcp_experimental import DCPExperimental
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
    __version__ = '0.1.0'
    __version_minor__ = '20221109'

    # UI components
    console: LogConsole = None
    controller: UIController = None
    statusbar: QStatusBar = None
    tab: QTabWidget = None
    toolbar: DCPCreatorToolBar = None

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

    # Option Window
    option_win = None

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(1000, 800)
        self.setWindowTitle('DCP Creator')
        self.setWindowIcon(QIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarMenuButton
        )))
        # Console output
        self.console.insertOut(
            'Python %s' % sys.version
        )
        self.console.insertOut(
            'PySide (Python for Qt) %s' % PySide6.__version__
        )
        self.console.insertOut(
            'DCP Creator %s, %s' % (self.__version__, self.__version_minor__)
        )

    def button_open_csv_clicked(self):
        """Action for 'Open' button clicked.
        """
        # only at the first time to open
        if self.opendir is None:
            self.opendir = str(Path.home())
        # dialog
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

    def button_dcp_read_clicked(self):
        if self.features is None:
            dlg = DialogWarn('At first, please read summary statistics!')
            dlg.exec()
            return
        # default directory to open
        if self.opendir is None:
            self.opendir = str(Path.home())
        # dialog
        selection = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select JSON file',
            dir=self.opendir,
            filter='JSON File (*.json)'
        )
        jsonfile = selection[0]
        if len(jsonfile) > 0:
            self.opendir = os.path.dirname(jsonfile)
            self.controller.readJSON4DCP(jsonfile)

    def button_dcp_save_clicked(self):
        """Action for 'Save' button clicked.
        """
        if self.controller is None:
            print('There is no data!')
            return
        # default directory to open
        if self.opendir is None:
            self.opendir = str(Path.home())
        # dialog
        selection = QFileDialog.getSaveFileName(
            parent=self,
            caption='Specify name of JSON file to save',
            dir=os.path.join(self.opendir, 'dcp.json'),
            filter='JSON File (*.json)'
        )
        jsonfile = selection[0]
        if len(jsonfile) > 0:
            self.opendir = os.path.dirname(jsonfile)
            self.controller.saveJSON4DCP(jsonfile)

    def button_option_button_clicked(self):
        self.option_win = OptionWindow()
        self.option_win.show()

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
        self.toolbar.openCSVClicked.connect(self.button_open_csv_clicked)
        self.toolbar.dcpReadClicked.connect(self.button_dcp_read_clicked)
        self.toolbar.dcpSaveClicked.connect(self.button_dcp_save_clicked)
        self.toolbar.optionButtonClicked.connect(self.button_option_button_clicked)
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
            'stats': DCPStats(self.features),
        }
        # tab creation
        self.tab.addTab(page['summary'], 'Summary')
        self.tab.addTab(page['sensors'], 'Sensor Selection')
        self.tab.addTab(page['recipe'], 'Setting Data')
        self.tab.addTab(page['stats'], 'Summary Stats')
        # Log event
        page['summary'].logMessage.connect(self.showLog)
        page['sensors'].logMessage.connect(self.showLog)
        page['recipe'].logMessage.connect(self.showLog)
        page['stats'].logMessage.connect(self.showLog)
        # _____________________________________________________________________
        # for tab click event
        self.tab.currentChanged.connect(self.tab_changed)
        # _____________________________________________________________________
        # Controller for tab and other UI interaction
        self.controller = UIController(page)
        # Experimental
        page['experimental'] = DCPExperimental(self.features, self.controller)
        self.tab.addTab(page['experimental'], 'Experimental')
        page['experimental'].logMessage.connect(self.showLog)

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

    def read_csv(self, csvfile: str):
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
            self.console.insertIn('Contents of the zip file:')
            for name_file in list_file:
                self.console.insertIn('- %s' % name_file)
            if len(list_file) > 1:
                self.console.insertAttention()
                self.console.insertIn('Several files are included in this zip file.')
                self.console.insertIn('Sorry, this type of file cannot be read.')
                return
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

    def showLog(self, msg):
        self.console.insertIn(msg)

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
