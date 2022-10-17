from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QWidget, QSizePolicy, QRadioButton, QButtonGroup

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
        # filter for excluding step 1 (usually this step is just for stability)
        but_exclude_step_1 = MenuButton('exclude Step 1')
        but_exclude_step_1.clicked.connect(self.exclude_step_1)
        layout.addWidget(but_exclude_step_1)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding step >= 1000 (de-chuck step)
        but_exclude_step_dechuck = MenuButton('exclude Step >= 1000')
        but_exclude_step_dechuck.clicked.connect(self.exclude_step_dechuck)
        layout.addWidget(but_exclude_step_dechuck)
        # _____________________________________________________________________
        # Condition Filters
        lab_condition = LabelFrameNarrow('Condition Filter')
        layout.addWidget(lab_condition)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding steps without (setting data)
        but_exclude_no_setting = MenuButton('exclude Step w/o (setting data)')
        but_exclude_no_setting.clicked.connect(self.exclude_no_setting)
        layout.addWidget(but_exclude_no_setting)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding steps where (setting data) = 0
        but_exclude_setting_0 = MenuButton('exclude Step setting = 0')
        but_exclude_setting_0.clicked.connect(self.exclude_setting_0)
        layout.addWidget(but_exclude_setting_0)
        # _____________________________________________________________________
        # Category Filters
        lab_category = LabelFrameNarrow('Sensor Category')
        layout.addWidget(lab_category)
        rb_category_group = QButtonGroup()
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # category: ALL
        rb_category_all = QRadioButton('ALL')
        rb_category_group.addButton(rb_category_all)
        layout.addWidget(rb_category_all)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # category: ESC
        rb_category_esc = QRadioButton('ESC')
        rb_category_group.addButton(rb_category_esc)
        layout.addWidget(rb_category_esc)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # category: Other
        rb_category_other = QRadioButton('Other')
        rb_category_group.addButton(rb_category_other)
        layout.addWidget(rb_category_other)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # category: Pressure
        rb_category_pressure = QRadioButton('Pressure')
        rb_category_group.addButton(rb_category_pressure)
        layout.addWidget(rb_category_pressure)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # category: RF
        rb_category_rf = QRadioButton('RF')
        rb_category_group.addButton(rb_category_rf)
        layout.addWidget(rb_category_rf)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # category: Temperature
        rb_category_temperature = QRadioButton('Temperature')
        rb_category_group.addButton(rb_category_temperature)
        layout.addWidget(rb_category_temperature)
        # _____________________________________________________________________
        # padding
        vpad = QWidget()
        vpad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addWidget(vpad)

    def exclude_step_1(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()
        list_col = list()
        model = self.getPanelSensorsModel()
        # column search
        for i in range(model.columnCount()):
            name_head = model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            if type(name_head) is not int:
                continue
            # condition
            if name_head == 1:
                list_col.append(i)
        # set checkbox in the columns to flag
        for col in list_col:
            self.switch_check_all_rows(col, flag)

        self.updateFeatures()

    def exclude_step_dechuck(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()
        list_col = list()
        model = self.getPanelSensorsModel()
        # column search
        for i in range(model.columnCount()):
            name_head = model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            if type(name_head) is not int:
                continue
            # condition
            if name_head >= 1000:
                list_col.append(i)
        # set checkbox in the columns to flag
        for col in list_col:
            self.switch_check_all_rows(col, flag)

        self.updateFeatures()

    def exclude_no_setting(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()
        # obtain list of sensor name which has setting value
        list_sensor_setting = self.getPanelRecipeSensorWithSetting()
        # collect sensors which does not have setting value
        features = self.getPanelSensorsFeatures()
        list_sensor = list()
        for sensor in features.getSensors():
            if sensor not in list_sensor_setting:
                list_sensor.append(sensor)
        # get list of row index of the sensors w/o setting data
        list_row = list()
        for sensor in list_sensor:
            list_row.append(features.getSensors().index(sensor))
        # get all of step columns
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)
        #
        self.updateFeatures()

    def exclude_setting_0(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()
        model = self.getPanelSensorsModel()
        features = self.getPanelSensorsFeatures()
        dict_sensor_step_setting_0 = self.getPanelRecipeSensorStepSetting0()
        list_sensor_step_setting_0 = dict_sensor_step_setting_0.keys()
        for sensor in features.getSensors():
            row = features.getSensors().index(sensor)
            if sensor in list_sensor_step_setting_0:
                for step_name in dict_sensor_step_setting_0[sensor]:
                    col: int = self.find_header_label(step_name)
                    index = model.index(row, col)
                    if flag:
                        model.setData(index, Qt.CheckState.Unchecked, role=Qt.CheckStateRole)
                    else:
                        model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)
        self.updateFeatures()

