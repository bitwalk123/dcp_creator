from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QScrollArea,
    QSizePolicy,
)

from app_widgets import VBoxLayout, LabelCell, LabelHead, ButtonOn2Labels, ButtonSensor
from experimental_css_style import ExperimentalCSSStyle
from features import Features


class TargetTolerance(QScrollArea):
    def __init__(self):
        super().__init__()
        self.style = ExperimentalCSSStyle()
        self.setStyleSheet('font-family:monospace;')
        self.setFixedHeight(500)
        self.setWidgetResizable(True)
        base = QFrame()
        base.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.setWidget(base)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        base.setLayout(self.layout)

    def gen_table(self, info: dict, features: Features):
        sensors: list = info['sensors']
        units: dict = info['units']
        steps: list = info['steps']

        col_start = 3
        row_start = 1
        list_sensor_setting = features.getSensorSetting()
        dict_sensor_setting_step = features.getSensorSettingStep()
        # column header
        lab_sensor_head = LabelHead('Sensor', self.style.style_head)
        self.layout.addWidget(lab_sensor_head, 0, 0)
        lab_unit_head = LabelHead('Unit', self.style.style_head)
        self.layout.addWidget(lab_unit_head, 0, 1)
        lab_scale_head = LabelHead('Scaler', self.style.style_head)
        self.layout.addWidget(lab_scale_head, 0, 2)
        for i, step in enumerate(steps):
            col = i + col_start
            lab_step_head = LabelHead(str(step), self.style.style_head)
            lab_step_head.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.layout.addWidget(lab_step_head, 0, col)
        # row header
        for j, sensor in enumerate(sensors):
            row = j + row_start
            but_sensor = ButtonSensor(sensor, self.style.style_head_sensor)
            self.layout.addWidget(but_sensor, row, 0)
            lab_unit = LabelHead(units[sensor], self.style.style_head)
            self.layout.addWidget(lab_unit, row, 1)

            fra = QFrame()
            fra.setContentsMargins(0, 0, 0, 0)
            fra.setLineWidth(1)
            fra.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
            self.layout.addWidget(fra, row, 2)
            layout_target_tolerance = VBoxLayout()
            fra.setLayout(layout_target_tolerance)
            # target
            lab_target = LabelCell('Target/Mean', self.style.style_head)
            lab_target.setContentsMargins(0, 0, 0, 0)
            lab_target.setAlignment(Qt.AlignmentFlag.AlignBottom)
            lab_target.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
            layout_target_tolerance.addWidget(lab_target)
            # tolerance
            lab_tolerance = LabelCell('Tolerance/Sigma', self.style.style_head)
            lab_tolerance.setContentsMargins(0, 0, 0, 0)
            lab_tolerance.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
            lab_tolerance.setAlignment(Qt.AlignmentFlag.AlignBottom)
            layout_target_tolerance.addWidget(lab_tolerance)

        # contents
        for i, step in enumerate(steps):
            col = i + col_start
            for j, sensor in enumerate(sensors):
                row = j + row_start

                part_feature = '%s%s_%d' % (sensor, units[sensor], steps[i])
                if len([s for s in info['feature'] if s.startswith(part_feature)]) > 0:
                    flag_enable = True
                    css_style = self.style.style_cell
                else:
                    flag_enable = False
                    css_style = self.style.style_cell_disable

                if sensor in list_sensor_setting:
                    if step in dict_sensor_setting_step[sensor].keys():
                        css_style_upper = self.style.style_cell_target_tolerance
                        str_setting_value = str(dict_sensor_setting_step[sensor][step])
                    else:
                        str_setting_value = '0.0'
                        css_style_upper = self.style.style_cell_none
                else:
                    str_setting_value = '0.0'
                    css_style_upper = self.style.style_cell_mean_sigma

                str_tolerance_value = '0.0'

                css_style_lower = self.style.style_cell_mean_sigma
                but = ButtonOn2Labels(
                    [str_setting_value, str_tolerance_value],
                    [css_style, css_style_upper, css_style_lower],
                    flag_enable,
                )
                self.layout.addWidget(but, row, col)

            self.layout.columnStretch(col)
