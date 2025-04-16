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
        if not os.path.exists(sJsonPath):
            print(f"❌ Scenario file does not exist: {sJsonPath}")
            return

        if sExcelName is None:
            sExcelName = os.path.splitext(sFileName)[0] + ".xlsm"

        sExcelPath = os.path.join(Utils.Config.EXPORT_DIR, sExcelName)
        sTemplatePath = Utils.Config.EXCEL_TEMPLATE_PATH  # zakładamy że masz to w configu

        try:
            gen = ExcelGenerator(
                jsonPath=sJsonPath,
                templatePath=sTemplatePath,
                outputPath=sExcelPath
            )
            gen.generate()
            print(f"✅ Excel exported to: {sExcelPath}")
        except Exception as e:
            print(f"❌ Excel export failed: {e}")

