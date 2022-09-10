from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QScrollArea,
    QMainWindow,
)

from features import Features
from dcp_sensor_selection_dock import DCPSensorSelectionDock
from sensors import Sensors


class DCPSensorSelection(QMainWindow):
    """
    SensorSelectionMain
    Main windows for Sensor Selection
    """
    dcp = None
    dock = None

    def __init__(self, features: Features):
        super().__init__()
        # self.setAutoFillBackground(True)
        self.init_ui(features)

    def init_ui(self, features: Features):
        """
        init_ui
        initialize UI
        :param info_log:
        """
        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        # Blank Widget on the Scroll Area
        dcp = Sensors(features)
        central.setWidget(dcp)
        # _____________________________________________________________________
        # Right Dock
        dock = DCPSensorSelectionDock(dcp)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        #
        self.dcp = dcp
        self.dock = dock
