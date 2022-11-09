import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea

from app_functions import convert_dcp_dict2colname
from app_toolbar import ExperimentalToolBar
from base.tab_window import TabWindow
from experimental import Experimental
from features import Features
from ui_controller import UIController


class DCPExperimental(TabWindow):
    """
    Experimental Window/Panel/Tab
    """
    experimental = None
    col_chamber = 'Tool/Chamber'
    # for PCA
    df = None

    def __init__(self, features: Features, controller: UIController):
        super().__init__()
        self.features = features
        self.controller = controller
        self.init_ui()

    def button_perform_pca_clicked(self):
        """Handling when PCA button clicked
        """
        self.prep_df_from_dcp()
        self.update_experimental()

    def init_ui(self):
        """Initialize UI
        """
        toolbar = ExperimentalToolBar()
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        # PCA
        toolbar.performPCAClicked.connect(self.button_perform_pca_clicked)

        # Scroll Area for Central
        central = QScrollArea()
        central.setWidgetResizable(True)
        self.setCentralWidget(central)
        self.experimental = Experimental()
        self.experimental.logMessage.connect(self.showLog)
        central.setWidget(self.experimental)


    def prep_df_from_dcp(self):
        """Based on DCP, prepare Dataframe from source data currently loaded to this application.
        """
        # Current DCP
        dict_dcp = self.controller.getDictDCP()
        # Convert real column name of the dataframe
        colname_dcp = convert_dcp_dict2colname(dict_dcp)
        # Dataframe for PCA
        df: pd.DataFrame = self.features.df_source[colname_dcp]
        df.insert(0, self.col_chamber, self.features.df_source[self.features.src_chamber])
        self.df = df
    def update_experimental(self):
        self.experimental.update_ui(self.df)