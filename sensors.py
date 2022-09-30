from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)
from PySide6.QtWidgets import (
    QHeaderView,
    QSizePolicy,
)

from app_functions import is_num, timeit
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

    @timeit
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
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        table.setAlternatingRowColors(True)
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
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # At this moment, in order to save processing time,
                # it does not check if sensor/step certainly exists
                # in the exported CSV file or not.
                """
                result = self.features.checkFeatureValid(sensor, step)

                if not result:
                    # print(sensor, step)
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(Qt.CheckState.Checked)
                """
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

    def excludeLargeUnit(self, flag: bool):
        list_row = self.find_large_unit()
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorOES(self, flag: bool):
        list_row = self.find_sensor_oes()
        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSensorWithoutSetting(self, flag: bool, list_sensor_setting: list):
        list_sensor = list()
        for sensor in self.features.getSensors():
            if sensor not in list_sensor_setting:
                list_sensor.append(sensor)

        key_name = self.name_sensor
        col_name = self.find_header_label(key_name)
        list_row = list()
        for row in range(self.model.rowCount()):
            item: QStandardItem = self.model.item(row, col_name)
            sensor = item.text()
            if sensor in list_sensor:
                list_row.append(row)

        list_col = self.get_step_columns()
        self.swicth_check(list_row, list_col, flag)

    def excludeSetting0(self, flag: bool, dict_sensor_step_setting_0: dict):
        """
        excludeSetting0
        exclude sensor/step setting = 0
        """
        list_sensor_step_setting_0 = dict_sensor_step_setting_0.keys()
        key_name = self.name_sensor
        col_name = self.find_header_label(key_name)
        for row in range(self.model.rowCount()):
            item: QStandardItem = self.model.item(row, col_name)
            sensor = item.text()
            if sensor in list_sensor_step_setting_0:
                for step_name in dict_sensor_step_setting_0[sensor]:
                    col = self.find_header_label(step_name)
                    item: QStandardItem = self.model.item(row, col)
                    if item.isCheckable():
                        if flag:
                            item.setCheckState(Qt.CheckState.Unchecked)
                        else:
                            item.setCheckState(Qt.CheckState.Checked)

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

    def find_large_unit(self):
        list_row = list()
        # Unit
        key_unit = self.name_unit
        col_unit = self.find_header_label(key_unit)
        for row in range(self.model.rowCount()):
            item: QStandardItem = self.model.item(row, col_unit)
            unit = item.text()
            if unit == '[MPaG]' or unit == '[PaG]' or unit == '[Torr]':
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

    def find_sensor_oes(self):
        key = self.name_sensor
        col = self.find_header_label(key)
        list_row = list()
        pattern = self.features.pattern_sensor_oes
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


    def setSensorStep(self, flag: bool, list_sensor_step: list):
        info = {'step': list()}
        list_sensor = list()
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        for col in range(cols):
            item: QStandardItem = self.model.horizontalHeaderItem(col).text()
            if item == self.name_sensor:
                info[self.name_sensor] = col
            elif is_num(item):
                info['step'].append(item)
                info[item] = col

        for row in range(rows):
            item: QStandardItem = self.model.item(row, info[self.name_sensor])
            list_sensor.append(item.text().strip())

        for (sensor, step) in list_sensor_step:
            row = list_sensor.index(sensor)
            # item: QStandardItem = self.model.item(row, info[self.name_sensor])
            col = info[step]
            # print(sensor, ':', step, 'row', row, 'column', col, ':', item.text())
            item: QStandardItem = self.model.item(row, col)
            if item.isCheckable():
                if flag:
                    item.setCheckState(Qt.CheckState.Unchecked)
                else:
                    item.setCheckState(Qt.CheckState.Checked)

    def getDCP(self) -> dict:
        """
        get_dcp_current
        """

        rows = self.model.rowCount()
        # cols = self.model.columnCount()

        key_sensor = self.name_sensor
        col_sensor = self.find_header_label(key_sensor)
        key_unit = self.name_unit
        col_unit = self.find_header_label(key_unit)

        cols_step = self.get_step_columns()
        list_sensor_steps = list()
        for row in range(rows):
            for col in cols_step:
                item: QStandardItem = self.model.item(row, col)
                if item.isCheckable():
                    if item.checkState() == Qt.CheckState.Checked:
                        # count += 1
                        name_sensor = self.model.item(row, col_sensor).text()
                        name_unit = self.model.item(row, col_unit).text()
                        full_sensor = name_sensor + name_unit
                        name_step = self.model.horizontalHeaderItem(col).text()
                        dic_element = {'sensor': full_sensor, 'step': name_step}
                        list_sensor_steps.append(dic_element)
        dic_dcp = {'sensor_steps': list_sensor_steps, 'statistics': self.features.getStats()}
        return dic_dcp
