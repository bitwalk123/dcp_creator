from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QBrush,
    QColor,
    QPalette,
    QStandardItem, QIcon,
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
    QWidget, QStyle, QPlainTextEdit, QHBoxLayout,
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


class LogConsole(QWidget):
    prompt = '> '
    eol = '\n'

    def __init__(self):
        super().__init__()
        layout_horiz = QHBoxLayout()
        self.setLayout(layout_horiz)
        # log
        self.log = QPlainTextEdit()
        self.log.setFixedHeight(100)
        self.log.setStyleSheet('font-family: monospace;')
        self.log.setReadOnly(True)
        self.log.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout_horiz.addWidget(self.log)
        # control
        self.control = QWidget()
        layout_horiz.addWidget(self.control)
        #
        layout_vert = VBoxLayout()
        self.control.setLayout(layout_vert)
        # save log
        but_file = QPushButton(
            QIcon(self.style().standardIcon(QStyle.SP_FileDialogStart)),
            None
        )
        but_file.setToolTip('save log to file.')
        layout_vert.addWidget(but_file)
        # padding
        vpad = QWidget()
        layout_vert.addWidget(vpad)
        # trash log
        vpad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        but_trash = QPushButton(
            QIcon(self.style().standardIcon(QStyle.SP_TrashIcon)),
            None
        )
        but_trash.setToolTip('clear log on the console.')
        layout_vert.addWidget(but_trash)

    def insertIn(self, msg):
        line = msg + self.eol
        self.log.insertPlainText(line)

    def insertOut(self, msg):
        line = self.prompt + msg + self.eol
        self.log.insertPlainText(line)

    def insertCompleted(self, elapsed: float):
        line = 'done. (elapsed {:.3f} sec)'.format(elapsed) + self.eol
        self.log.insertPlainText(line)


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
    """
    FeatureMatrix
    base class for managing matrix data
    """
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
        print('layout (', rows, ',', cols, '),', 'checked', count)
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
    def __init__(self, parent, title='Working...'):
        super().__init__(parent=parent, labelText=title)
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        )
        self.setWindowModality(Qt.WindowModal)
        self.setCancelButton(None)
        self.setRange(0, 0)
        self.setWindowTitle('progress')
