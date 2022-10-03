import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QScrollArea,
    QSizePolicy,
    QWidget,
)

from features import Features


class SensorStepScatter(FigureCanvas):
    def __init__(self, df):
        facet = sns.FacetGrid(df, col='step')
        facet.map_dataframe(sns.scatterplot, x='*start_time', y='value', hue='*chamber')
        self.fig: Figure = facet.fig
        super().__init__(self.fig)


class SensorChart(QMainWindow):
    canvas: SensorStepScatter = None

    def __init__(self, parent, features: Features, row: int):
        super().__init__(parent=parent)
        self.features = features
        sensor = self.init_ui(row)
        self.setWindowTitle(sensor)
        self.resize(1000, 320)

    def init_ui(self, row):
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        base = QWidget()
        base.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        central.setWidget(base)
        layout = QHBoxLayout()
        base.setLayout(layout)

        sensor = self.features.getSensors()[row]
        unit = self.features.getUnits()[sensor]
        stats = self.features.getStats()
        stat = stats[0]
        #
        list_df_step = list()
        steps = self.features.getSteps()
        for step in steps:
            features_full = '%s%s_%s_%s' % (sensor, unit, step, stat)
            if features_full in self.features.getSrcDfColumns():
                list_cols = [self.features.getSrcDfStart(),
                             self.features.getSrcDfChamberCol()]
                df_step = self.features.getSrcDf()[list_cols].copy()
                df_step['value'] = self.features.getSrcDf()[features_full].copy()
                df_step['step'] = step
                list_df_step.append(df_step)

        df = pd.concat(list_df_step)
        self.canvas = SensorStepScatter(df)
        layout.addWidget(self.canvas)

        return sensor

    def closeEvent(self, event):
        plt.close(self.canvas.fig)
        event.accept()
