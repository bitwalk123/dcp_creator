from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QScrollArea,
    QSizePolicy, )

from app_widgets import (
    ButtonOn2Labels,
    ButtonSensor,
    LabelCell,
    LabelHead,
    VBoxLayout,
)
from custom_scaler import Scale
from experimental_css_style import ExperimentalCSSStyle
from experimental_dcp_table_dialogs import SensorScaleDlg
from features import Features


class DCPTable(QScrollArea):
    info = None
    features = None

    def __init__(self):
        super().__init__()
        self.style = ExperimentalCSSStyle()
        self.setStyleSheet('font-family:monospace;')
        self.setFixedHeight(500)
        self.setWidgetResizable(True)
        base = QFrame()
        base.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Preferred
        )
        self.setWidget(base)
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        base.setLayout(self.layout)

    def gen_table(self, info: dict, features: Features):
        """
        generate DCP table

        Parameters
        ----------
        info: dict
            'sensors': list -> sensors_dcp
            'units':   dict -> units[sensor]
            'steps':   list -> steps_recipe
            'feature': list -> features_selected,

        features: Features
        """
        sensors_dcp: list = info['sensors']
        units: dict = info['units']
        steps_recipe: list = info['steps']
        self.info = info
        self.features = features

        self.col_start = col_start = 3
        self.row_start = row_start = 1
        list_sensor_setting = features.getSensorSetting()
        dict_sensor_setting_step = features.getSensorSettingStep()
        # column header sensor, unit & scaler
        lab_sensor_head = LabelHead('Sensor', self.style.style_head)
        lab_unit_head = LabelHead('Unit', self.style.style_head)
        lab_scale_head = LabelHead('Scaler', self.style.style_head)
        self.layout.addWidget(lab_sensor_head, 0, 0)
        self.layout.addWidget(lab_unit_head, 0, 1)
        self.layout.addWidget(lab_scale_head, 0, 2)
        # column header for process step
        for i, step in enumerate(steps_recipe):
            col = i + col_start
            lab_step_head = LabelHead(str(step), self.style.style_head)
            lab_step_head.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            self.layout.addWidget(lab_step_head, 0, col)
        # row header
        for j, sensor in enumerate(sensors_dcp):
            row = j + row_start
            but_sensor = ButtonSensor(sensor, self.style.style_head_sensor)
            but_sensor.clicked.connect(self.sensor_clicked)
            self.layout.addWidget(but_sensor, row, 0)
            lab_unit = LabelHead(units[sensor], self.style.style_head)
            self.layout.addWidget(lab_unit, row, 1)
            # Target/Mean, Tolernce/Sigma
            fra = QFrame()
            fra.setContentsMargins(0, 0, 0, 0)
            fra.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
            self.layout.addWidget(fra, row, 2)
            layout_target_tolerance = VBoxLayout()
            fra.setLayout(layout_target_tolerance)
            # target
            lab_target = LabelCell('Target', self.style.style_head)
            lab_target.setContentsMargins(0, 0, 0, 0)
            lab_target.setAlignment(Qt.AlignmentFlag.AlignBottom)
            lab_target.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
            layout_target_tolerance.addWidget(lab_target)
            # tolerance
            lab_tolerance = LabelCell('Tolerance', self.style.style_head)
            lab_tolerance.setContentsMargins(0, 0, 0, 0)
            lab_tolerance.setFrameStyle(QFrame.Shape.NoFrame | QFrame.Shadow.Plain)
            lab_tolerance.setAlignment(Qt.AlignmentFlag.AlignBottom)
            layout_target_tolerance.addWidget(lab_tolerance)

        # default scale
        scale_center = Scale.MEAN_SIGMA
        scale_variation = Scale.MEAN_SIGMA

        # contents
        for i, step in enumerate(steps_recipe):
            col = i + col_start
            for j, sensor in enumerate(sensors_dcp):
                row = j + row_start

                feature_partial = '%s%s_%d' % (sensor, units[sensor], steps_recipe[i])
                if len([s for s in info['feature'] if s.startswith(feature_partial)]) > 0:
                    flag_enable = True
                    css_style = self.style.style_cell
                else:
                    flag_enable = False
                    css_style = self.style.style_cell_disable

                if sensor in list_sensor_setting:
                    # The sensor has setting
                    if step in dict_sensor_setting_step[sensor].keys():
                        str_setting_value = str(dict_sensor_setting_step[sensor][step])
                        method_upper = scale_center
                    else:
                        # This step of this sensor is not in DCP
                        str_setting_value = '0.0'
                        method_upper = Scale.NONE
                else:
                    # The sensor has no setting
                    str_setting_value = '0.0'
                    method_upper = scale_center

                str_tolerance_value = '0.0'
                method_lower = scale_variation

                but = ButtonOn2Labels(
                    [str_setting_value, str_tolerance_value],
                    [method_upper, method_lower],
                    css_style,
                    flag_enable,
                )
                self.layout.addWidget(but, row, col)

            self.layout.columnStretch(col)

    def sensor_clicked(self):
        button: ButtonSensor = self.sender()
        name_sensor = button.text()
        features_sensor = [s for s in self.info['feature'] if s.startswith(name_sensor)]
        sensor = list() # dummy
        unit = {}
        steps = list()
        stats = list()
        for feature in features_sensor:
            self.features.sensor_unit_step(feature, sensor, stats, steps, unit)
        steps = sorted(list(set(steps)))
        sensor = sorted(list(set(sensor)))[0]
        stats = sorted(list(set(stats)))

        info_sensor = {
            'sensor': sensor,
            'unit': unit[sensor],
            'steps':steps,
            'stats':stats,
        }
        dlg = SensorScaleDlg(info_sensor, self.features)
        if dlg.exec():
            print('OK')
        else:
            print('Cancel')
