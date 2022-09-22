from PySide6.QtWidgets import QMainWindow, QScrollArea

from features import Features
from summary import Summary


class DCPSummary(QMainWindow):
    summary: Summary = None

    def __init__(self, features: Features):
        super().__init__()
        self.features = features
        self.init_ui()

    def init_ui(self):
        """
        init_ui
        initialize UI
        :param info_log:
        """
        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        self.summary = Summary(self.features)
        central.setWidget(self.summary)

    def getPanel(self) -> Summary:
        return self.summary
