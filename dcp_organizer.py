from dcp_summary import DCPSummary


class DCPOrganizer:
    def __init__(self, page: dict):
        self.page = page

    def init(self):
        # _____________________________________________________________________
        # for Summary page
        page_summary: DCPSummary = self.page['summary']
        summary = page_summary.getPanel()
        # Recipe
        summary.setRecipe()
        # Chamber
        summary.setChambers()
        # Wafer
        summary.setWafers()
        # Features Original
        summary.setFeaturesOriginal()
        # Sensor
        summary.setSensor()
        # Step
        summary.setStep()
        # Stat
        summary.setStat()