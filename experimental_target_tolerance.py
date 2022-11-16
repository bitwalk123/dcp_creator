from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QScrollArea,
    QSizePolicy, QLabel, QWidget, QLineEdit,
)

from app_widgets import VBoxLayout, LabelCell, LabelHead
from features import Features


class TargetTolerance(QScrollArea):
    style_head = 'padding:2px 5px; font-family:monospace; background-color:#eee;'
    style_head2 = 'padding:2px 5px; font-family:monospace; font-size:7pt; background-color:#eee;'
    style_cell = 'padding:2px 5px; font-family:monospace; background-color:#f8fff8;'
    style_cell_disable = 'padding:2px 5px; font-family:monospace;'

    def __init__(self):
        super().__init__()
        self.setFixedHeight(500)
        self.setWidgetResizable(True)
        base = QFrame()
        base.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        self.setWidget(base)
        self.layout = QGridLayout()
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
        for i, step in enumerate(steps):
            col = i + col_start
            lab_step = LabelHead(str(step), self.style_head)
            lab_step.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.layout.addWidget(lab_step, 0, col)

        # row header
        lab_sensor = LabelHead('Sensor', self.style_head)
        self.layout.addWidget(lab_sensor, 0, 0)
        lab_unit = LabelHead('Unit', self.style_head)
        self.layout.addWidget(lab_unit, 0, 1)
        for j, sensor in enumerate(sensors):
            row = j + row_start
            lab_sensor = LabelHead(sensor, self.style_head)
            self.layout.addWidget(lab_sensor, row, 0)
            lab_unit = LabelHead(units[sensor], self.style_head)
            self.layout.addWidget(lab_unit, row, 1)

            fra = QFrame()
            fra.setLineWidth(1)
            fra.setFrameStyle(QFrame.Shape.WinPanel | QFrame.Shadow.Sunken)
            self.layout.addWidget(fra, row, 2)
            layout_target_tolerance = VBoxLayout()
            fra.setLayout(layout_target_tolerance)
            # target
            lab_target = LabelCell('Target', self.style_head2)
            lab_target.setAlignment(Qt.AlignmentFlag.AlignBottom)
            lab_target.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
            layout_target_tolerance.addWidget(lab_target)
            # tolerance
            lab_tolerance = LabelCell('Tolerance', self.style_head2)
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
                    css_style = self.style_cell
                else:
                    flag_enable = False
                    css_style = self.style_cell_disable

                if sensor in list_sensor_setting:
                    if step in dict_sensor_setting_step[sensor].keys():
                        # print(sensor, step, dict_sensor_setting_step[sensor][step])
                        str_value = str(dict_sensor_setting_step[sensor][step])
                    else:
                        # print(sensor, step)
                        str_value = '0.0'
                else:
                    str_value = '0.0'

                fra = QFrame()
                fra.setLineWidth(1)
                fra.setFrameStyle(QFrame.Shape.WinPanel | QFrame.Shadow.Sunken)
                fra.setEnabled(flag_enable)
                self.layout.addWidget(fra, row, col)
                layout_target_tolerance = VBoxLayout()
                fra.setLayout(layout_target_tolerance)
                #
                lab_target = LabelCell(str_value, css_style)
                lab_target.setAlignment(Qt.AlignmentFlag.AlignRight)
                lab_target.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
                layout_target_tolerance.addWidget(lab_target)
                #
                lab_tolerance = LabelCell('0.0', css_style)
                lab_tolerance.setAlignment(Qt.AlignmentFlag.AlignRight)
                lab_tolerance.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
                layout_target_tolerance.addWidget(lab_tolerance)
