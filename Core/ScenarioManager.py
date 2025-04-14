from Core.ScreenshootService import ScreenshotService

class ScenarioManager:
    def __init__(self):
        self.oScreenshotService = ScreenshotService()
        self.oDescriptionService = None  # You can inject or assign this later

    def startRecordingScenario(self):
        self.oScreenshotService.startListener()

    def stopRecordingScenario(self):
        self.oScreenshotService.stopListener()



    def generateFullScenario(self):
        # Logic to combine screenshots + descriptions + save to Excel
        pass
