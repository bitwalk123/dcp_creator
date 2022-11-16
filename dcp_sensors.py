from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QDockWidget,
)

from base.tab_window import TabWindow
from dcp_sensors_dock import DCPSensorSelectionDock
from features import Features
from sensors import Sensors


class DCPSensorSelection(TabWindow):
    """
    SensorSelectionMain
    Main windows for Sensor Selection
    """
    excludeGasFlow0 = Signal(bool)
    excludePower0 = Signal(bool)

    sensors = None
    dock = None

    def __init__(self, features: Features):
        super().__init__()
        self.init_ui(features)

    def init_ui(self, features: Features):
        """initialize UI
        """
        sensors = Sensors(features)
        sensors.logMessage.connect(self.showLog)
        self.setCentralWidget(sensors)
        # _____________________________________________________________________
        # Right Dock
        dock = DCPSensorSelectionDock()
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        #
        self.sensors = sensors
        self.dock = dock

    def getPanel(self) -> Sensors:
        """get/return instance of this panel
        """
        return self.sensors

    def getDock(self) -> DCPSensorSelectionDock:
        """get/return instance of the dock at right
        """
        return self.dock
