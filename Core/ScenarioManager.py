import os
import json
from Core.Screenshot.ScreenshotService import ScreenshotService
from Core.Description.DescriptionService import DescriptionService
from Core.ScenarioRecorder import ScenarioRecorder
from Core.Excel.ExcelGenerator import ExcelGenerator
from Core.API.OpenAIClient import OpenAIClient
from Core.API.PromptBuilder import PromptBuilder
import Utils.Config

class ScenarioManager:
    def __init__(self):
        self.oRecorder = None
        self.oScreenshotService = None
        self.oDescriptionService = None
        self.oOpenAIClient = OpenAIClient(sApiKey=Utils.Config.OPENAI_API_KEY)

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

    def enhanceDescriptionsWithAI(self, sFileName: str):
        sFullPath = os.path.join(Utils.Config.SCENARIO_DIR, sFileName)
        if not os.path.exists(sFullPath):
            print(f"❌ Scenario file does not exist: {sFullPath}")
            return

        with open(sFullPath, "r", encoding="utf-8") as f:
            lSteps = json.load(f)

        for dStep in lSteps:
            sPrompt = PromptBuilder.buildPromptFromStep(dStep)

            lImages = [dStep.get("Taken Action Picture")]
            if dStep.get("Expected Result Picture"):
                lImages.append(dStep["Expected Result Picture"])

            try:
                sResponse = self.oOpenAIClient.sendStepToAI(sPrompt, lImages)
                
                lLines = [l.strip() for l in sResponse.strip().splitlines() if l.strip()]
                if len(lLines) >= 2:
                    dStep["Taken Action"] = lLines[0]
                    dStep["Expected Result"] = lLines[1]
                    print(f"✅ Step {dStep['Step Number']} updated.")
                else:
                    print(f"⚠ Step {dStep['Step Number']} – AI response not usable.")

            except Exception as e:
                print(f"❌ Step {dStep['Step Number']} – AI request failed: {e}")

        with open(sFullPath, "w", encoding="utf-8") as f:
            json.dump(lSteps, f, indent=4, ensure_ascii=False)
            print(f"💾 Updated scenario saved to: {sFullPath}")

    def exportToExcel(self, sFileName: str, sExcelName: str = None):
        sJsonPath = os.path.join(Utils.Config.SCENARIO_DIR, sFileName)
        if not os.path.exists(sJsonPath):
            print(f"❌ Scenario file does not exist: {sJsonPath}")
            return

        if sExcelName is None:
            sExcelName = os.path.splitext(sFileName)[0] + ".xlsm"

        sExcelPath = os.path.join(Utils.Config.EXPORT_DIR, sExcelName)
        sTemplatePath = Utils.Config.EXCEL_TEMPLATE_PATH

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
