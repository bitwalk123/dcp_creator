from PySide6.QtWidgets import QSizePolicy

from app_widgets import (
    ComboBox,
    FeatureMatrix,
    GridLayout,
    LabelHead,
    LabelNumeric, Pad,
)
from features import Features


class Summary(FeatureMatrix):
    style_cell = 'padding:2px 5px;'

    # Recipe
    combo_recipe: ComboBox = None
    # Chamber
    lab_chamber: LabelNumeric = None
    combo_chamber: ComboBox = None
    # Wafers
    lab_wafer: LabelNumeric = None
    # Feature
    lab_feature_original: LabelNumeric = None
    lab_feature_modified: LabelNumeric = None
    # Sensor
    lab_sensor: LabelNumeric = None
    # Step
    lab_step: LabelNumeric = None
    # Stat
    lab_stat_original: LabelNumeric = None
    lab_stat_moified: LabelNumeric = None

    def __init__(self, features: Features):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # source
        self.features = features
        #
        self.init_ui()

    def init_ui(self):
        """
        init_ui
        initialize UI
        """
        layout = GridLayout()
        self.setLayout(layout)
        #
        row = 0
        lab = LabelHead('Recipe', self.style_cell)
        layout.addWidget(lab, row, 0)
        self.combo_recipe = ComboBox()
        layout.addWidget(self.combo_recipe, row, 1, 1, 3)
        #
        row += 1
        lab = LabelHead('Chamber', self.style_cell)
        layout.addWidget(lab, row, 0)
        self.lab_chamber = LabelNumeric(0, self.style_cell)
        layout.addWidget(self.lab_chamber, row, 1)
        #
        row += 1
        lab = LabelHead('Wafer', self.style_cell)
        layout.addWidget(lab, row, 0)
        self.lab_wafer = LabelNumeric(0, self.style_cell)
        layout.addWidget(self.lab_wafer, row, 1)
        #
        row += 1
        lab = LabelHead('Original', self.style_cell)
        layout.addWidget(lab, row, 1)
        lab = LabelHead('Modified', self.style_cell)
        layout.addWidget(lab, row, 2)
        pad = Pad()
        layout.addWidget(pad, row, 3)
        #
        row += 1
        lab = LabelHead('Feature', self.style_cell)
        layout.addWidget(lab, row, 0)
        self.lab_feature_original = LabelNumeric(0, self.style_cell)
        layout.addWidget(self.lab_feature_original, row, 1)
        self.lab_feature_modified = LabelNumeric(0, self.style_cell)
        layout.addWidget(self.lab_feature_modified, row, 2)
        #
        row += 1
        lab = LabelHead('Sensor', self.style_cell)
        layout.addWidget(lab, row, 0)
        self.lab_sensor = LabelNumeric(0, self.style_cell)
        layout.addWidget(self.lab_sensor, row, 1)
        #
        row += 1
        lab = LabelHead('Step', self.style_cell)
        layout.addWidget(lab, row, 0)
        self.lab_step = LabelNumeric(0, self.style_cell)
        layout.addWidget(self.lab_step, row, 1)
        #
        row += 1
        lab = LabelHead('Statistics', self.style_cell)
        layout.addWidget(lab, row, 0)
        self.lab_stat_original = LabelNumeric(0, self.style_cell)
        layout.addWidget(self.lab_stat_original, row, 1)
        self.lab_stat_modified = LabelNumeric(0, self.style_cell)
        layout.addWidget(self.lab_stat_modified, row, 2)

    def setRecipe(self):
        list_recipe = self.features.getRecipe()
        if len(list_recipe) > 0:
            self.combo_recipe.addItems(list_recipe)

    def setChambers(self):
        list_chamber = self.features.getChambers()
        if len(list_chamber) > 0:
            self.lab_chamber.setValue(len(list_chamber))
            # for debug purpose
            self.logMessage.emit('Chambers:')
            for chamber in list_chamber:
                self.logMessage.emit(chamber)

    def setWafers(self):
        self.lab_wafer.setValue(self.features.getWafers())

    def setFeaturesOriginal(self):
        self.lab_feature_original.setValue(self.features.getFeaturesOriginal())

    def setFeaturesModified(self, n_feature_valid:int):
        """
        setFeaturesModified
        :param sensor_step:
        :return:
        """
        self.lab_feature_modified.setValue(n_feature_valid)

    def setSensor(self):
        list_sensor = self.features.getSensors()
        self.lab_sensor.setValue(len(list_sensor))

    def setStep(self):
        list_step = self.features.getSteps()
        steps = len(list_step)
        if -1 in list_step:
            steps -= 1
        self.lab_step.setValue(steps)

    def setStat(self):
        list_stat = self.features.getStats()
        n_stat = len(list_stat)
        self.lab_stat_original.setValue(n_stat)

    def setStatModified(self, n_stat_valid:int):
        self.lab_stat_modified.setValue(n_stat_valid)
