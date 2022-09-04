from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel,
    Qt,
)
from PySide6.QtWidgets import QSizePolicy

from app_widgets import (
    FeatureMatrix,
    TableView,
    VBoxLayout,
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
        headers.extend([str(n) for n in self.features.getSteps()])
        model.setHorizontalHeaderLabels(headers)
        model.itemChanged.connect(self.on_check_item)
        table.setModel(model)
        layout.addWidget(table)

        pattern = self.features.pattern_sensor_setting
        for sensor in self.features.getSensors():
            result = pattern.match(sensor)
            if not result:
                continue

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
                item.setEditable(False)
                list_row.append(item)

            model.appendRow(list_row)
        #
        self.model = model
