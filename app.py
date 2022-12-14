#!/usr/bin/env python
# coding: utf-8
import os
import pathlib
import sys
import warnings
from pathlib import Path

import PySide6
import matplotlib
import pandas as pd
import sklearn
from PySide6.QtCore import (
    Qt,
    QThread,
    QUrl,
)
from PySide6.QtGui import QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QStatusBar,
    QTabWidget,
    QStyle,
)

from app_toolbar import DCPCreatorToolBar
from app_widgets import WorkInProgress, DialogWarn, OptionWindow
from base.log_console import LogConsole
from dcp_experimental import DCPExperimental
from dcp_recipe import DCPStepValueSetting
from dcp_sensors import DCPSensorSelection
from dcp_stats import DCPStats
from dcp_summary import DCPSummary
from features import Features
from modules.read_csv import ReadCSV, CSVReadWorker
from ui_controller import UIController

warnings.simplefilter('ignore', FutureWarning)


class DCPCreator(QMainWindow):
    """DCP creator with the CSV file exported from the fleet analysis tool
    """
    __version__ = '0.1.4'
    __version_minor__ = '20230107'

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

    # image/icon location
    imgdir = 'image'

    # thread instances
    reader: CSVReadWorker = None
    thread_reader: QThread = None
    thread_parser: QThread = None

    # progressbar
    progress_reader: WorkInProgress = None
    progress_parser: WorkInProgress = None

    # Option Window
    option_win = None

    # manual
    view_manual = None

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(1000, 800)
        self.setWindowTitle('DCP Creator')
        self.setWindowIcon(QIcon(os.path.join(self.imgdir, 'logo.png')))
        # _____________________________________________________________________
        # Console output
        self.console.insertOut(
            'Python {}'.format(sys.version)
        )
        self.console.insertOut(
            'PySide6 (Python for Qt) {}'.format(PySide6.__version__)
        )
        self.console.insertOut(
            'matplotlib {}'.format(matplotlib.__version__)
        )
        self.console.insertOut(
            'scikit-learn {}'.format(sklearn.__version__)
        )
        self.console.insertIn(
            '<<< Welcome to DCP Creator {}, {} >>>'.format(self.__version__, self.__version_minor__)
        )

    def button_dcp_help_clicked(self):
        """manual browser for DCP Creator
        """
        self.view_manual = QWebEngineView()
        self.view_manual.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion))
        )
        self.view_manual.setWindowTitle('DCP Creator user\'s manual')
        index_file = pathlib.Path(os.path.join(os.getcwd(), 'doc/index.html'))
        site = index_file.as_uri()
        self.view_manual.load(QUrl(site))
        self.view_manual.show()

    def button_dcp_read_clicked(self):
        """DCP Reader in JSON format
        """
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
        """DCP Saver in JSON format
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

    def button_open_csv_clicked(self):
        """Data Reader in CSV format, which is exported from main application
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
        if len(csvfile) == 0:
            return

        # remember directory location
        self.opendir = os.path.dirname(csvfile)
        self.console.insertIn('reading %s.' % csvfile)
        obj = ReadCSV()
        obj.readCompleted.connect(self.parse_df)
        obj.read(csvfile)

    def parse_df(self, df: pd.DataFrame):
        self.df = df
        self.features = Features(df)
        self.main_ui()

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
        if self.view_manual is not None:
            self.view_manual.close()
        event.accept()

    def init_ui(self):
        """Initialize UI
        """
        # _____________________________________________________________________
        # Toolbar
        self.toolbar = DCPCreatorToolBar()
        self.toolbar.openCSVClicked.connect(self.button_open_csv_clicked)
        self.toolbar.dcpReadClicked.connect(self.button_dcp_read_clicked)
        self.toolbar.optionButtonClicked.connect(self.button_option_button_clicked)
        self.toolbar.dcpHelpClicked.connect(self.button_dcp_help_clicked)
        self.toolbar.dcpSaveClicked.connect(self.button_dcp_save_clicked)
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
        for key in page.keys():
            page[key].logMessage.connect(self.showLog)
        # page['sensors'].logMessage.connect(self.showLog)
        # page['recipe'].logMessage.connect(self.showLog)
        # page['stats'].logMessage.connect(self.showLog)
        # page['experimental'].logMessage.connect(self.showLog)
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
