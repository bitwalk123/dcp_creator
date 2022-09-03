from PySide6.QtWidgets import (
    QDockWidget,
    QSizePolicy,
    QWidget, QPushButton,
)

from app_widgets import (
    VBoxLayout,
    MenuButton,
)
from dcp_matrix import DCPMatrix


class DockFilter(QDockWidget):
    """
    DockFilter
    dock for sensor filtering
    """
    def __init__(self, dcp:DCPMatrix):
        super().__init__('Filter')
        self.dcp = dcp
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)
        # Layout for dock
        layout = VBoxLayout()
        base.setLayout(layout)
        self.init_ui(layout)

    def init_ui(self, layout):
        """
        init_ui
        filtering options
        :param layout:
        """
        but = MenuButton('exclude Step -1')
        but.clicked.connect(self.exclude_step_minus1)
        layout.addWidget(but)
        #
        but = MenuButton('exclude Step >= 1000')
        layout.addWidget(but)
        #
        but = MenuButton('exclude Sensor endswith @')
        layout.addWidget(but)
        #
        but = MenuButton('exclude Step Variation = 0')
        layout.addWidget(but)
        #
        but = MenuButton('exclude OES data')
        layout.addWidget(but)
        #
        but = MenuButton('exclude time dependent sensor')
        layout.addWidget(but)

    def exclude_step_minus1(self):
        but: QPushButton = self.sender()
        self.dcp.excludeStepMinus1(but.isChecked())
