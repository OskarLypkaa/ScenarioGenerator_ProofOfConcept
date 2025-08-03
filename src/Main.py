from Core.ScenarioManager import ScenarioManager
from utilities.logger import log


def main():
    log.info("Application started")
    mManager = ScenarioManager()

    sFileName = input("📝 Enter name for new scenario file (e.g. `test_scenario.json`): ").strip()
    if not sFileName.endswith(".json"):
        sFileName += ".json"

    mManager.startRecordingScenario(sFileName)

    log.info("Recording started. Press Enter to stop.")
    input()

    mManager.stopRecordingScenario()
    log.info("Recording stopped.")

    bGenerate = input("🔍 Generate basic descriptions now? (y/n): ").strip().lower()
    if bGenerate == "y":
        mManager.updateDecriptions(sFileName)

    bAIEnhance = input("🤖 Enhance descriptions with AI? (y/n): ").strip().lower()
    if bAIEnhance == "y":
        mManager.enhanceDescriptionsWithAI(sFileName)

    bExport = input("📤 Export to Excel (.xlsm)? (y/n): ").strip().lower()
    if bExport == "y":
        mManager.exportToExcel(sFileName)

    log.info("Application finished")


if __name__ == "__main__":
    main()

