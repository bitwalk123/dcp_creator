from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)
from PySide6.QtWidgets import QSizePolicy

from app_functions import is_num
from app_widgets import (
    FeatureMatrix,
    TableView,
    VBoxLayout,
)
from features import Features


class Sensors(FeatureMatrix):
    """
    DCPMatrix class
    manage sensor selection
    """

    def __init__(self, features: Features):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # source
        self.features = features
        #
        self.init_ui()
        # count = self.count_checkbox_checked(layout)
        # print('original count', count)

    def init_ui(self):
        """
        init_ui
        initialize UI
        """
        layout = VBoxLayout()
        self.setLayout(layout)
        #
        table = TableView()
        model = QStandardItemModel()
        # headers
        headers = [self.name_sensor, self.name_unit]
        headers.extend([str(n) for n in self.features.getSteps()])
        model.setHorizontalHeaderLabels(headers)
        model.itemChanged.connect(self.on_check_item)
        table.setModel(model)
        table.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        layout.addWidget(table)

        for sensor in self.features.getSensors():
            list_row = list()
            # sensor
            item = QStandardItem()
            item.setText(sensor)
            list_row.append(item)
            # unit
            item = QStandardItem()
            item.setText(self.features.getUnits()[sensor])
            list_row.append(item)
            # step
            for step in self.features.getSteps():
                item = QStandardItem()
                item.setCheckable(True)
                item.setEditable(False)
                result = self.features.checkFeatureVaid(sensor, step)
                if not result:
                    print(sensor, step)
                item.setCheckState(Qt.CheckState.Checked)
                list_row.append(item)

            model.appendRow(list_row)
        # set the model to member variable
        self.model = model

    def excludeStepMinus1(self, flag: bool):
        key = '-1'
        col = self.find_header_label(key)
        if col < 0:
            return
        self.switch_check_all_rows(col, flag)

    def excludeStepDechuck(self, flag: bool):
        list_col = list()
        for i in range(self.model.columnCount()):
            item: QStandardItem = self.model.horizontalHeaderItem(i)
            name_head = item.text()
            if not name_head.isdecimal():
                continue
            if int(name_head) >= 1000:
                list_col.append(i)
        for col in list_col:
            self.switch_check_all_rows(col, flag)

    def excludeSensorSetting(self, flag: bool):
        list_row = self.find_sensor_setting()
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorTimeDependent(self, flag: bool):
        list_row = self.find_sensor_time_dependent()
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorDYP(self, flag: bool):
        list_row = self.find_sensor_dyp()
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorEPD(self, flag: bool):
        list_row = self.find_sensor_epd()
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def get_step_columns(self):
        list_col = list()
        for col in range(self.model.columnCount()):
            item: QStandardItem = self.model.horizontalHeaderItem(col)
            if is_num(item.text()):
                list_col.append(col)
        return list_col

    def find_sensor_setting(self):
        key = self.name_sensor
        col = self.find_header_label(key)
        list_row = list()
        pattern = self.features.pattern_sensor_setting
        for row in range(self.model.rowCount()):
            item: QStandardItem = self.model.item(row, col)
            sensor = item.text()
            result = pattern.match(sensor)
            if result:
                list_row.append(row)
        return list(set(list_row))

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
        for pattern in list_pattern:
            for row in range(self.model.rowCount()):
                item: QStandardItem = self.model.item(row, col_unit)
                unit = item.text()
                # result = pattern.match(unit)
                if unit == '[min]' or unit == '[times]':
                    list_row.append(row)

        return list_row

    def find_sensor_dyp(self):
        key = self.name_sensor
        col = self.find_header_label(key)
        list_row = list()
        pattern = self.features.pattern_sensor_dyp
        for row in range(self.model.rowCount()):
            item: QStandardItem = self.model.item(row, col)
            sensor = item.text()
            result = pattern.match(sensor)
            if result:
                list_row.append(row)
        return list(set(list_row))

    def find_sensor_epd(self):
        key = self.name_sensor
        col = self.find_header_label(key)
        list_row = list()
        pattern = self.features.pattern_sensor_epd
        for row in range(self.model.rowCount()):
            item: QStandardItem = self.model.item(row, col)
            sensor = item.text()
            result = pattern.match(sensor)
            if result:
                list_row.append(row)
        return list(set(list_row))

    def swicth_check(self, list_row, list_col, flag):
        for row in list_row:
            for col in list_col:
                item: QStandardItem = self.model.item(row, col)
                if item.isCheckable():
                    if flag:
                        item.setCheckState(Qt.CheckState.Unchecked)
                    else:
                        item.setCheckState(Qt.CheckState.Checked)

    def switch_check_all_rows(self, col, flag):
        rows = self.model.rowCount()
        for row in range(rows):
            item: QStandardItem = self.model.item(row, col)
            if item.isCheckable():
                if flag:
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(Qt.CheckState.Checked)

    def find_header_label(self, key):
        col = -1
        for i in range(self.model.columnCount()):
            item: QStandardItem = self.model.horizontalHeaderItem(i)
            if item.text() == key:
                col = i
                break
        return col

    def count_checkbox_checked(self):
        """
        count_checkbox_checked
        :param layout:
        :return:
        """
        count = 0
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        for row in range(rows):
            for col in range(cols):
                item: QStandardItem = self.model.item(row, col)
                if item.isCheckable():
                    if item.checkState() == Qt.CheckState.Checked:
                        count += 1
        print('layout (', rows, ',', cols, '),', 'checked', count)
        return count
