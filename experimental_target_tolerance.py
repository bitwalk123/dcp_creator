from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QScrollArea,
    QSizePolicy,
)


class TargetTolerance(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        base = QFrame()
        base.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setWidget(base)
        self.layout = QGridLayout()
        base.setLayout(self.layout)

    def set_dimension(self, dim: list):
        pass
