from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QDockWidget,
    QSizePolicy,
    QWidget,
)

from app_widgets import (
    VBoxLayout,
)


class DCPSensorSelectionDock(QDockWidget):
    """Dock for sensor filtering
    """
    def __init__(self):
        super().__init__('Filter')
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWidget(base)
        # Layout for the dock
        self.layout = VBoxLayout()
        base.setLayout(self.layout)

    def getLayout(self):
        return self.layout