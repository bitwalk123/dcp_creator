from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QScrollArea,
    QMainWindow,
)

from feature_info import FeatureInfo
from dcp_sensor_selection_dock import DCPSensorSelectionDock
from dcp_matrix import DCPMatrix


class DCPSensorSelection(QMainWindow):
    """
    SensorSelectionMain
    Main windows for Sensor Selection
    """
    dcp = None
    dock = None

    def __init__(self, features: FeatureInfo):
        super().__init__()
        # self.setAutoFillBackground(True)
        self.init_ui(features)

    def init_ui(self, features: FeatureInfo):
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
        dcp = DCPMatrix(features)
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
