from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from app_widgets import (
    VBoxLayout,
    MenuButton, Label, LabelFrameNarrow,
)
from sensors import Sensors


class DCPSensorSelectionDock(QDockWidget):
    """
    DockFilter
    dock for sensor filtering
    """
    excludeNoSetting = Signal(bool)
    excludeSetting0 = Signal(bool)
    excludeGasFlow0 = Signal(bool)
    excludeRFPower0 = Signal(bool)

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
        # _____________________________________________________________________
        # Misc. Filters
        lab_auto = LabelFrameNarrow('Auto')
        layout.addWidget(lab_auto)

        but_exclude_no_setting = MenuButton('exclude Step w/o (setting data)')
        but_exclude_no_setting.clicked.connect(self.exclude_no_setting)
        layout.addWidget(but_exclude_no_setting)

        but_exclude_setting_0 = MenuButton('exclude Step setting = 0')
        but_exclude_setting_0.clicked.connect(self.exclude_setting_0)
        layout.addWidget(but_exclude_setting_0)

        but_exclude_step_minus1 = MenuButton('exclude Step -1')
        but_exclude_step_minus1.clicked.connect(self.exclude_step_minus1)
        layout.addWidget(but_exclude_step_minus1)
        #
        but_exclude_step_dechuck = MenuButton('exclude Step >= 1000')
        but_exclude_step_dechuck.clicked.connect(self.exclude_step_dechuck)
        layout.addWidget(but_exclude_step_dechuck)
        # _____________________________________________________________________
        # Misc. Filters
        lab_misc = LabelFrameNarrow('Misc.')
        layout.addWidget(lab_misc)
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
        but_exclude_sensor_oes = MenuButton('exclude OES data')
        but_exclude_sensor_oes.clicked.connect(self.exclude_oes)
        layout.addWidget(but_exclude_sensor_oes)
        #
        but_exclude_large_unit = MenuButton('exclude sensor with unit [MPaG]')
        but_exclude_large_unit.clicked.connect(self.exclude_large_unit)
        layout.addWidget(but_exclude_large_unit)
        #
        but_exclude_gas_flow_0 = MenuButton('exclude Gas Flow setting = 0')
        but_exclude_gas_flow_0.clicked.connect(self.exclude_gas_flow_0)
        layout.addWidget(but_exclude_gas_flow_0)
        #
        but_exclude_power_0 = MenuButton('exclude RF Power setting = 0')
        but_exclude_power_0.clicked.connect(self.exclude_rf_power_0)
        layout.addWidget(but_exclude_power_0)
        #
        but = MenuButton('exclude Step with Small Variation')
        layout.addWidget(but)

        # _____________________________________________________________________
        # initial filter
        but_exclude_sensor_dyp.animateClick()
        self.sensors.excludeSensorDYP(True)

        but_exclude_step_minus1.animateClick()
        self.sensors.excludeStepMinus1(True)

        but_exclude_step_dechuck.animateClick()
        self.sensors.excludeStepDechuck(True)

        """
        but_exclude_sensor_time_dependent.animateClick()
        self.sensors.excludeSensorTimeDependent(True)

        but_exclude_sensor_epd.animateClick()
        self.sensors.excludeSensorEPD(True)

        but_exclude_large_unit.animateClick()
        self.sensors.excludeLargeUnit(True)

        # --- need event to change --------------------------------------------
        but_exclude_gas_flow_0.animateClick()
        self.excludeGasFlow0.emit(True)

        but_exclude_power_0.animateClick()
        self.excludeRFPower0.emit(True)

        but_exclude_sensor_for_setting.animateClick()
        self.sensors.excludeSensorSetting(True)

        but_exclude_sensor_oes.animateClick()
        self.sensors.excludeSensorOES(True)
        """

    def exclude_no_setting(self):
        but: QPushButton = self.sender()
        self.excludeNoSetting.emit(but.isChecked())

    def exclude_setting_0(self):
        but: QPushButton = self.sender()
        self.excludeSetting0.emit(but.isChecked())

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

    def exclude_large_unit(self):
        but: QPushButton = self.sender()
        self.sensors.excludeLargeUnit(but.isChecked())

    def exclude_oes(self):
        but: QPushButton = self.sender()
        self.sensors.excludeSensorOES(but.isChecked())

    def exclude_gas_flow_0(self):
        but: QPushButton = self.sender()
        self.excludeGasFlow0.emit(but.isChecked())

    def exclude_rf_power_0(self):
        but: QPushButton = self.sender()
        self.excludeRFPower0.emit(but.isChecked())
