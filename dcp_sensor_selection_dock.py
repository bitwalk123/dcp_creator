from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QPushButton,
    QSizePolicy,
    QWidget,
)

from app_widgets import (
    LabelFrameNarrow,
    MenuButton,
    VBoxLayout,
)


class DCPSensorSelectionDock(QDockWidget):
    """
    DockFilter
    dock for sensor filtering
    """
    excludeNoSetting = Signal(bool)
    excludeSetting0 = Signal(bool)
    excludeGasFlow0 = Signal(bool)
    excludeRFPower0 = Signal(bool)
    excludeSensorDYP = Signal(bool)
    excludeStepMinus1 = Signal(bool)
    excludeStepDechuck = Signal(bool)
    excludeSensorSetting = Signal(bool)
    excludeSensorTimeDependent = Signal(bool)
    excludeSensorEPD = Signal(bool)
    excludeLargeUnit = Signal(bool)
    excludeSensorOES = Signal(bool)

    def __init__(self):
        super().__init__('Filter')
        # self.sensors = sensors
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)
        # Layout for the dock
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
        but_exclude_sensor_general_counter = MenuButton('exclude General Counter sensor')
        but_exclude_sensor_general_counter.clicked.connect(self.exclude_sensor_time_dependent)
        layout.addWidget(but_exclude_sensor_general_counter)
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
        but_exclude_sensor_oes.clicked.connect(self.exclude_sensor_oes)
        layout.addWidget(but_exclude_sensor_oes)
        #
        but_exclude_large_unit = MenuButton('exclude sensor with unit [MPaG]')
        but_exclude_large_unit.clicked.connect(self.exclude_sensor_large_unit)
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
        self.excludeSensorDYP.emit(True)

        but_exclude_step_minus1.animateClick()
        self.excludeStepMinus1.emit(True)

        but_exclude_step_dechuck.animateClick()
        self.excludeStepDechuck.emit(True)

    def exclude_no_setting(self):
        but: QPushButton = self.sender()
        self.excludeNoSetting.emit(but.isChecked())

    def exclude_setting_0(self):
        but: QPushButton = self.sender()
        self.excludeSetting0.emit(but.isChecked())

    def exclude_gas_flow_0(self):
        but: QPushButton = self.sender()
        self.excludeGasFlow0.emit(but.isChecked())

    def exclude_rf_power_0(self):
        but: QPushButton = self.sender()
        self.excludeRFPower0.emit(but.isChecked())

    def exclude_sensor_dyp(self):
        but: QPushButton = self.sender()
        self.excludeSensorDYP.emit(but.isChecked())

    def exclude_step_minus1(self):
        but: QPushButton = self.sender()
        self.excludeStepMinus1.emit(but.isChecked())

    def exclude_step_dechuck(self):
        but: QPushButton = self.sender()
        self.excludeStepDechuck.emit(but.isChecked())

    def exclude_sensor_for_setting(self):
        but: QPushButton = self.sender()
        self.excludeSensorSetting.emit(but.isChecked())

    def exclude_sensor_time_dependent(self):
        but: QPushButton = self.sender()
        self.excludeSensorTimeDependent.emit(but.isChecked())

    def exclude_sensor_epd(self):
        but: QPushButton = self.sender()
        self.excludeSensorEPD.emit(but.isChecked())

    def exclude_sensor_large_unit(self):
        but: QPushButton = self.sender()
        self.excludeLargeUnit.emit(but.isChecked())

    def exclude_sensor_oes(self):
        but: QPushButton = self.sender()
        self.excludeSensorOES.emit(but.isChecked())
