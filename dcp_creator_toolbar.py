from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QSizePolicy,
    QStyle,
    QToolBar,
    QToolButton,
    QWidget,
)


class DCPCreatorToolBar(QToolBar):
    """
    DCPCreatorToolBar
    toolbar class of the sensor window
    """
    openClicked = Signal()
    dcpClicked = Signal()
    saveClicked = Signal()

    def __init__(self):
        super().__init__()
        # _____________________________________________________________________
        # Open button
        button_open = QToolButton()
        button_open.setStyleSheet('margin:0 1em 0 0;')
        button_open.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_open.setIcon(
            QIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        )
        button_open.setToolTip('read summary stat data exported from the Fleet Analysis Tool.')
        button_open.clicked.connect(self.openClicked.emit)
        self.addWidget(button_open)
        self.addSeparator()
        # _____________________________________________________________________
        # Load saved DCP
        button_dcp = QToolButton()
        button_dcp.setStyleSheet('margin:0 1em;')
        button_dcp.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_dcp.setIcon(
            QIcon(self.style().standardIcon(QStyle.SP_DriveFDIcon))
        )
        button_dcp.setToolTip('load DCP file previously saved.')
        button_dcp.clicked.connect(self.dcpClicked.emit)
        self.addWidget(button_dcp)
        self.addSeparator()
        # Pad
        pad = QWidget()
        pad.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addWidget(pad)
        self.addSeparator()
        # _____________________________________________________________________
        # Save button
        button_save = QToolButton()
        button_save.setStyleSheet('margin:0 0 0 1em;')
        button_save.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_save.setIcon(
            QIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        )
        button_save.setToolTip('save DCP info importing to the Fleet Analysis Tool.')
        button_save.clicked.connect(self.saveClicked.emit)
        self.addWidget(button_save)
