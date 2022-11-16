from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QScrollArea,
    QSizePolicy, QLabel,
)


class TargetTolerance(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(300)
        self.setWidgetResizable(True)
        base = QFrame()
        # base.setFixedHeight(300)
        base.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.setWidget(base)
        self.layout = QGridLayout()
        base.setLayout(self.layout)

    def set_dimension(self, info: dict):
        sensors: list = info['sensors']
        units: dict = info['units']
        steps: list = info['steps']

        col_start = 2
        row_start = 1
        # column header
        for i, step in enumerate(steps):
            col = i + col_start
            lab = QLabel(str(step))
            self.layout.addWidget(lab, 0, col)
        # row header
        for j, sensor in enumerate(sensors):
            row = j + row_start
            lab0 = QLabel(sensor)
            self.layout.addWidget(lab0, row, 0)
            lab1 = QLabel(units[sensor])
            self.layout.addWidget(lab1, row, 1)
        # contents
        for i, step in enumerate(steps):
            col = i + col_start
            for j, sensor in enumerate(sensors):
                row = j + row_start
                lab = QLabel('TEST(%d, %d)' % (row, col))
                self.layout.addWidget(lab, row, col)
