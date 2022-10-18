from typing import Union, Any

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex, Signal,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QPalette,
    QStandardItem, QTextCursor,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QProgressDialog,
    QProxyStyle,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QTableView,
    QVBoxLayout,
    QWidget, QMainWindow,
)

from features import Features


class MenuButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet(
            'QPushButton {'
            'text-align: left;'
            'padding:0.1em 1em;'
            'font-family: monospace;'
            'font-size: 10pt;'
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
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setChecked(True)


class LogConsole(QWidget):
    prompt = '> '
    eol = '\n'

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        layout_horiz = QHBoxLayout()
        layout_horiz.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout_horiz)
        # log
        self.log = QPlainTextEdit()
        self.log.setFixedHeight(100)
        self.log.setStyleSheet(
            'font-family: monospace; '
            'font-size: 9pt; '
            'padding: 5px 5px;'
        )
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
        but_file.setContentsMargins(0, 0, 0, 0)
        layout_vert.addWidget(but_file)
        layout_vert.setContentsMargins(0, 0, 0, 0)
        # padding
        vpad = QWidget()
        vpad.setContentsMargins(0, 0, 0, 0)
        layout_vert.addWidget(vpad)
        vpad.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # trash log
        but_trash = QPushButton(
            QIcon(self.style().standardIcon(QStyle.SP_TrashIcon)),
            None
        )
        but_trash.setContentsMargins(0, 0, 0, 0)
        but_trash.setToolTip('clear log on the console.')
        layout_vert.addWidget(but_trash)

    def insertLine(self, line):
        self.log.insertPlainText(line)
        self.log.moveCursor(QTextCursor.End)

    def insertIn(self, msg):
        line = msg + self.eol
        self.insertLine(line)

    def insertOut(self, msg):
        line = self.prompt + msg + self.eol
        self.insertLine(line)

    def insertCompleted(self, elapsed: float):
        line = 'done. (elapsed {:.3f} sec)'.format(elapsed) + self.eol
        self.insertLine(line)

    def insertAttention(self):
        line = '■■■ ATTENTION ■■■' + self.eol
        self.insertLine(line)


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)


class Label(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setContentsMargins(0, 0, 0, 0)


class LabelFrameNarrow(Label):
    def __init__(self, *args, flag=False):
        super().__init__(*args)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(1)
        if flag:
            style_sheet = (
                'QLabel {'
            )
        else:
            style_sheet = (
                'QLabel {'
                'margin: 1em 0 0 0;'
            )

        style_sheet += (
            'padding: 0.1em 0.4em; '
            'font-family: monospace;'
            'font-size: 9pt;'
            '}'
        )
        self.setStyleSheet(style_sheet)


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


class RadioButton(QRadioButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('padding: 0 1em;')


class RecipeItem(QStandardItem):
    status = 0

    def __init__(self, *args, status: int):
        super().__init__(*args)
        self.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
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


class TabWindow(QMainWindow):
    """Tab Window/Panel/Tab
    """
    logMessage = Signal(str)

    def __init__(self):
        super().__init__()

    def showLog(self, msg: str):
        self.logMessage.emit(msg)


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


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# related to the table with checkbox
# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
class ProxyStyle4CheckBoxCenter(QProxyStyle):
    def subElementRect(self, element, opt, widget=None):
        if element == self.SE_ItemViewItemCheckIndicator:
            rect = super().subElementRect(element, opt, widget)
            rect.moveCenter(opt.rect.center())
            return rect
        return super().subElementRect(element, opt, widget)


class CheckBoxDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index: QModelIndex):
        value = index.data(Qt.CheckStateRole)
        if value is None:
            model = index.model()
            model.setData(index, Qt.Unchecked, Qt.CheckStateRole)
        super().initStyleOption(option, index)


class SensorStepModel(QAbstractTableModel):
    def __init__(self, data: Features):
        super(SensorStepModel, self).__init__()
        self._data = data
        # self.check_states = dict()

    def rowCount(self, index: QModelIndex = None):
        return self._data.getRows()

    def columnCount(self, index: QModelIndex = None):
        return self._data.getCols()

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._data.getData(row, column)
            return value

        if role == Qt.CheckStateRole:
            value = self._data.check_states.get(QPersistentModelIndex(index))
            if value is not None:
                return value

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole = Qt.EditRole):
        if role == Qt.CheckStateRole:
            self._data.check_states[QPersistentModelIndex(index)] = value
            self.dataChanged.emit(index, index, (role,))
            return True

        return False

    def getCheckColStart(self):
        return self._data.getCheckColStart()

    def flags(self, index: QModelIndex):
        # return (
        #        Qt.ItemIsEnabled
        #        | Qt.ItemIsSelectable
        #        | Qt.ItemIsUserCheckable
        # )
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.column() >= self.getCheckColStart():
            # return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            return (
                    Qt.ItemIsEnabled
                    | Qt.ItemIsSelectable
                    | Qt.ItemIsUserCheckable
            )

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.getColumnHeader(section)
            elif orientation == Qt.Vertical:
                return self._data.getRowIndex(section)


class FrozenTableView(QTableView):
    def __init__(self, parent: QTableView = None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setFocusPolicy(Qt.NoFocus)
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().hide()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)


class MyTableView(QTableView):
    def __init__(self, model: SensorStepModel, parent=None, *args):
        QTableView.__init__(self, parent, *args)
        self.setModel(model)
        # self.setMinimumSize(800, 400)
        self.setEditTriggers(QAbstractItemView.SelectedClicked)
        self.setStyleSheet('font-family: monospace;')
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        # self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        for col in range(model.getCheckColStart()):
            self.setColumnWidth(col, self.sizeHintForColumn(col))
            self.horizontalHeader().resizeSection(col, self.sizeHintForColumn(col))
            # self.resizeColumnToContents(col)

        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        # FrozenTableView
        self.frozenTableView = FrozenTableView(self)
        self.frozenTableView.setModel(model)
        # self.frozenTableView.setSelectionModel(QAbstractItemView.selectionModel(self))
        for col in range(model.getCheckColStart()):
            self.frozenTableView.setColumnWidth(col, self.frozenTableView.sizeHintForColumn(col))
            self.frozenTableView.horizontalHeader().resizeSection(col, self.frozenTableView.sizeHintForColumn(col))
            # self.frozenTableView.resizeColumnToContents(col)
        # self.frozenTableView.resizeColumnsToContents()
        self.viewport().stackUnder(self.frozenTableView)
        self.frozenTableView.show()
        self.updateFrozenTableGeometry()

        # connect the headers and scrollbars of both tableviews together
        self.verticalScrollBar().valueChanged.connect(
            self.frozenTableView.verticalScrollBar().setValue
        )
        self.frozenTableView.verticalScrollBar().valueChanged.connect(
            self.verticalScrollBar().setValue
        )

    def resizeEvent(self, event):
        QTableView.resizeEvent(self, event)
        self.updateFrozenTableGeometry()

    def scrollTo(self, index, hint):
        if index.column() > 1:
            QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(
                self.verticalHeader().width() + self.frameWidth(),
                self.frameWidth(),
                self.columnWidth(0) + self.columnWidth(1),
                self.viewport().height() + self.horizontalHeader().height()
            )
        else:
            self.frozenTableView.setGeometry(
                self.frameWidth(),
                self.frameWidth(),
                self.columnWidth(0) + self.columnWidth(1),
                self.viewport().height() + self.horizontalHeader().height()
            )

    def moveCursor(self, cursorAction, modifiers):
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        x = self.visualRect(current).topLeft().x()
        frozen_width = self.frozenTableView.columnWidth(0) + self.frozenTableView.columnWidth(1)
        if cursorAction == self.MoveLeft and current.column() > 1 and x < frozen_width:
            new_value = self.horizontalScrollBar().value() + x - frozen_width
            self.horizontalScrollBar().setValue(new_value)
        return current
