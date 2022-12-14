from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel,
)
from PySide6.QtWidgets import QSizePolicy, QHeaderView

from app_functions import is_num
from app_widgets import (
    TableView,
    VBoxLayout,
)
from base.recipe_item import RecipeItem
from base.feature_matrix import FeatureMatrix
from features import Features


class Recipe(FeatureMatrix):
    def __init__(self, features: Features):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # source
        self.features = features
        # UI
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        layout = VBoxLayout()
        self.setLayout(layout)
        #
        table = TableView()
        model = QStandardItemModel()
        # headers
        headers = [self.name_sensor, self.name_unit]
        headers.extend([str(n) for n in self.features.getSteps() if n > 0])
        model.setHorizontalHeaderLabels(headers)
        model.itemChanged.connect(self.on_check_item)
        table.setModel(model)
        table.setStyleSheet(self.features.style_disp)
        table.setWordWrap(False)
        head_vertical = table.verticalHeader()
        head_vertical.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        head_vertical.setDefaultAlignment(Qt.AlignRight)
        layout.addWidget(table)
        # pattern with (setting data)
        pattern = self.features.pattern_sensor_setting
        sensors_setting = list()
        units_setting = list()
        sensors_setting_step = {}
        for sensor in self.features.getSensors():
            # check if sensor has (setting data)
            result = pattern.match(sensor)
            if not result:
                continue
            name_sensor = result.group(1)
            sensors_setting.append(name_sensor)
            list_row = list()
            # sensor
            item = QStandardItem()
            item.setText(name_sensor)
            list_row.append(item)
            # unit
            item = QStandardItem()
            unit_sensor = self.features.getUnits()[sensor]
            units_setting.append(unit_sensor)
            item.setText(unit_sensor)
            list_row.append(item)
            # step
            sensors_setting_step[name_sensor] = {}
            for step in self.features.getSteps():
                if step <= 0:
                    continue
                list_value = self.features.getFeatureValue(sensor, step)
                if len(list_value) == 1:
                    str_value = str(list_value[0])
                    if str_value == '0.0':
                        # setting data == 0
                        item = RecipeItem(str_value, status=1)
                    else:
                        # Valid value
                        if is_num(str_value):
                            str_value_new = str(round(float(str_value), 1))
                            item = RecipeItem(str_value_new, status=0)
                        else:
                            item = RecipeItem(str_value, status=0)
                            str_value_new = str_value

                        sensors_setting_step[name_sensor][step] = str_value_new
                else:
                    # multiple values
                    item = RecipeItem('', status=-1)

                item.setEditable(False)
                list_row.append(item)

            model.appendRow(list_row)

        # adjust specific column width
        width_char = table.fontMetrics().averageCharWidth()
        head_horizontal = table.horizontalHeader()
        # Sensor column
        sensor_chars_max = max([len(sensor) for sensor in sensors_setting])
        width = width_char * (sensor_chars_max + 2)
        head_horizontal.resizeSection(0, width)
        # Unit column
        unit_chars_max = max([len(unit) for unit in units_setting])
        width = width_char * (unit_chars_max + 2)
        head_horizontal.resizeSection(1, width)
        # Steps
        for col in range(2, model.columnCount()):
            table.resizeColumnToContents(col)
        #
        self.features.setSensorSetting(sensors_setting)
        self.features.setSensorSettingStep(sensors_setting_step)
        self.model = model

    def excludeGasFlow0(self, flag: bool) -> list:
        pattern = self.features.pattern_gas_flow
        return self.get_sensor_step_zero(pattern)
        # print(list_zero)
        # print('Complete!')

    def excludeRFPower0(self, flag: bool):
        pattern = self.features.pattern_rf_power
        return self.get_sensor_step_zero(pattern)

    def get_sensor_step_zero(self, pattern):
        list_zero = list()
        info = {'step': list()}
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
            sensor = item.text().strip()
            result = pattern.match(sensor)
            if result:
                for step_name in info['step']:
                    col = info[step_name]
                    item_step: QStandardItem = self.model.item(row, col)
                    value_str = item_step.text().strip()
                    if value_str is None:
                        continue
                    if not is_num(value_str):
                        continue
                    value = float(value_str)
                    if value != 0.0:
                        continue
                    list_zero.append([sensor, step_name])
        return list_zero

    def getSensorWithSetting(self) -> list:
        list_sensor = list()
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        col_sensor = 0
        for col in range(cols):
            item: QStandardItem = self.model.horizontalHeaderItem(col)
            label_item = item.text()
            if label_item == self.name_sensor:
                col_sensor = col
                break
        for row in range(rows):
            item: QStandardItem = self.model.item(row, col_sensor)
            sensor = item.text().strip()
            list_sensor.append(sensor)
        return list_sensor

    def getSensorStepSetting0(self) -> dict:
        """
        getSensorStepSetting0
        get sensor/step where setting = 0
        """
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        col_sensor = 0
        dict_col_step = {}
        for col in range(cols):
            item: QStandardItem = self.model.horizontalHeaderItem(col)
            label_item = item.text().strip()
            if label_item == self.name_sensor:
                col_sensor = col
            elif is_num(label_item):
                dict_col_step[int(label_item)] = col

        dict_sensor_step = {}
        for row in range(rows):
            item: QStandardItem = self.model.item(row, col_sensor)
            sensor = item.text().strip()
            list_label_step = list()
            for label_step in dict_col_step.keys():
                col = dict_col_step[label_step]
                item: QStandardItem = self.model.item(row, col)
                label_step_value = item.text()
                if is_num(label_step_value):
                    value = float(label_step_value)
                    if value == 0.0:
                        list_label_step.append(label_step)
            if len(list_label_step) > 0:
                dict_sensor_step[sensor] = list_label_step

        return dict_sensor_step
