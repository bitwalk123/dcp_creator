from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QWidget,
)

from app_widgets import VBoxLayout, LabelHead
from experimental_css_style import ExperimentalCSSStyle


class SensorScaleDlg(QDialog):
    style = ExperimentalCSSStyle()
    col_start = 0
    row_start = 0

    def __init__(self, info: dict):
        super().__init__()
        self.info = info
        self.setWindowTitle(info['sensor'])

        layout = VBoxLayout()
        self.setLayout(layout)

        base = QWidget()
        layout.addWidget(base)
        self.gen_table(base)

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        buttonbox = QDialogButtonBox(buttons)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        layout.addWidget(buttonbox)

    def gen_table(self, base):
        layout = QGridLayout()
        base.setLayout(layout)
        #
        self.col_start = col_start = 2
        self.row_start = row_start = 1
        # column header sensor, unit & scaler
        lab_sensor_head = LabelHead('Sensor', self.style.style_head)
        lab_unit_head = LabelHead('Unit', self.style.style_head)
        layout.addWidget(lab_sensor_head, 0, 0)
        layout.addWidget(lab_unit_head, 0, 1)
        # column header for process step
        for i, step in enumerate(self.info['steps']):
            col = i + col_start
            lab_step_head = LabelHead(str(step), self.style.style_head)
            lab_step_head.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            layout.addWidget(lab_step_head, 0, col)
        # row header
        sensor = self.info['sensor']
        unit = self.info['unit']
        lab_sensor = LabelHead(sensor, self.style.style_head_sensor)
        layout.addWidget(lab_sensor, 1, 0)
        lab_unit = LabelHead(unit, self.style.style_head)
        layout.addWidget(lab_unit, 1, 1)
