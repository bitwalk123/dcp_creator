from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QFrame, QRadioButton, QButtonGroup, QComboBox

from app_widgets import Pad
from experimental_css_style import ExperimentalCSSStyle


class ExperimentalDCPMenu(QWidget):
    LABEL_MEAN_STDDEV = 'Mean / Stddev'
    LABEL_TARGET_TOLERANCE = 'Target / Tolerance'

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        style = ExperimentalCSSStyle()
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Summary Statistics Selection
        label_summary_statistics = QLabel('Summary Stat.')
        layout.addWidget(label_summary_statistics)
        combo_summary_statistics = QComboBox()
        layout.addWidget(combo_summary_statistics)

        # RadioButton to switch Mean/Stddev and Target/Tolerance
        radio_mean_stddev = QRadioButton(self.LABEL_MEAN_STDDEV)
        #radio_mean_stddev.toggled.connect(self.radiobutton_changed)
        layout.addWidget(radio_mean_stddev)

        radio_target_tolerance = QRadioButton(self.LABEL_TARGET_TOLERANCE)
        # radio_target_tolerance.toggled.connect(self.radiobutton_changed)
        layout.addWidget(radio_target_tolerance)

        radio_group = QButtonGroup()
        radio_group.addButton(radio_mean_stddev)
        radio_group.addButton(radio_target_tolerance)

        radio_mean_stddev.setChecked(True)

        # padding
        pad = Pad()
        layout.addWidget(pad)
        # legend
        label_color = QLabel('Color Legend :')
        layout.addWidget(label_color)
        titles = ['Mean/Stddev', 'Target/Tolerance']
        styles = [style.style_cell_mean_sigma, style.style_cell_target_tolerance]
        for title, style_title in zip(titles, styles):
            lab = QLabel(title)
            lab.setStyleSheet(style_title)
            lab.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
            layout.addWidget(lab)
