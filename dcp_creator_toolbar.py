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
    toolbar class of the main window
    """
    openClicked = Signal()
    saveClicked = Signal()

    def __init__(self):
        super().__init__()
        # _____________________________________________________________________
        # Open button
        button_open = QToolButton()
        button_open.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_open.setIcon(
            QIcon(self.style().standardIcon(QStyle.SP_FileDialogStart))
        )
        button_open.setToolTip('read summary stat data exported from the Fleet Analysis Tool.')
        button_open.clicked.connect(self.openClicked.emit)
        self.addWidget(button_open)
        # Pad
        pad = QWidget()
        pad.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addWidget(pad)
        # _____________________________________________________________________
        # Save button
        button_save = QToolButton()
        button_save.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button_save.setIcon(
            QIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        )
        button_save.setToolTip('save DCP info importing to the Fleet Analysis Tool.')
        button_save.clicked.connect(self.saveClicked.emit)
        self.addWidget(button_save)
