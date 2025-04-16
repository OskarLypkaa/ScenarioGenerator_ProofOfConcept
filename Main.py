from Core.ScenarioManager import ScenarioManager
from Core.Excel.ExcelGenerator import ExcelGenerator
def main():
    mManager = ScenarioManager()

    gen = ExcelGenerator(
        jsonPath=r"C:\Users\oskar.lypka\Desktop\Output\Scenario\VSCSDA.json",
        templatePath=r"C:\Users\oskar.lypka\Desktop\Self Learnign\ManualScenarioGenerator\Templates\Template.xlsm",  # opcjonalne, nieużywane
        outputPath=r"C:\Users\oskar.lypka\Desktop\Output\Excel\export.xlsm"
    )
    gen.generate()
    # sFileName = input("📝 Enter name for new scenario file (e.g. `test_scenario.json`): ").strip()
    # if not sFileName.endswith(".json"):
    #     sFileName += ".json"

    # mManager.startRecordingScenario(sFileName)

    # print("▶ Recording started. Press Enter to stop.")
    # input()

    # mManager.stopRecordingScenario()
    # print("⏹ Recording stopped.")

    # bGenerate = input("🔍 Generate descriptions now? (y/n): ").strip().lower()
    # if bGenerate == "y":
    #     mManager.updateDecriptions(sFileName)

if __name__ == "__main__":
    main()
