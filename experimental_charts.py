import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import seaborn as sns


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# ### MEMO ###
# how to delete chart object created by matplotlib
# Reference:
# https://www.tutorialspoint.com/how-to-clear-the-memory-completely-of-all-matplotlib-plots
# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# fig = plt.figure()
# plt.figure().clear()
# plt.close()
# plt.cla()
# plt.clf()

class Scatter(FigureCanvas):
    fig = Figure()

    def __init__(self, df: pd.DataFrame, x: str, y: str, hue: str):
        super().__init__(self.fig)
        self.df = df
        self.x = x
        self.y = y
        self.hue = hue
        # Seaborn Scatter
        ax = self.fig.add_subplot(111)
        sns.scatterplot(
            data=self.df,
            x=self.df[self.x],
            y=self.df[self.y],
            hue=self.df[self.hue],
            ax=ax,
        )
        ax.set_aspect('equal', 'box')
        ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, fontsize=8)

    def delete(self):
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
