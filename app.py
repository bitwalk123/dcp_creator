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
from dcp_organizer import DCPOrganizer
from dcp_sensor_selection_dock import DCPSensorSelectionDock
from dcp_summary import DCPSummary
from features import Features
from dcp_sensor_selection import DCPSensorSelection
from dcp_step_value_setting import DCPStepValueSetting


class DCPCreator(QMainWindow):
    """
    DCPCreator
    DCP creator with the CSV file exported from the fleet analysis tool
    """
    __version__ = '20220916'
    toolbar = None
    statusbar = None
    organizer = None

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
        self.read_csv()

    def read_csv(self):
        selection = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select CSV file',
            filter='CSV File (*.csv)'
        )
        csvfile = selection[0]
        if not os.path.exists(csvfile):
            return

        df = pd.read_csv(csvfile)
        obj_feature = Features(df)
        self.main_ui(obj_feature)


    def button_save_clicked(self):
        """
        button_save_clicked
        action for 'Save' button clicked.
        """
        if self.organizer is None:
            print('There is no data!')
            return
        selection = QFileDialog.getSaveFileName(
            parent=self,
            caption='Specify name of JSON file to save',
            dir='dcp.json',
            filter='JSON File (*.json)'
        )
        jsonfile = selection[0]
        self.organizer.saveDCP(jsonfile)

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

    def main_ui(self, features: Features):
        """
        main_ui
        :param features:
        :return:
        """
        page = {}
        # remove central widget if exists.
        self.takeCentralWidget()
        # make new tab widget
        tab = QTabWidget()
        self.setCentralWidget(tab)
        # _____________________________________________________________________
        # Summary
        page['summary'] = page_summary = DCPSummary(features)
        tab.addTab(page_summary, 'Summary')
        # _____________________________________________________________________
        # Sensor Selection
        page['sensors'] = page_sensor = DCPSensorSelection(features)
        tab.addTab(page_sensor, 'Sensor Selection')
        # binding
        dock_sensors: DCPSensorSelectionDock = page_sensor.getDock()
        dock_sensors.excludeNoSetting.connect(self.exclude_no_setting)
        dock_sensors.excludeSetting0.connect(self.exclude_setting_0)
        dock_sensors.excludeGasFlow0.connect(self.exclude_gas_flow_0)
        dock_sensors.excludeRFPower0.connect(self.exclude_rf_power_0)
        # _____________________________________________________________________
        # Setting Data
        page['recipe'] = page_recipe = DCPStepValueSetting(features)
        tab.addTab(page_recipe, 'Setting Data')
        # _____________________________________________________________________
        self.organizer = DCPOrganizer(page)
        self.organizer.init()
        # _____________________________________________________________________
        # for tab click event
        tab.currentChanged.connect(self.tab_changed)

    def tab_changed(self):
        """
        tab_changed
        for event when Tab changed
        """
        tab: QTabWidget = self.sender()
        idx = tab.currentIndex()
        if idx == 0:
            self.organizer.update_features()
        print('current tab', idx)

    def exclude_no_setting(self, flag: bool):
        """
        exclude_no_setting
        exclude sensor w/o setting data
        """
        recipe = self.organizer.getPanelRecipe()
        list_sensor_setting = recipe.getSensorWithSetting()
        sensors = self.organizer.getPanelSensors()
        sensors.excludeSensorWithoutSetting(flag, list_sensor_setting)
        self.organizer.update_features()

    def exclude_setting_0(self, flag: bool):
        """
        exclude_setting_0
        exclude sensor where setting data = 0
        """
        print('DEBUG!')
        recipe = self.organizer.getPanelRecipe()
        dict_sensor_step_setting_0 = recipe.getSensorStepSetting0()
        sensors = self.organizer.getPanelSensors()
        sensors.excludeSetting0(flag, dict_sensor_step_setting_0)
        self.organizer.update_features()

    def exclude_gas_flow_0(self, flag: bool):
        """
        exclude_gas_flow_0
        exclude sensor/step where Gas Flow = 0
        """
        recipe = self.organizer.getPanelRecipe()
        list_sensor_step = recipe.excludeGasFlow0(flag)
        sensors = self.organizer.getPanelSensors()
        sensors.setSensorStep(flag, list_sensor_step)
        self.organizer.update_features()

    def exclude_rf_power_0(self, flag: bool):
        """
        exclude_rf_power_0
        exclude sensor/step where RF Power = 0
        """
        recipe = self.organizer.getPanelRecipe()
        list_sensor_step = recipe.excludeRFPower0(flag)
        sensors = self.organizer.getPanelSensors()
        sensors.setSensorStep(flag, list_sensor_step)
        self.organizer.update_features()


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
