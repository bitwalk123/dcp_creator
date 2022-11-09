from typing import Union, Any

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
)
from PySide6.QtGui import (
    QIcon,
    QPalette,
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
    QProgressDialog,
    QProxyStyle,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QTableView,
    QVBoxLayout,
    QWidget, QMessageBox,
)

from features import Features


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


class ComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)


class DialogWarn(QMessageBox):
    def __init__(self, msg: str):
        super().__init__()
        self.setWindowTitle('Warning')
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning))
        )
        self.setText(msg)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.setIcon(QMessageBox.Icon.Warning)


class Label(QLabel):
    def __init__(self, *args):
        super().__init__(*args)
        self.setContentsMargins(0, 0, 0, 0)


class LabelFrameNarrow(Label):
    def __init__(self, *args, flag=False):
        super().__init__(*args)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
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
            'color #444400;'
            'background-color: #fffff8;'
            'font-family: monospace;'
            'font-size: 9pt;'
            'font-weight: bold;'
            '}'
        )
        self.setStyleSheet(style_sheet)


class LabelCell(QLabel):
    """    LabelCell
    label for the cell in the DCP matrix
    """

    def __init__(self, name: str, style_cell: str):
        super().__init__(name)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.setStyleSheet(style_cell)


class LabelHead(QLabel):
    """
    LabelHead
    label for the header in the DCP matrix
    """

    def __init__(self, name: str, style_cell: str):
        super().__init__(name)
        self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        self.setLineWidth(1)
        self.setStyleSheet(style_cell)


class LabelNumeric(LabelCell):
    """
    LabelNumeric
    """

    def __init__(self, num: Union[float, int, str], style_cell: str):
        super().__init__(str(num), style_cell)
        self.setAlignment(Qt.AlignRight)
        # self.setStyleSheet('background-color:white;')
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


class GridLayout(QGridLayout):
    """
    VBoxLayout
    """

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class HBoxLayout(QHBoxLayout):
    """HBoxLayout
    """

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)


class MenuButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet(
            'QPushButton {'
            'padding:0.25em 1em;'
            'text-align: left;'
            'font-family: monospace;'
            'font-size: 10pt;'
            '}'
        )
        self.setCheckable(True)


class OptionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        )
        self.setWindowTitle('Option Window')
        layout = QVBoxLayout()
        self.label = QLabel('Not Implemented yet!')
        layout.addWidget(self.label)
        self.setLayout(layout)


class Pad(QWidget):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class RadioButton(QRadioButton):
    def __init__(self, *args):
        super().__init__(*args)
        # self.setStyleSheet('padding: 0 1em;')
        self.setStyleSheet(
            'QRadioButton {'
            'padding:0.05em 1em;'
            'text-align: left;'
            'font-family: monospace;'
            'font-size: 10pt;'
            '}'
        )


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
            QHeaderView.ResizeMode.ResizeToContents
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
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation))
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
        if element == self.SubElement.SE_ItemViewItemCheckIndicator:
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

    def rowCount(self, index: QModelIndex = None):
        return self._data.getRows()

    def columnCount(self, index: QModelIndex = None):
        return self._data.getCols()

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
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
            # TODO
            self.dataChanged.emit(index, index, (role,))
            return True

        return False

    def getCheckColStart(self):
        return self._data.getCheckColStart()

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.column() >= self.getCheckColStart():
            return (
                    Qt.ItemIsEnabled
                    | Qt.ItemIsSelectable
                    | Qt.ItemIsUserCheckable
            )

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
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
        self.verticalHeader().hide()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)


class MyTableView(QTableView):
    def __init__(self, model: SensorStepModel, parent=None, *args):
        QTableView.__init__(self, parent, *args)
        self.setModel(model)
        self.setEditTriggers(QAbstractItemView.EditTrigger.SelectedClicked)
        self.setStyleSheet('font-family: monospace;')
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.setAlternatingRowColors(True)
        for col in range(model.getCheckColStart()):
            self.setColumnWidth(col, self.sizeHintForColumn(col))
            self.horizontalHeader().resizeSection(col, self.sizeHintForColumn(col))

        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        # FrozenTableView
        self.frozenTableView = FrozenTableView(self)
        self.frozenTableView.setModel(model)
        for col in range(model.getCheckColStart()):
            self.frozenTableView.setColumnWidth(col, self.frozenTableView.sizeHintForColumn(col))
            self.frozenTableView.horizontalHeader().resizeSection(col, self.frozenTableView.sizeHintForColumn(col))
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
        # TODO
        if cursorAction == self.MoveLeft and current.column() > 1 and x < frozen_width:
            new_value = self.horizontalScrollBar().value() + x - frozen_width
            self.horizontalScrollBar().setValue(new_value)
        return current
