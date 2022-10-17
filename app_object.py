from PySide6.QtCore import QObject

from dcp_sensor_selection import DCPSensorSelection
from dcp_stats_selection import DCPStats
from dcp_step_value_setting import DCPStepValueSetting
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

    def getPanelSensorsModel(self):
        sensors = self.getPanelSensors()
        return sensors.model

    def getPanelSensorsFeatures(self):
        sensors = self.getPanelSensors()
        return sensors.features

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
