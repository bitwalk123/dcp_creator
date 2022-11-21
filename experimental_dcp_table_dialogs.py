from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout, QRadioButton, QButtonGroup, QLineEdit, QFrame,
)

from app_widgets import VBoxLayout, LabelHead, LabelCell, LabelTitle
from experimental_css_style import ExperimentalCSSStyle
from features import Features


class SensorScaleDlg(QDialog):
    style = ExperimentalCSSStyle()
    col_start = 0
    row_start = 0

    LABEL_MEAN_STDDEV = 'Mean / Stddev'
    LABEL_TARGET_TOLERANCE = 'Target / Tolerance'
    label_target_cell = None
    entry_tolerance_cell = None

    def __init__(self, info: dict, features: Features):
        super().__init__()
        self.info = info
        self.features = features
        self.setWindowTitle(info['sensor'])
        self.setContentsMargins(2, 2, 2, 2)

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
        option = QFrame()
        option.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        option.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        option.setLineWidth(2)
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
        label_sensor_head = LabelHead('Sensor', self.style.style_head)
        layout.addWidget(label_sensor_head, 0, 0)

        label_unit_head = LabelHead('Unit', self.style.style_head)
        layout.addWidget(label_unit_head, 0, 1)
        # column header for process step
        for i, step in enumerate(self.info['steps']):
            col = i + col_start
            label_step_head = LabelHead(str(step), self.style.style_head)
            label_step_head.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(label_step_head, 0, col)
        # row header
        sensor = self.info['sensor']
        unit = self.info['unit']

        label_sensor = LabelCell(sensor, self.style.style_cell_label)
        layout.addWidget(label_sensor, 1, 0)

        label_unit = LabelCell(unit, self.style.style_cell_label)
        layout.addWidget(label_unit, 1, 1)

        label_setting = LabelCell('Setting', self.style.style_cell_label)
        layout.addWidget(label_setting, 1, 2)

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

            label_cell = LabelCell(str_setting_value, self.style.style_cell_label)
            label_cell.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(label_cell, 1, col)

    def gen_option(self, base):
        layout = QGridLayout()
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(2)
        base.setLayout(layout)
        #
        radio_mean_stddev = QRadioButton(self.LABEL_MEAN_STDDEV)
        radio_mean_stddev.setStyleSheet(self.style.style_cell_radio)
        radio_mean_stddev.toggled.connect(self.radiobutton_changed)
        layout.addWidget(radio_mean_stddev, 0, 0)

        radio_target_tolerance = QRadioButton(self.LABEL_TARGET_TOLERANCE)
        radio_target_tolerance.setStyleSheet(self.style.style_cell_radio)
        radio_target_tolerance.toggled.connect(self.radiobutton_changed)
        layout.addWidget(radio_target_tolerance, 1, 0)

        label_target = LabelHead('Target', self.style.style_head)
        layout.addWidget(label_target, 1, 1)

        self.label_target_cell = label_target_cell = LabelCell('Setting', self.style.style_cell_label)
        layout.addWidget(label_target_cell, 1, 2)

        label_tolerance = LabelHead('Tolerance', self.style.style_head)
        layout.addWidget(label_tolerance, 1, 3)

        self.entry_tolerance_cell = entry_tolerance_cell = EntryTolerance(self.style.style_cell_entry)
        """
        self.entry_tolerance_cell = entry_tolerance_cell = QLineEdit()
        entry_tolerance_cell.setStyleSheet(self.style.style_cell_entry)
        entry_tolerance_cell.setAlignment(Qt.AlignmentFlag.AlignRight)
        validator = QDoubleValidator()
        validator.setBottom(0.0)  # only positive value is accepted for tolerance
        entry_tolerance_cell.setValidator(validator)
        """
        layout.addWidget(entry_tolerance_cell, 1, 4)

        radio_group = QButtonGroup()
        radio_group.addButton(radio_mean_stddev)
        radio_group.addButton(radio_target_tolerance)

        radio_mean_stddev.setChecked(True)

    def radiobutton_changed(self):
        rb: QRadioButton = self.sender()
        if rb.isChecked():
            if rb.text() == self.LABEL_MEAN_STDDEV:
                self.label_target_cell.setEnabled(False)
                self.entry_tolerance_cell.setEnabled(False)
            else:
                self.label_target_cell.setEnabled(True)
                self.entry_tolerance_cell.setEnabled(True)


class EntryTolerance(QLineEdit):
    def __init__(self, css_style:str):
        super().__init__()
        self.setStyleSheet(css_style)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        validator = QDoubleValidator()
        validator.setBottom(0.0)  # only positive value is accepted for tolerance
        self.setValidator(validator)
