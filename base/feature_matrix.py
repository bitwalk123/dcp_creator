from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QWidget


class FeatureMatrix(QWidget):
    """base class for managing matrix data
    """
    logMessage = Signal(str)
    name_sensor = 'Sensor Name'
    name_stat = 'Summary Stats'
    name_unit = 'unit'
    name_sel = 'selection'

    model = None
    style_cell = 'padding:2px 5px;'

    def __init__(self):
        super().__init__()

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

    def count_checkbox_checked(self):
        """
        count_checkbox_checked
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
        msg = 'layout (%d, %d) checked %d' % (rows, cols, count)
        self.logMessage.emit(msg)
        return count

    def find_header_label(self, key) -> int:
        """
        find_header_label
        """
        col = -1
        for i in range(self.model.columnCount()):
            item: QStandardItem = self.model.horizontalHeaderItem(i)
            if item.text() == key:
                col = i
                break
        return col
