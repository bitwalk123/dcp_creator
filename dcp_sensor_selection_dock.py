from PySide6.QtWidgets import (
    QDockWidget,
    QSizePolicy,
    QWidget, QPushButton,
)

from app_widgets import (
    VBoxLayout,
    MenuButton,
)
from sensors import Sensors


class DCPSensorSelectionDock(QDockWidget):
    """
    DockFilter
    dock for sensor filtering
    """

    def __init__(self, sensors: Sensors):
        super().__init__('Filter')
        self.sensors = sensors
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)
        # Layout for dock
        layout = VBoxLayout()
        base.setLayout(layout)
        self.init_ui(layout)

    def init_ui(self, layout):
        """
        init_ui
        filtering options
        :param layout:
        """
        but_exclude_step_minus1 = MenuButton('exclude Step -1')
        but_exclude_step_minus1.clicked.connect(self.exclude_step_minus1)
        layout.addWidget(but_exclude_step_minus1)
        #
        but_exclude_step_dechuck = MenuButton('exclude Step >= 1000')
        but_exclude_step_dechuck.clicked.connect(self.exclude_step_dechuck)
        layout.addWidget(but_exclude_step_dechuck)
        #
        but_exclude_sensor_for_setting = MenuButton('exclude Sensor of setting data')
        but_exclude_sensor_for_setting.clicked.connect(self.exclude_sensor_for_setting)
        layout.addWidget(but_exclude_sensor_for_setting)
        #
        but = MenuButton('exclude Step with Small Variation')
        layout.addWidget(but)
        #
        but = MenuButton('exclude OES data')
        layout.addWidget(but)
        #
        but = MenuButton('exclude time dependent sensor')
        layout.addWidget(but)
        # _____________________________________________________________________
        # clicked by default
        #but_exclude_step_minus1.animateClick()
        #but_exclude_step_dechuck.animateClick()
        #but_exclude_sensor_for_setting.animateClick()

    def exclude_step_minus1(self):
        but: QPushButton = self.sender()
        self.sensors.excludeStepMinus1(but.isChecked())

    def exclude_step_dechuck(self):
        but: QPushButton = self.sender()
        self.sensors.excludeStepDechuck(but.isChecked())

    def exclude_sensor_for_setting(self):
        but: QPushButton = self.sender()
        self.sensors.excludeSensorForSetting(but.isChecked())
