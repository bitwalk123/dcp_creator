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
    openCSVClicked = Signal()
    dcpReadClicked = Signal()
    dcpSaveClicked = Signal()

    def __init__(self):
        super().__init__()
        # _____________________________________________________________________
        # Open button
        button_open = QToolButton()
        button_open.setStyleSheet('margin:0 1em 0 0;')
        button_open.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_open.setIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        )
        button_open.setToolTip('read Summary Stat data.')
        button_open.clicked.connect(self.openCSVClicked.emit)
        self.addWidget(button_open)
        self.addSeparator()
        # _____________________________________________________________________
        # Load saved DCP
        button_dcp = QToolButton()
        button_dcp.setStyleSheet('margin:0 1em;')
        button_dcp.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_dcp.setIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DriveFDIcon))
        )
        button_dcp.setToolTip('load DCP file in JSON, previously saved.')
        button_dcp.clicked.connect(self.dcpReadClicked.emit)
        self.addWidget(button_dcp)
        self.addSeparator()
        # Pad
        pad = QWidget()
        pad.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addWidget(pad)
        self.addSeparator()
        # _____________________________________________________________________
        # Option button
        button_option = QToolButton()
        button_option.setStyleSheet('margin:0 1em;')
        button_option.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_option.setIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        )
        button_option.setToolTip('Various options and utilities.')
        self.addWidget(button_option)
        self.addSeparator()
        # _____________________________________________________________________
        # Save button
        button_save = QToolButton()
        button_save.setStyleSheet('margin:0 0 0 1em;')
        button_save.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_save.setIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton))
        )
        button_save.setToolTip('save DCP file in JSON.')
        button_save.clicked.connect(self.dcpSaveClicked.emit)
        self.addWidget(button_save)
