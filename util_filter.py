from PySide6.QtWidgets import QPushButton, QWidget, QSizePolicy

from app_widgets import LabelFrameNarrow, MenuButton
from app_object import AppObject
from dcp_sensor_selection_dock import DCPSensorSelectionDock


class UtilFilter(AppObject):
    def __init__(self, page: dict):
        super().__init__(page)
        self.init_sensor_filter()

    def init_sensor_filter(self):
        dock_sensors: DCPSensorSelectionDock = self.page['sensors'].getDock()
        layout = dock_sensors.getLayout()
        # _____________________________________________________________________
        # Basic Filters for Column
        lab_step = LabelFrameNarrow('Step Selection')
        layout.addWidget(lab_step)
        # _____________________________________________________________________
        # filter for excluding step >= 1000 (dechuck step)
        but_exclude_step_dechuck = MenuButton('exclude Step >= 1000')
        but_exclude_step_dechuck.clicked.connect(self.exclude_step_dechuck)
        layout.addWidget(but_exclude_step_dechuck)
        # _____________________________________________________________________
        # filter for excluding steps without (setting data)
        but_exclude_no_setting = MenuButton('exclude Step w/o (setting data)')
        but_exclude_no_setting.clicked.connect(self.exclude_no_setting)
        layout.addWidget(but_exclude_no_setting)
        # _____________________________________________________________________
        # Basic Filters for Column
        lab_condition = LabelFrameNarrow('Filter with Condition')
        layout.addWidget(lab_condition)
        # _____________________________________________________________________
        # filter for excluding steps where (setting data) = 0
        but_exclude_setting_0 = MenuButton('exclude Step setting = 0')
        but_exclude_setting_0.clicked.connect(self.exclude_setting_0)
        layout.addWidget(but_exclude_setting_0)
        # padding
        vpad = QWidget()
        vpad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addWidget(vpad)


    def exclude_step_dechuck(self):
        but: QPushButton = self.sender()
        sensors = self.getPanelSensors()
        sensors.excludeStepDechuck(but.isChecked())
        self.updateFeatures()

    def exclude_no_setting(self):
        but: QPushButton = self.sender()
        recipe = self.getPanelRecipe()
        list_sensor_setting = recipe.getSensorWithSetting()
        sensors = self.getPanelSensors()
        sensors.excludeSensorWithoutSetting(but.isChecked(), list_sensor_setting)
        self.updateFeatures()

    def exclude_setting_0(self):
        but: QPushButton = self.sender()
        recipe = self.getPanelRecipe()
        dict_sensor_step_setting_0 = recipe.getSensorStepSetting0()
        sensors = self.getPanelSensors()
        sensors.excludeSetting0(but.isChecked(), dict_sensor_step_setting_0)
        self.updateFeatures()
