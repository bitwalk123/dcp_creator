from PySide6.QtCore import QObject, Qt

from dcp_sensors import DCPSensorSelection
from dcp_stats import DCPStats
from dcp_recipe import DCPStepValueSetting
from dcp_summary import DCPSummary
from recipe import Recipe
from sensors import Sensors
from stats import Stats
from summary import Summary


class AppObject(QObject):
    def __init__(self, page: dict):
        super().__init__()
        self.page = page

    def getPanelSummary(self) -> Summary:
        """
        getPanelSummary
        get summary instance
        """
        page_summary: DCPSummary = self.page['summary']
        summary: Summary = page_summary.getPanel()
        return summary

    def getPanelSensors(self) -> Sensors:
        """
        getPanelSensors
        get sensors instance
        """
        page_sensors: DCPSensorSelection = self.page['sensors']
        sensors: Sensors = page_sensors.getPanel()
        return sensors

    def getPanelRecipe(self) -> Recipe:
        """
        getPanelRecipe
        get recipe instance
        """
        page_recipe: DCPStepValueSetting = self.page['recipe']
        recipe: Recipe = page_recipe.getPanel()
        return recipe

    def getPanelStats(self) -> Stats:
        """
        getPanelRecipe
        get recipe instance
        """
        page_stats: DCPStats = self.page['stats']
        stats: Stats = page_stats.getPanel()
        return stats

    def updateFeatures(self):
        """
        update_features
        """
        # _____________________________________________________________________
        # for Summary page
        summary = self.getPanelSummary()
        # _____________________________________________________________________
        # for Sensor Selection page
        sensors = self.getPanelSensors()
        # _____________________________________________________________________
        # for Summary Stats Selection page
        stats = self.getPanelStats()
        # Sensor Selection Modified
        n_sensor_step_valid = sensors.count_checkbox_checked()
        n_stat_valid = stats.count_checkbox_checked()
        # Features Modified
        summary.setFeaturesModified(n_sensor_step_valid * n_stat_valid)
        summary.setStatModified(n_stat_valid)

    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    # FILTER RELATED ROUTINES
    def getPanelSensorsFeatures(self):
        sensors = self.getPanelSensors()
        return sensors.features

    def getPanelSensorsModel(self):
        sensors = self.getPanelSensors()
        return sensors.model

    def getPanelStatsModel(self):
        stats = self.getPanelStats()
        return stats.model

    def getPanelRecipeSensorWithSetting(self):
        recipe = self.getPanelRecipe()
        return recipe.getSensorWithSetting()

    def getPanelRecipeSensorStepSetting0(self):
        recipe = self.getPanelRecipe()
        return recipe.getSensorStepSetting0()

    def find_header_label(self, key) -> int:
        model = self.getPanelSensorsModel()
        features = self.getPanelSensorsFeatures()
        col = -1
        for i in range(features.getCols()):
            name_head = model.headerData(i, Qt.Horizontal, Qt.DisplayRole)
            if name_head == key:
                col = i
                break
        return col

    def get_sensor_row(self, sensor)-> int:
        features = self.getPanelSensorsFeatures()
        for row in range(features.getRows()):
            if features.getSensors()[row] == sensor:
                return row

    def find_sensor_with_regex(self, pattern):
        features = self.getPanelSensorsFeatures()
        list_row = list()
        for row in range(features.getRows()):
            sensor = features.getSensors()[row]
            result = pattern.match(sensor)
            if result:
                list_row.append(row)
        return list(set(list_row))

    def find_sensor_without_regex(self, pattern):
        features = self.getPanelSensorsFeatures()
        list_row = list()
        for row in range(features.getRows()):
            sensor = features.getSensors()[row]
            result = pattern.match(sensor)
            if not result:
                list_row.append(row)
        return list(set(list_row))

    def get_step_columns(self) -> list:
        model = self.getPanelSensorsModel()
        features = self.getPanelSensorsFeatures()
        list_col = list()
        for col in range(features.getCols()):
            name_head = model.headerData(col, Qt.Horizontal, Qt.DisplayRole)
            if type(name_head) is int:
                list_col.append(col)
        return list_col

    def swicth_check(self, list_row, list_col, flag):
        model = self.getPanelSensorsModel()
        for row in list_row:
            for col in list_col:
                index = model.index(row, col)
                if flag:
                    model.setData(index, Qt.CheckState.Unchecked, role=Qt.CheckStateRole)
                else:
                    model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)

    def switch_check_all_rows(self, col, flag):
        """check/uncheck checkbox in specified columns
        """
        model = self.getPanelSensorsModel()
        features = self.getPanelSensorsFeatures()
        for row in range(features.getRows()):
            index = model.index(row, col)
            if flag:
                model.setData(index, Qt.CheckState.Unchecked, role=Qt.CheckStateRole)
            else:
                model.setData(index, Qt.CheckState.Checked, role=Qt.CheckStateRole)
