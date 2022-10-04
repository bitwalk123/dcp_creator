import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
from PySide6.QtWidgets import (
    QMainWindow,
    QScrollArea,
    QSizePolicy, QToolBar, QComboBox, QLabel, QStyle,
)

from features import Features


class SensorStepScatter(FigureCanvas):
    def __init__(self, df):
        #sns.set_theme(style='grid', palette='colorblind', font_scale=0.8)
        print(df)
        mpl.rcParams.update({'font.size': 9})
        facet = sns.FacetGrid(data=df, col='step', height=2, aspect=0.6)
        facet.map_dataframe(sns.scatterplot, x='*start_time', y='value', hue='*chamber')
        facet.set(xticklabels=[])
        #facet.set(xlabel=None)
        facet.tight_layout()
        self.fig: Figure = facet.figure
        super().__init__(self.fig)


class SensorChart(QMainWindow):
    canvas: SensorStepScatter = None

    def __init__(self, parent, features: Features, row: int):
        super().__init__(parent=parent)
        self.features = features
        sensor, unit = self.init_ui(row)
        self.setWindowTitle('%s%s'%(sensor, unit))
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        )
        self.resize(1000, 200)

    def init_ui(self, row):
        # _____________________________________________________________________
        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        label_stat = QLabel('Summary Statistics')
        label_stat.setStyleSheet('margin:0 1em 0 0;')
        toolbar.addWidget(label_stat)
        combo_stat = QComboBox()
        toolbar.addWidget(combo_stat)
        # _____________________________________________________________________
        # Central Widget
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        base = QMainWindow()
        base.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        central.setWidget(base)

        sensor = self.features.getSensors()[row]
        unit = self.features.getUnits()[sensor]
        stats = self.features.getStats()
        if 'Avg' in stats:
            stat = 'Avg'
        else:
            stat = stats[0]
        combo_stat.addItems(stats)
        combo_stat.setCurrentText(stat)
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
                print(df_step)
                list_df_step.append(df_step)

        df = pd.concat(list_df_step)
        self.canvas = SensorStepScatter(df)
        base.setCentralWidget(self.canvas)

        return sensor, unit

    def closeEvent(self, event):
        plt.close(self.canvas.fig)
        event.accept()
