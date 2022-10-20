from PySide6.QtCore import (
    Qt,
    QRect, Signal,
)
from PySide6.QtGui import (
    QStandardItem,
)
from PySide6.QtWidgets import (
    QHeaderView,
    QSizePolicy,
    QTableView,
)

from app_widgets import (
    CheckBoxDelegate,
    FeatureMatrix,
    ProxyStyle4CheckBoxCenter,
    SensorStepModel,
    VBoxLayout,
)
from features import Features
from sensors_chart import SensorChart


class Sensors(FeatureMatrix):
    """
    DCPMatrix class
    manage sensor selection
    """
    logMessage = Signal(str)
    win_chart: SensorChart = None

    def __init__(self, features: Features):
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
        table = QTableView()
        model = SensorStepModel(self.features)
        table.setModel(model)
        # table = MyTableView(model)
        table.setStyleSheet(self.features.style_disp)
        layout.addWidget(table)

        table.setWordWrap(False)
        table.setAlternatingRowColors(True)
        # Vertical Header
        head_vertical = table.verticalHeader()
        head_vertical.setDefaultAlignment(Qt.AlignRight)
        head_vertical.setSectionResizeMode(QHeaderView.ResizeToContents)
        head_vertical.sectionDoubleClicked.connect(self.on_row_section_double_clicked)
        # checkbox delegation
        delegate = CheckBoxDelegate(table)
        for col in range(self.features.getCheckColStart(), self.features.getCols()):
            table.setItemDelegateForColumn(col, delegate)
        table.setStyle(ProxyStyle4CheckBoxCenter())
        # column width (Sensor Name and Unit)
        width_char = table.fontMetrics().averageCharWidth()
        head_horizontal = table.horizontalHeader()
        for col in range(model.getCheckColStart()):
            list_str = list()
            if col == 0:
                list_str = self.features.getSensorNameMaxLen()
            elif col == 1:
                list_str = self.features.getUnitNameMaxLen()
            width = 0
            for name in list_str:
                qsize = table.fontMetrics().size(Qt.TextSingleLine, name)
                if qsize.width() > width:
                    width = qsize.width()
            head_horizontal.resizeSection(col, width + width_char * 2)
        # column width (CheckBox)
        for col in range(model.getCheckColStart(), model.columnCount()):
            table.resizeColumnToContents(col)
        # set default status
        for row in range(self.features.getRows()):
            for col in range(self.features.getCheckColStart(), self.features.getCols()):
                index = model.index(row, col)
                model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)

        self.model = model

    def getModel(self):
        return self.model

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
        msg = 'layout (%d, %d) checked %d' % (rows, cols, count)
        self.logMessage.emit(msg)
        return count

    def find_header_label(self, key) -> int:
        col = -1
        for i in range(self.features.getCols()):
            name_head = self.model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            if name_head == key:
                col = i
                break
        return col

    def on_row_section_double_clicked(self, row: int):
        winrect: QRect = None
        if self.win_chart is not None:
            winrect = self.win_chart.geometry()
            self.win_chart.close()
        self.win_chart = SensorChart(self, self.features, row)
        if winrect is not None:
            self.win_chart.setGeometry(winrect)
        self.win_chart.show()
