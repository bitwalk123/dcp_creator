#!/usr/bin/env python
# coding: utf-8
import os
import sys
import pandas as pd

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QStatusBar,
    QStyle,
    QTabWidget,
)

from dcp_creator_toolbar import DCPCreatorToolBar
from dcp_feature import FeatureInfo
from dcp_main import DCPMain
from dcp_setting import DCPSettingData


class DCPCreator(QMainWindow):
    """
    DCPCreator
    DCP creator with the CSV file exported from the fleet analysis tool
    """
    __version__ = '20220902'
    toolbar = None
    statusbar = None

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(1000, 800)
        self.setWindowTitle('DCP Creator')
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        )

    def button_open_clicked(self):
        """
        button_open_clicked
        action for 'Open' button clicked.
        """
        selection = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select CSV file',
            filter='CSV File (*.csv)'
        )
        csvfile = selection[0]
        if os.path.exists(csvfile):
            df = pd.read_csv(csvfile)
            obj = FeatureInfo(df)
            self.main_ui(obj)

    def button_save_clicked(self):
        """
        button_save_clicked
        action for 'Save' button clicked.
        """
        print('Not implemented yet!')

    def closeEvent(self, event):
        """
        closeEvent
        close event handling.
        :param event:
        """
        print('Exiting application ...')
        event.accept()

    def init_ui(self):
        """
        init_ui
        initialize UI
        """
        # _____________________________________________________________________
        # Toolbar
        self.toolbar = DCPCreatorToolBar()
        self.toolbar.openClicked.connect(self.button_open_clicked)
        self.toolbar.saveClicked.connect(self.button_save_clicked)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        # _____________________________________________________________________
        # Statusbar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def main_ui(self, features: FeatureInfo):
        """
        main_ui
        generate main UI
        :param df: dataframe of summary stat log data read from CSV
        """
        # remove central widget if exists.
        self.takeCentralWidget()
        # make new tab widget
        tab = QTabWidget()
        self.setCentralWidget(tab)
        # Sensor Selection
        tab.addTab(DCPMain(features), 'Sensor Selection')
        # Setting Data
        tab.addTab(DCPSettingData(features), 'Setting Data')


def main():
    """
    Event Loop
    """
    app: QApplication = QApplication(sys.argv)
    ex = DCPCreator()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
