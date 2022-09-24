from PySide6.QtWidgets import (
    QMainWindow,
    QScrollArea,
)

from features import Features


class DCPSummaryStat(QMainWindow):
    def __init__(self, features: Features):
        super().__init__()
        self.init_ui(features)

    def init_ui(self, features: Features):
        """
        init_ui
        initialize UI
        :param info_log:
        """
        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
