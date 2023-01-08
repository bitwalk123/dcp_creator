import pandas as pd
import sys

from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QStyle, )

from modules.read_csv import ReadCSV


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sample for ReadCSV')
        self.init_ui()

    def init_ui(self):
        menu_file = self.menuBar().addMenu('&File')
        action_open = QAction(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton),
            'Open',
            self
        )
        action_open.triggered.connect(self.readfile_selection)
        menu_file.addAction(action_open)

    def readfile_selection(self):
        selection = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select CSV file',
            filter='Zip File (*.zip);; CSV File (*.csv)'
        )
        csvfile = selection[0]
        print(csvfile)
        obj = ReadCSV()
        obj.readCompleted.connect(self.show_df)
        obj.read(csvfile)

    def show_df(self, df: pd.DataFrame):
        print(df)


def main():
    """Main Event Loop
    """
    app: QApplication = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
