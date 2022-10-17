from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QWidget, QSizePolicy

from app_widgets import LabelFrameNarrow, MenuButton
from app_object import AppObject
from dcp_sensor_selection_dock import DCPSensorSelectionDock


class UtilFilter(AppObject):
    def __init__(self, page: dict):
        super().__init__(page)
        self.init_sensor_filter()

    def init_sensor_filter(self):
        """Toggle Button creation for various filters
        """
        dock_sensors: DCPSensorSelectionDock = self.page['sensors'].getDock()
        layout = dock_sensors.getLayout()
        # _____________________________________________________________________
        # Basic Filters for Column
        lab_step = LabelFrameNarrow('Step Selection')
        layout.addWidget(lab_step)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding step >= 1000 (de-chuck step)
        but_exclude_step_dechuck = MenuButton('exclude Step >= 1000')
        but_exclude_step_dechuck.clicked.connect(self.exclude_step_dechuck)
        layout.addWidget(but_exclude_step_dechuck)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding steps without (setting data)
        but_exclude_no_setting = MenuButton('exclude Step w/o (setting data)')
        but_exclude_no_setting.clicked.connect(self.exclude_no_setting)
        layout.addWidget(but_exclude_no_setting)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Basic Filters for Column
        lab_condition = LabelFrameNarrow('Filter with Condition')
        layout.addWidget(lab_condition)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding steps where (setting data) = 0
        but_exclude_setting_0 = MenuButton('exclude Step setting = 0')
        but_exclude_setting_0.clicked.connect(self.exclude_setting_0)
        layout.addWidget(but_exclude_setting_0)
        # _____________________________________________________________________
        # padding
        vpad = QWidget()
        vpad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addWidget(vpad)

    def exclude_step_dechuck(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()
        list_col = list()
        model = self.getPanelSensorsModel()
        for i in range(model.columnCount()):
            name_head = model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            if type(name_head) is not int:
                continue
            if name_head >= 1000:
                list_col.append(i)
        for col in list_col:
            self.switch_check_all_rows(model, col, flag)

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

    def switch_check_all_rows(self, model, col, flag):
        """check/uncheck checkbox in specified columns
        """
        features = self.getPanelSensorsFeatures()
        for row in range(features.getRows()):
            index = model.index(row, col)
            if flag:
                model.setData(index, Qt.CheckState.Unchecked, role=Qt.CheckStateRole)
            else:
                model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)
