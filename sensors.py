from PySide6.QtCore import (
    Qt,
    QRect,
)
from PySide6.QtGui import (
    QStandardItem,
)
from PySide6.QtWidgets import (
    QFrame,
    QHeaderView,
    QSizePolicy,
    QTableView,
)

from app_functions import timeit
from app_widgets import (
    FeatureMatrix,
    VBoxLayout, ProxyStyle4CheckBoxCenter, CheckBoxDelegate, SensorStepModel,
)
from features import Features
from sensors_chart import SensorChart


class Sensors(FeatureMatrix):
    """
    DCPMatrix class
    manage sensor selection
    """
    win_chart: SensorChart = None

    def __init__(self, features: Features):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # source
        self.features = features
        #
        self.init_ui()

    @timeit
    def init_ui(self):
        """
        init_ui
        initialize UI
        """
        layout = VBoxLayout()
        self.setLayout(layout)
        #
        table = QTableView()
        layout.addWidget(table)
        #
        table.setStyle(ProxyStyle4CheckBoxCenter())
        table.setWordWrap(False)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        # Horizontal Header
        head_horizontal = table.horizontalHeader()
        head_horizontal.setLineWidth(2)
        head_horizontal.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        table.setHorizontalHeader(head_horizontal)
        head_horizontal.setSectionResizeMode(QHeaderView.ResizeToContents)
        # Vertical Header
        head_vertical = table.verticalHeader()
        head_vertical.setLineWidth(2)
        head_vertical.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        head_vertical.sectionDoubleClicked.connect(self.on_row_section_double_clicked)
        head_vertical.setSectionResizeMode(QHeaderView.ResizeToContents)
        table.setVerticalHeader(head_vertical)

        delegate = CheckBoxDelegate(table)
        for col in range(self.features.getCheckColStart(), self.features.getCols()):
            table.setItemDelegateForColumn(col, delegate)
        model = SensorStepModel(self.features)
        table.setModel(model)
        self.model = model

        # set default status
        for row in range(self.features.getRows()):
            for col in range(self.features.getCheckColStart(), self.features.getCols()):
                index = model.index(row, col)
                model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)

    def find_sensor_time_dependent(self):
        # Sensor Name
        key_name = self.name_sensor
        col_name = self.find_header_label(key_name)
        list_row = list()
        list_pattern = [self.features.pattern_sensor_general_counter]
        for pattern in list_pattern:
            for row in range(self.model.rowCount()):
                item: QStandardItem = self.model.item(row, col_name)
                sensor = item.text()
                result = pattern.match(sensor)
                if result:
                    list_row.append(row)
        # Unit
        key_unit = self.name_unit
        col_unit = self.find_header_label(key_unit)
        for row in range(self.model.rowCount()):
            item: QStandardItem = self.model.item(row, col_unit)
            unit = item.text()
            if unit == '[sec]' \
                    or unit == '[min]' \
                    or unit == '[times]' \
                    or unit == '[L]' \
                    or unit == '[ms]' \
                    or unit == '[um]':
                list_row.append(row)

        return list_row

    # _________________________________________________________________________
    # apply new table model
    def count_checkbox_checked(self) -> int:
        count = 0
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        for row in range(self.features.getRows()):
            for col in range(self.features.getCheckColStart(), self.features.getCols()):
                index = self.model.index(row, col)
                value = self.model.data(index, role=Qt.CheckStateRole)
                if value == Qt.CheckState.Checked:
                    count += 1
        print('layout (', rows, ',', cols, '),', 'checked', count)
        return count

    def excludeSensorDYP(self, flag: bool):
        list_row = self.find_sensor_with_regex(self.features.pattern_sensor_dyp)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorEPD(self, flag: bool):
        list_row = self.find_sensor_with_regex(self.features.pattern_sensor_epd)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorOES(self, flag: bool):
        list_row = self.find_sensor_with_regex(self.features.pattern_sensor_oes)
        print(list_row)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorSetting(self, flag: bool):
        list_row = self.find_sensor_with_regex(self.features.pattern_sensor_setting)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorGeneralCounter(self, flag: bool):
        list_row = self.find_sensor_with_regex(self.features.pattern_sensor_general_counter)
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorWithoutSetting(self, flag: bool, list_sensor_setting: list):
        list_sensor = list()
        for sensor in self.features.getSensors():
            if sensor not in list_sensor_setting:
                list_sensor.append(sensor)

        list_row = list()
        for sensor in list_sensor:
            list_row.append(self.features.getSensors().index(sensor))

        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSetting0(self, flag: bool, dict_sensor_step_setting_0: dict):
        """
        excludeSetting0
        exclude sensor/step setting = 0
        """
        list_sensor_step_setting_0 = dict_sensor_step_setting_0.keys()
        for sensor in self.features.getSensors():
            row = self.features.getSensors().index(sensor)
            if sensor in list_sensor_step_setting_0:
                for step_name in dict_sensor_step_setting_0[sensor]:
                    col: int = self.find_header_label(step_name)

                    index = self.model.index(row, col)
                    if flag:
                        self.model.setData(index, Qt.CheckState.Unchecked, role=Qt.CheckStateRole)
                    else:
                        self.model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)

    def excludeStepMinus1(self, flag: bool):
        key = -1
        col = self.find_header_label(key)
        if col < 0:
            return
        self.switch_check_all_rows(col, flag)

    def excludeStepDechuck(self, flag: bool):
        list_col = list()
        for i in range(self.model.columnCount()):
            name_head = self.model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            if type(name_head) is not int:
                continue
            if name_head >= 1000:
                list_col.append(i)
        for col in list_col:
            self.switch_check_all_rows(col, flag)

    def find_header_label(self, key) -> int:
        col = -1
        for i in range(self.features.getCols()):
            name_head = self.model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            if name_head == key:
                col = i
                break
        return col

    def find_sensor_with_regex(self, pattern):
        list_row = list()
        for row in range(self.features.getRows()):
            sensor = self.features.getSensors()[row]
            result = pattern.match(sensor)
            if result:
                list_row.append(row)
        return list(set(list_row))

    def get_step_columns(self):
        list_col = list()
        for col in range(self.features.getCols()):
            name_head = self.model.headerData(col, Qt.Horizontal, Qt.DisplayRole)
            if type(name_head) is int:
                list_col.append(col)
        return list_col

    def swicth_check(self, list_row, list_col, flag):
        for row in list_row:
            for col in list_col:
                index = self.model.index(row, col)
                if flag:
                    self.model.setData(index, Qt.CheckState.Unchecked, role=Qt.CheckStateRole)
                else:
                    self.model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)

    def switch_check_all_rows(self, col, flag):
        for row in range(self.features.getRows()):
            index = self.model.index(row, col)
            if flag:
                self.model.setData(index, Qt.CheckState.Unchecked, role=Qt.CheckStateRole)
            else:
                self.model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)

    def getDCP(self) -> list:
        """get sensor/tep currently selected.
        """

        rows = self.model.rowCount()
        cols_step = self.get_step_columns()
        list_sensor_steps = list()
        for row in range(rows):
            for col in cols_step:
                index = self.model.index(row, col)
                value = self.model.data(index, role=Qt.CheckStateRole)
                if value == Qt.CheckState.Checked:
                    name_sensor = self.features.getSensors()[row]
                    name_unit = self.features.getUnits()[name_sensor]
                    num_step = self.model.headerData(col, Qt.Horizontal, Qt.DisplayRole)
                    full_sensor = name_sensor + name_unit
                    dict_element = {'sensor': full_sensor, 'step': str(num_step)}
                    list_sensor_steps.append(dict_element)
        return list_sensor_steps

    def on_row_section_double_clicked(self, row: int):
        winrect: QRect = None
        if self.win_chart is not None:
            winrect = self.win_chart.geometry()
            self.win_chart.close()
        self.win_chart = SensorChart(self, self.features, row)
        if winrect is not None:
            self.win_chart.setGeometry(winrect)
        self.win_chart.show()
