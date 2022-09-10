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
from feature_info import FeatureInfo


class DCPMatrix(FeatureMatrix):
    """
    DCPMatrix class
    manage sensor selection
    """

    def __init__(self, features: FeatureInfo):
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
                item.setCheckState(Qt.CheckState.Checked)
                item.setEditable(False)
                list_row.append(item)

            model.appendRow(list_row)
        #
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

    def excludeSensorForSetting(self, flag: bool):
        list_row = self.find_sensor_with_pattern()
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def get_step_columns(self):
        list_col = list()
        for col in range(self.model.columnCount()):
            item: QStandardItem = self.model.horizontalHeaderItem(col)
            if is_num(item.text()):
                list_col.append(col)
        return list_col

    def find_sensor_with_pattern(self):
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
        return list_row

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

    def count_checkbox_checked(self, layout):
        """
        count_checkbox_checked
        :param layout:
        :return:
        """
        count = 0
        rows = layout.rowCount()
        cols = layout.columnCount()
        print('layout (', rows, ',', cols, ')')
        for row in range(1, rows):
            for col in range(2, cols):
                item = layout.itemAtPosition(row, col)
                check = item.widget()
                if check.metaObject().className() == 'QCheckBox':
                    if check.checkState() == Qt.Checked:
                        count += 1
        return count

