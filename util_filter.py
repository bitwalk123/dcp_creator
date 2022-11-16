from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QPushButton,
    QSizePolicy,
    QWidget,
)
from app_widgets import (
    LabelFrameNarrow,
    MenuButton,
    RadioButton,
)
from app_object import AppObject
from dcp_sensors_dock import DCPSensorSelectionDock


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
        lab_step = LabelFrameNarrow('▸ Step Selection', flag=True)
        layout.addWidget(lab_step)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding step 1 (usually this step is just for stability)
        but_exclude_step_1 = MenuButton('exclude Step 1')
        but_exclude_step_1.clicked.connect(self.excludeStep1)
        layout.addWidget(but_exclude_step_1)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding step >= 1000 (de-chuck step)
        but_exclude_dechuck_steps = MenuButton('exclude Step >= 1000')
        but_exclude_dechuck_steps.clicked.connect(self.excludeStepDechuck)
        layout.addWidget(but_exclude_dechuck_steps)

        # _____________________________________________________________________
        # Condition Filters
        lab_condition = LabelFrameNarrow('▸ Filter to exclude by condition')
        layout.addWidget(lab_condition)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding steps without (setting data)
        but_exclude_sensor_wo_setting = MenuButton('Step w/o Setting Data')
        but_exclude_sensor_wo_setting.clicked.connect(self.excludeSensorWOSetting)
        layout.addWidget(but_exclude_sensor_wo_setting)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # filter for excluding steps where (setting data) = 0
        but_exclude_step_setting_0 = MenuButton('Step Setting = 0')
        but_exclude_step_setting_0.clicked.connect(self.excludeStepSettingIs0)
        layout.addWidget(but_exclude_step_setting_0)

        # _____________________________________________________________________
        # Filters for Specific Sensor
        lab_specific = LabelFrameNarrow('▸ Specific Sensor to exclude')
        layout.addWidget(lab_specific)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # excluding OES sensor
        but_exclude_sensor_oes = MenuButton('OES sensors')
        but_exclude_sensor_oes.clicked.connect(self.excludeSensorOES)
        layout.addWidget(but_exclude_sensor_oes)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # excluding sensor for Setting Data
        but_exclude_sensor_setting = MenuButton('Sensors for Setting Data')
        but_exclude_sensor_setting.clicked.connect(self.excludeSensorSetting)
        layout.addWidget(but_exclude_sensor_setting)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # excluding sensor for Add Line
        but_exclude_sensor_add_line = MenuButton('Add Line')
        but_exclude_sensor_add_line.clicked.connect(self.excludeSensorAddLine)
        layout.addWidget(but_exclude_sensor_add_line)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # excluding sensor for Dynamic Process
        but_exclude_sensor_dyp = MenuButton('Dynamic Process')
        but_exclude_sensor_dyp.clicked.connect(self.excludeSensorDYP)
        layout.addWidget(but_exclude_sensor_dyp)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # excluding sensor for EPD DATA
        but_exclude_sensor_epd = MenuButton('EPD DATA')
        but_exclude_sensor_epd.clicked.connect(self.excludeSensorEPD)
        layout.addWidget(but_exclude_sensor_epd)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # excluding sensor for General Counter
        but_exclude_sensor_general_counter = MenuButton('General Counter')
        but_exclude_sensor_general_counter.clicked.connect(self.excludeSensorGeneralCounter)
        layout.addWidget(but_exclude_sensor_general_counter)

        # _____________________________________________________________________
        # Filters for Selection
        lab_specific = LabelFrameNarrow('▸ Specific Sensor to select')
        layout.addWidget(lab_specific)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # excluding sensor for General Counter
        but_select_sensor_setting_data = MenuButton('Sensor with (setting data)')
        but_select_sensor_setting_data.clicked.connect(self.selectSensorSettingData)
        layout.addWidget(but_select_sensor_setting_data)

        # _____________________________________________________________________
        # Category Filters
        lab_category = LabelFrameNarrow('▸ Sensor Category')
        layout.addWidget(lab_category)
        rb_category_group = QButtonGroup()
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        list_category = ['ALL', 'ESC', 'Other', 'Pressure', 'RF', 'Temperature']
        for category in list_category:
            rb_category = RadioButton(category)
            if category == 'ALL':
                rb_category.setChecked(True)
            else:
                rb_category.setEnabled(False)
            rb_category_group.addButton(rb_category)
            layout.addWidget(rb_category)
        # _____________________________________________________________________
        # padding
        vpad = QWidget()
        vpad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addWidget(vpad)

    def excludeStep1(self):
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

    def excludeStepDechuck(self):
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

    def excludeSensorWOSetting(self):
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
        # get all of the step columns
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)
        #
        self.updateFeatures()

    def excludeStepSettingIs0(self):
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
                        model.setData(
                            index,
                            Qt.CheckState.Unchecked,
                            role=Qt.CheckStateRole
                        )
                    else:
                        model.setData(
                            index,
                            Qt.CheckState.Checked,
                            role=Qt.CheckStateRole
                        )
        self.updateFeatures()

    def excludeSensorSetting(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()

        features = self.getPanelSensorsFeatures()
        list_row = self.find_sensor_with_regex(features.pattern_sensor_setting)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

        self.updateFeatures()

    def excludeSensorOES(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()

        features = self.getPanelSensorsFeatures()
        list_row = self.find_sensor_with_regex(features.pattern_sensor_oes)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

        self.updateFeatures()

    def excludeSensorAddLine(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()

        features = self.getPanelSensorsFeatures()
        list_row = self.find_sensor_with_regex(features.pattern_sensor_add_line)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

        self.updateFeatures()

    def excludeSensorDYP(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()

        features = self.getPanelSensorsFeatures()
        list_row = self.find_sensor_with_regex(features.pattern_sensor_dyp)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

        self.updateFeatures()

    def excludeSensorEPD(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()

        features = self.getPanelSensorsFeatures()
        list_row = self.find_sensor_with_regex(features.pattern_sensor_epd)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

        self.updateFeatures()

    def excludeSensorGeneralCounter(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()

        features = self.getPanelSensorsFeatures()
        list_row = self.find_sensor_with_regex(features.pattern_sensor_general_counter)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

        self.updateFeatures()

    def selectSensorSettingData(self):
        but: QPushButton = self.sender()
        flag = but.isChecked()

        features = self.getPanelSensorsFeatures()
        list_row = self.find_sensor_without_regex(features.pattern_sensor_setting)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

        self.updateFeatures()
