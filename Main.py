from Core.ScenarioManager import ScenarioManager

def main():
    mManager = ScenarioManager()
    mManager.startRecordingScenario()

    # Optional: wait or block to keep the script alive
    print("▶ Recording started. Press Enter to stop.")
    input()

    mManager.stopRecordingScenario()
    print("⏹ Recording stopped.")

if __name__ == "__main__":
    main()
