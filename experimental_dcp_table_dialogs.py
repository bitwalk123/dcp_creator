from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout, QRadioButton, QButtonGroup,
)

from app_widgets import VBoxLayout, LabelHead, LabelCell, LabelTitle
from experimental_css_style import ExperimentalCSSStyle
from features import Features


class SensorScaleDlg(QDialog):
    style = ExperimentalCSSStyle()
    col_start = 0
    row_start = 0

    def __init__(self, info: dict, features: Features):
        super().__init__()
        self.info = info
        self.features = features
        self.setWindowTitle(info['sensor'])

        layout = VBoxLayout()
        self.setLayout(layout)

        # Title
        title_sensor = LabelTitle('Scaler for each Sensor in DCP')
        layout.addWidget(title_sensor)

        # Setting Table
        table = QWidget()
        table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(table)
        self.gen_table(table)

        # Option
        option = QWidget()
        layout.addWidget(option)
        self.gen_option(option)

        # ButtonBox
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        buttonbox = QDialogButtonBox(buttons)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        layout.addWidget(buttonbox)

    def gen_table(self, base):
        layout = QGridLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(1)
        base.setLayout(layout)
        #
        self.col_start = col_start = 3
        self.row_start = row_start = 1
        # column header sensor, unit & scaler
        lab_sensor_head = LabelHead('Sensor', self.style.style_head)
        layout.addWidget(lab_sensor_head, 0, 0)
        lab_unit_head = LabelHead('Unit', self.style.style_head)
        layout.addWidget(lab_unit_head, 0, 1)
        # column header for process step
        for i, step in enumerate(self.info['steps']):
            col = i + col_start
            lab_step_head = LabelHead(str(step), self.style.style_head)
            lab_step_head.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(lab_step_head, 0, col)
        # row header
        sensor = self.info['sensor']
        unit = self.info['unit']
        lab_sensor = LabelHead(sensor, self.style.style_head_sensor)
        layout.addWidget(lab_sensor, 1, 0)
        lab_unit = LabelHead(unit, self.style.style_head)
        layout.addWidget(lab_unit, 1, 1)
        lab_setting = LabelHead('Setting', self.style.style_head)
        layout.addWidget(lab_setting, 1, 2)

        list_sensor_setting = self.features.getSensorSetting()
        dict_sensor_setting_step = self.features.getSensorSettingStep()

        for i, step in enumerate(self.info['steps']):
            col = i + col_start
            if sensor in list_sensor_setting:
                # The sensor has setting
                if step in dict_sensor_setting_step[sensor].keys():
                    str_setting_value = str(dict_sensor_setting_step[sensor][step])
                else:
                    # This step of this sensor is not in DCP
                    str_setting_value = 'error'
            else:
                # The sensor has no setting
                str_setting_value = '---'

            lab_cell = LabelCell(str_setting_value, self.style.style_cell_2)
            lab_cell.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(lab_cell, 1, col)

    def gen_option(self, base):
        layout = QGridLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(1)
        base.setLayout(layout)
        #
        rb_A = QRadioButton('Mean / Stddev')
        # rad_A.toggle()
        #rb_A.toggled.connect(self.checkboxChanged)
        layout.addWidget(rb_A, 0, 0)

        rb_B = QRadioButton('Target / Tolerance')
        #rb_B.toggled.connect(self.checkboxChanged)
        layout.addWidget(rb_B, 1, 0)
        lab_target = LabelHead('Target', self.style.style_head)
        layout.addWidget(lab_target, 1, 1)
        lab_target_cell = LabelCell('Setting', self.style.style_cell_2)
        layout.addWidget(lab_target_cell, 1, 2)
        lab_tolerance = LabelHead('Tolerance', self.style.style_head)
        layout.addWidget(lab_tolerance, 1, 3)
        lab_tolerance_cell = LabelCell('---', self.style.style_cell_2)
        layout.addWidget(lab_tolerance_cell, 1, 4)

        rb_group = QButtonGroup()
        rb_group.addButton(rb_A)
        rb_group.addButton(rb_B)
