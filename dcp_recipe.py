from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel,
    Qt, QColor, QBrush,
)
from PySide6.QtWidgets import QSizePolicy

from app_widgets import (
    FeatureMatrix,
    TableView,
    VBoxLayout, RecipeItem,
)
from dcp_feature import FeatureInfo


class DCPRecipe(FeatureMatrix):
    def __init__(self, features: FeatureInfo):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # source
        self.features = features
        #
        self.init_ui()

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
        headers.extend([str(n) for n in self.features.getSteps() if n > 0])
        model.setHorizontalHeaderLabels(headers)
        model.itemChanged.connect(self.on_check_item)
        table.setModel(model)
        layout.addWidget(table)

        pattern = self.features.pattern_sensor_setting
        for sensor in self.features.getSensors():
            result = pattern.match(sensor)
            if not result:
                continue
            name_sensor = result.group(1)
            list_row = list()
            # sensor
            item = QStandardItem()
            item.setText(name_sensor)
            list_row.append(item)
            # unit
            item = QStandardItem()
            item.setText(self.features.getUnits()[sensor])
            list_row.append(item)
            # step
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
                        # valid value
                        item = RecipeItem(str_value, status=0)
                else:
                    # multiple values
                    item = RecipeItem('', status=-1)

                item.setEditable(False)
                list_row.append(item)

            model.appendRow(list_row)
        #
        self.model = model
