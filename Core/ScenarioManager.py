import os
from Core.Screenshot.ScreenshotService import ScreenshotService
from Core.Description.DescriptionService import DescriptionService
from Core.ScenarioRecorder import ScenarioRecorder
from Core.Excel.ExcelGenerator import ExcelGenerator
import Utils.Config

class ScenarioManager:
    def __init__(self):
        self.oRecorder = None
        self.oScreenshotService = None
        self.oDescriptionService = None

    def startRecordingScenario(self, sFileName: str):
        sFullPath = os.path.join(Utils.Config.SCENARIO_DIR, sFileName)

        if os.path.exists(sFullPath):
            print(f"⚠ File already exists: {sFullPath}")
            print("❌ Recording aborted to avoid overwriting existing scenario.")
            return

        self.oRecorder = ScenarioRecorder(sPath=sFullPath)
        self.oScreenshotService = ScreenshotService()
        self.oScreenshotService.recorder = self.oRecorder
        self.oScreenshotService.startListener()
        print(f"▶ Started recording scenario to: {sFullPath}")

    def stopRecordingScenario(self):
        if self.oScreenshotService:
            self.oScreenshotService.stopListener()
            print("⏹ Scenario recording stopped.")

    def updateDecriptions(self, sFileName: str):
        sFullPath = os.path.join(Utils.Config.SCENARIO_DIR, sFileName)
        if not os.path.exists(sFullPath):
            print(f"❌ Scenario file does not exist: {sFullPath}")
            return

        self.oRecorder = ScenarioRecorder(sPath=sFullPath)
        self.oDescriptionService = DescriptionService(self.oRecorder)
        self.oDescriptionService.generateDescriptions()
        print(f"✅ Descriptions generated for: {sFullPath}")

    def exportToExcel(self, sFileName: str, sExcelName: str = None):
        sJsonPath = os.path.join(Utils.Config.SCENARIO_DIR, sFileName)
        sTemplatePath = Utils.Config.TEMPLATE_PATH

        if not os.path.exists(sJsonPath):
            print(f"❌ Scenario file does not exist: {sJsonPath}")
            return

        if not os.path.exists(sTemplatePath):
            print(f"❌ Excel template file does not exist: {sTemplatePath}")
            return

        os.makedirs(Utils.Config.EXCEL_DIR, exist_ok=True)

        sExcelOutputPath = os.path.join(
            Utils.Config.EXCEL_DIR,
            sExcelName if sExcelName else sFileName.replace(".json", ".xlsx")
        )

        generator = ExcelGenerator(
            jsonPath=sJsonPath,
            templatePath=sTemplatePath,
            outputPath=sExcelOutputPath
        )
        generator.generate()
