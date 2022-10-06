import json

from app_object import AppObject
from util_filter import UtilFilter


class UIController(AppObject):
    """UI controler, especially for cross-tab management
    """

    def __init__(self, page: dict):
        super().__init__(page)
        # filters
        self.filter_utility = UtilFilter(page)
        # _____________________________________________________________________
        # for Summary page
        summary = self.getPanelSummary()
        # _____________________________________________________________________
        # for Sensor Selection page
        sensors = self.getPanelSensors()
        # _____________________________________________________________________
        # for Summary Stats Selection page
        stats = self.getPanelStats()
        # _____________________________________________________________________
        # Sensor Selection Modified
        n_sensor_step_valid = sensors.count_checkbox_checked()
        n_stat_valid = stats.count_checkbox_checked()
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
        summary.setFeaturesModified(n_sensor_step_valid * n_stat_valid)
        # Sensor Selection
        summary.setSensor()
        # Step
        summary.setStep()
        # Stat
        summary.setStat()
        summary.setStatModified(n_stat_valid)

    def saveJSON4DCP(self, filename: str):
        """
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        save JSON file for DCP
        _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        """
        dict_dcp = {}
        # SENSOR/STEP
        sensors = self.getPanelSensors()
        dict_dcp['sensor_steps'] = sensors.getDCP()
        # STAT
        stats = self.getPanelStats()
        dict_dcp['statistics'] =  stats.getDCP()
        # _____________________________________________________________________
        # OUTPUT
        with open(filename, 'w') as f:
            json.dump(dict_dcp, f, indent=4)
        # for debug
        print(json.dumps(dict_dcp, indent=4))

