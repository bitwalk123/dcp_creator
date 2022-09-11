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
    sensors = None
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
        sensors = Sensors(features)
        central.setWidget(sensors)
        # _____________________________________________________________________
        # Right Dock
        dock = DCPSensorSelectionDock(sensors)
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        #
        self.sensors = sensors
        self.dock = dock

    def getPanel(self) -> Sensors:
        return self.sensors
