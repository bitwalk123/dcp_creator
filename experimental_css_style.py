class ExperimentalCSSStyle:
    # CSS Style Sheet
    style_head = 'padding:2px 5px; font-family:monospace; background-color:#eee;'
    style_head2 = 'padding:2px 5px; font-family:monospace; font-size:7pt; background-color:#eee;'
    style_head_sensor = """
    QPushButton {
        padding:2px 5px;
        font-family:monospace;
        background-color:#eee;
        text-align:left;
    }
    QPushButton:hover {
        background-color:#fff;
    }
    QPushButton:pressed {
        background-color:#ddd;
    }
    """
    style_cell = """
    QPushButton {
        font-family:monospace;
        background-color:#ded;
    }
    QPushButton:hover {
        background-color:#efe;
    }
    QPushButton:pressed {
        background-color:#bcb;
    }
    """
    style_cell_target_tolerance = """
    QLabel {
        padding:2px 5px;
        font-family:monospace;
        background-color:#eef;
    }
    """
    style_cell_mean_sigma = """
    QLabel {
        padding:2px 5px;
        font-family:monospace;
        background-color:#fee;
    }
    """
    style_cell_none = """
    QLabel {
        padding:2px 5px;
        font-family:monospace;
    }
    """
    style_cell_disable = """
    QPushButton {
        font-family:monospace;
    }
    """
    def getStyle(self, name):
        return getattr(self, name)
