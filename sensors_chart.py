import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PySide6.QtWidgets import QMainWindow

from features import Features

class Scatter(FigureCanvas):
    df: pd.DataFrame = None

    def __init__(self, df):
        #tips = sns.load_dataset("tips")
        g = sns.FacetGrid(df, col='step', hue='*chamber')
        g.map(sns.scatterplot, '*start_time', 'value')
        #g = sns.FacetGrid(df, col="time", row="sex")
        #g.map(sns.scatterplot, "total_bill", "tip")
        super().__init__(g.fig)

class SensorChart(QMainWindow):
    def __init__(self, parent, features: Features, row: int):
        super().__init__(parent=parent)
        self.features = features
        sensor = self.init_ui(row)
        self.setWindowTitle(sensor)

    def init_ui(self, row):
        # list_cols = list()
        # list_cols.append(self.features.getSrcDfStart())
        # list_cols.append(self.features.getSrcDfChamberCol())
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
                df_step = self.features.getSrcDf()[list_cols]
                df_step['value'] = self.features.getSrcDf()[features_full]
                df_step['step'] = step
                list_df_step.append(df_step)

        df = pd.concat(list_df_step)
        print(df)

        #fig = plt.figure(dpi=100)
        #ax = fig.add_subplot(111, title=sensor)
        #plt.subplots_adjust(bottom=0.2, left=0.2, right=0.8, top=0.9)
        #ax.grid(True)
        #g = sns.FacetGrid(df, col='step')
        #g.map(sns.scatterplot, '*start_time', 'value')
        #tips = sns.load_dataset('tips')
        #g = sns.FacetGrid(tips, col='time', row='sex')
        #g.map(sns.scatterplot, 'total_bill', 'tip')
        canvas = Scatter(df)
        self.setCentralWidget(canvas)
        return sensor


