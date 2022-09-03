from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QWidget,
)

from app_widgets import (
    VBoxLayout,
    TableView,
)
from dcp_feature import FeatureInfo


class DCPMatrix(QWidget):
    """
    DCPMatrix class
    manage sensor selection
    """
    model = None
    style_cell = 'padding:2px 5px;'

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
        headers = ['Sensor Name', 'unit']
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

    def on_check_item(self, item: QStandardItem):
        """
        on_check_item
        examine check status
        """
        if item.isCheckable():
            row = item.row()
            col = item.column()
            if item.checkState() == Qt.CheckState.Checked:
                msg = 'checked'
            else:
                msg = 'unchecked'
            # print('(%d, %d) -> %s' % (row, col, msg))
