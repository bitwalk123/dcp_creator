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
        but_exclude_sensor_time_dependent = MenuButton('exclude time dependent sensor')
        but_exclude_sensor_time_dependent.clicked.connect(self.exclude_sensor_time_dependent)
        layout.addWidget(but_exclude_sensor_time_dependent)
        #
        but_exclude_sensor_dyp = MenuButton('exclude Dynamic Process sensors')
        but_exclude_sensor_dyp.clicked.connect(self.exclude_sensor_dyp)
        layout.addWidget(but_exclude_sensor_dyp)
        #
        but_exclude_sensor_epd = MenuButton('exclude EPD DATA sensors')
        but_exclude_sensor_epd.clicked.connect(self.exclude_sensor_epd)
        layout.addWidget(but_exclude_sensor_epd)
        #
        but = MenuButton('exclude Gas Flow setting = 0')
        layout.addWidget(but)
        #
        but = MenuButton('exclude Power setting = 0')
        layout.addWidget(but)
        #
        but = MenuButton('exclude OES data')
        layout.addWidget(but)
        #
        but = MenuButton('exclude Step with Small Variation')
        layout.addWidget(but)

        # _____________________________________________________________________
        # initial filter
        but_exclude_step_minus1.animateClick()
        self.sensors.excludeStepMinus1(True)

        but_exclude_step_dechuck.animateClick()
        self.sensors.excludeStepDechuck(True)

        but_exclude_sensor_for_setting.animateClick()
        self.sensors.excludeSensorSetting(True)

        but_exclude_sensor_time_dependent.animateClick()
        self.sensors.excludeSensorTimeDependent(True)

        but_exclude_sensor_dyp.animateClick()
        self.sensors.excludeSensorDYP(True)

        but_exclude_sensor_epd.animateClick()
        self.sensors.excludeSensorEPD(True)

    def exclude_step_minus1(self):
        but: QPushButton = self.sender()
        self.sensors.excludeStepMinus1(but.isChecked())

    def exclude_step_dechuck(self):
        but: QPushButton = self.sender()
        self.sensors.excludeStepDechuck(but.isChecked())

    def exclude_sensor_for_setting(self):
        but: QPushButton = self.sender()
        self.sensors.excludeSensorSetting(but.isChecked())

    def exclude_sensor_time_dependent(self):
        but: QPushButton = self.sender()
        self.sensors.excludeSensorTimeDependent(but.isChecked())

    def exclude_sensor_dyp(self):
        but: QPushButton = self.sender()
        self.sensors.excludeSensorDYP(but.isChecked())

    def exclude_sensor_epd(self):
        but: QPushButton = self.sender()
        self.sensors.excludeSensorEPD(but.isChecked())
