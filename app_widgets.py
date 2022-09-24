from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QPalette,
    QStandardItem,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QProgressDialog,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class MenuButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet(
            'QPushButton {'
            'background-color: #eee;'
            'text-align: left;'
            'padding:5px 10px;'
            '}'
            'QPushButton:checked {'
            'background-color: white;'
            '}'
        )
        self.setCheckable(True)


class CheckBox(QCheckBox):
    """
    CheckBox
    This checkbox is for selecting/deselecting feature in the DCP matrix
    """

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        # self.setStyleSheet('QCheckBox {border:1px solid gray; margin-left:50%; margin-right:50%;}')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setChecked(True)


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)


class Label(QLabel):
    def __init__(self, *args):
        super().__init__(*args)


class LabelFrameNarrow(Label):
    def __init__(self, *args):
        super().__init__(*args)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLineWidth(1)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setStyleSheet(
            'QLabel {'
            'margin:1em 0 0 0; '
            'padding:0.05em 0.4em; '
            'background-color:#eef;font-size:9pt; '
            '}'
        )


class LabelCell(QLabel):
    """
    LabelCell
    label for the cell in the DCP matrix
    """

    def __init__(self, name: str, style_cell: str):
        super().__init__(name)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setStyleSheet(style_cell)


class LabelHead(QLabel):
    """
    LabelHead
    label for the header in the DCP matrix
    """

    def __init__(self, name: str, style_cell: str):
        super().__init__(name)
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setLineWidth(1)
        self.setStyleSheet(style_cell)


class LabelNumeric(LabelCell):
    """
    LabelNumeric
    """

    def __init__(self, num: Union[float, int], style_cell: str):
        super().__init__(str(num), style_cell)
        self.setAlignment(Qt.AlignRight)
        self.setStyleSheet('background-color:white;')
        # align

    def setValue(self, num: Union[float, int]):
        self.setText(str(num))


class LabelSensor(LabelCell):
    """
    LabelSensor
    label for sensor name in the DCP matrix

    note:
    This class overrides LabelCell class
    """

    def __init__(self, name: str, style_cell: str):
        super().__init__(name, style_cell)
        # background color
        pal = QPalette()
        pal.setColor(QPalette.Window, Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)


class FeatureMatrix(QWidget):
    name_sensor = 'Sensor Name'
    name_unit = 'unit'

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


class GridLayout(QGridLayout):
    """
    VBoxLayout
    """

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class Pad(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class RecipeItem(QStandardItem):
    status = 0

    def __init__(self, *args, status: int):
        super().__init__(*args)
        self.setTextAlignment(Qt.AlignRight)
        self.setStatus(status)

    def setStatus(self, status):
        if status == -1:
            # multiple values
            self.setValueMultiple()
        elif status == 0:
            # valid value
            self.setValueValid()
        elif status == 1:
            # setting data == 0
            self.setValueZero()
        else:
            pass
        #
        self.status = status

    def setValueMultiple(self):
        self.setBackground(QColor(255, 224, 224))

    def setValueValid(self):
        self.setBackground(QColor(240, 240, 255))
        self.setForeground(QBrush(QColor(0, 0, 32)))

    def setValueZero(self):
        self.setBackground(QColor(240, 240, 240))
        self.setForeground(QBrush(QColor(128, 128, 128)))


class TableView(QTableView):
    """
    VBoxLayout
    """

    def __init__(self):
        super().__init__()
        self.setCornerButtonEnabled(False)
        self.setStyleSheet(
            'QTableCornerButton::section {background-color:#ddd;}'
            'QHeaderView::section {background-color:#eee;}'
        )
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )


class VBoxLayout(QVBoxLayout):
    """
    VBoxLayout
    """

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class WorkInProgress(QProgressDialog):
    def __init__(self, parent):
        super().__init__(labelText='Working...', parent=parent)
        self.setWindowModality(Qt.WindowModal)
        self.setCancelButton(None)
        self.setRange(0, 0)
        self.setWindowTitle('progress')
