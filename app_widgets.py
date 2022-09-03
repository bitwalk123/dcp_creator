from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QFrame,
    QHeaderView,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
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
    checkbox for selecting/deselecting feature in the DCP matrix
    """

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        # self.setStyleSheet('QCheckBox {border:1px solid gray; margin-left:50%; margin-right:50%;}')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setChecked(True)


# check.setAutoFillBackground(True)

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
