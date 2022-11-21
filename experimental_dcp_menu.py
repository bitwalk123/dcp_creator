from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QFrame

from app_widgets import Pad
from experimental_css_style import ExperimentalCSSStyle


class ExperimentalDCPMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        style = ExperimentalCSSStyle()
        layout = QHBoxLayout()
        self.setLayout(layout)
        # padding
        pad = Pad()
        layout.addWidget(pad)
        # legend
        lab_color = QLabel('Color Legend :')
        layout.addWidget(lab_color)
        titles = ['Target/Tolerance', 'Mean/Stddev']
        styles = [style.style_cell_target_tolerance, style.style_cell_mean_sigma]
        for title, style_title in zip(titles, styles):
            lab = QLabel(title)
            lab.setStyleSheet(style_title)
            lab.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
            layout.addWidget(lab)

