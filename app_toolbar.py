import os

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
    dcpHelpClicked = Signal()
    dcpReadClicked = Signal()
    dcpSaveClicked = Signal()
    optionButtonClicked = Signal()

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
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
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
        button_option.setStyleSheet('margin:0;')
        button_option.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_option.setIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        )
        button_option.setToolTip('Various options and utilities.')
        button_option.clicked.connect(self.optionButtonClicked.emit)
        self.addWidget(button_option)
        self.addSeparator()
        # _____________________________________________________________________
        # Help button
        button_help = QToolButton()
        button_help.setStyleSheet('margin:0 1em;')
        button_help.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_help.setIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion))
        )
        button_help.setToolTip('Help Document.')
        button_help.clicked.connect(self.dcpHelpClicked.emit)
        self.addWidget(button_help)
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


class ExperimentalToolBar(QToolBar):
    performUpdateClicked = Signal()

    imgdir = 'image'

    def __init__(self):
        super().__init__()
        # _____________________________________________________________________
        # PCA button
        button_pca = QToolButton()
        button_pca.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_pca.setIcon(QIcon(os.path.join(self.imgdir, 'update.png')))
        button_pca.setToolTip('perform PCA')
        button_pca.clicked.connect(self.performUpdateClicked.emit)
        self.addWidget(button_pca)
