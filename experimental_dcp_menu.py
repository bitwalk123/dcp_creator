from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QFrame, QRadioButton

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
        # RadioButton
        radio_mean_stddev = QRadioButton(self.LABEL_MEAN_STDDEV)
        #radio_mean_stddev.setStyleSheet(self.style.style_cell_radio)
        #radio_mean_stddev.toggled.connect(self.radiobutton_changed)
        layout.addWidget(radio_mean_stddev)

        radio_target_tolerance = QRadioButton(self.LABEL_TARGET_TOLERANCE)
        #radio_target_tolerance.setStyleSheet(self.style.style_cell_radio)
        #radio_target_tolerance.toggled.connect(self.radiobutton_changed)
        layout.addWidget(radio_target_tolerance)

        # padding
        pad = Pad()
        layout.addWidget(pad)
        # legend
        label_color = QLabel('Color Legend :')
        layout.addWidget(label_color)
        titles = ['Target/Tolerance', 'Mean/Stddev']
        styles = [style.style_cell_target_tolerance, style.style_cell_mean_sigma]
        for title, style_title in zip(titles, styles):
            lab = QLabel(title)
            lab.setStyleSheet(style_title)
            lab.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
            layout.addWidget(lab)

