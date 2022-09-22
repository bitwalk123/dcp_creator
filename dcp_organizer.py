import json
from dcp_sensor_selection import DCPSensorSelection
from dcp_step_value_setting import DCPStepValueSetting
from dcp_summary import DCPSummary
from recipe import Recipe
from sensors import Sensors
from summary import Summary


class DCPOrganizer:
    def __init__(self, page: dict):
        self.page = page

    def init(self):
        # _____________________________________________________________________
        # for Summary page
        summary = self.getPanelSummary()
        # _____________________________________________________________________
        # for Sensor Selection page
        sensors = self.getPanelSensors()
        # Sensor Selection Modified
        n_sensor_step_valid = sensors.count_checkbox_checked()
        # _____________________________________________________________________
        # for Summary page (update)
        # Recipe
        summary.setRecipe()
        # Chamber
        summary.setChambers()
        # Wafer
        summary.setWafers()
        # Features Original
        summary.setFeaturesOriginal()
        # Features Modified
        summary.setFeaturesModified(n_sensor_step_valid)
        # Sensor Selection
        summary.setSensor()
        # Step
        summary.setStep()
        # Stat
        summary.setStat()

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

    def update_features(self):
        """
        update_features
        """
        # _____________________________________________________________________
        # for Summary page
        summary = self.getPanelSummary()
        # _____________________________________________________________________
        # for Sensor Selection page
        sensors = self.getPanelSensors()
        # Sensor Selection Modified
        n_sensor_step_valid = sensors.count_checkbox_checked()
        # Features Modified
        summary.setFeaturesModified(n_sensor_step_valid)

    def saveDCP(self, filename:str):
        """
        saveDCP
        save current DCP
        """
        sensors = self.getPanelSensors()
        # get sensor/step & statistics selected
        dict_dcp: dict = sensors.getDCP()
        with open(filename, 'w') as f:
            json.dump(dict_dcp, f, indent=4)
