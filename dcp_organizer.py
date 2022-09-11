from dcp_sensor_selection import DCPSensorSelection
from dcp_summary import DCPSummary


class DCPOrganizer:
    def __init__(self, page: dict):
        self.page = page

    def init(self):
        # _____________________________________________________________________
        # for Summary page
        page_summary: DCPSummary = self.page['summary']
        summary = page_summary.getPanel()
        # _____________________________________________________________________
        # for Sensor Selection page
        page_sensors: DCPSensorSelection = self.page['sensors']
        sensors = page_sensors.getPanel()
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

    def update_features(self):
        # _____________________________________________________________________
        # for Summary page
        page_summary: DCPSummary = self.page['summary']
        summary = page_summary.getPanel()
        # _____________________________________________________________________
        # for Sensor Selection page
        page_sensors: DCPSensorSelection = self.page['sensors']
        sensors = page_sensors.getPanel()
        # Sensor Selection Modified
        n_sensor_step_valid = sensors.count_checkbox_checked()
        # Features Modified
        summary.setFeaturesModified(n_sensor_step_valid)
