from Core.ScenarioManager import ScenarioManager

def main():
    mManager = ScenarioManager()

    sFileName = input("📝 Enter name for new scenario file (e.g. `test_scenario.json`): ").strip()
    if not sFileName.endswith(".json"):
        sFileName += ".json"

    mManager.startRecordingScenario(sFileName)

    print("▶ Recording started. Press Enter to stop.")
    input()

    mManager.stopRecordingScenario()
    print("⏹ Recording stopped.")

    bGenerate = input("🔍 Generate basic descriptions now? (y/n): ").strip().lower()
    if bGenerate == "y":
        mManager.updateDecriptions(sFileName)

    bAIEnhance = input("🤖 Enhance descriptions with AI? (y/n): ").strip().lower()
    if bAIEnhance == "y":
        mManager.enhanceDescriptionsWithAI(sFileName)

    bExport = input("📤 Export to Excel (.xlsm)? (y/n): ").strip().lower()
    if bExport == "y":
        mManager.exportToExcel(sFileName)

if __name__ == "__main__":
    main()

"""
🔴 IMPORTANT NOW
----------------
    - Determine if there is a time window between clicking a mouse/key and the action being reflected in SEE.
      If yes, we can capture more accurate 'before' and 'after' inputs.
    - In Excel generation, add auto-save after image insertion.
    - Integrate free AI models to extract more information from screenshots.
    - Use those AI models to generate action descriptions.
    - Improve click pointer on images (make it semi-transparent so it doesn't block the view).
    - Add gitignore.
    - Make API calls less expensive by correcting the question in prompt and by resizing the images
    - Try to correct Model so the results are smaller and more precised
    
🟡 NOT IMPORTANT NOW
---------------------
    - Redesign code structure for readability and maintainability (apply clean code principles and read about design patterns, maybe add packages and modules).
    - Add functionality to detect a process/window created immediately after left-click.
    - Consider doing the same with key input (e.g. Enter press).
    - Implement double-click detection and step generation.
    - Right-click should also generate a step:
        - "Before" = where user right-clicked.
        - "After" = the popup that appeared.
    - Fix issue where "After" screenshot is not generated when it should be.
    - Update the package installer.

🟢 WILL BE DONE LATER
---------------------
    - Improve description generation for clicking drawing area. Snap the values of steps that are on the bottom-right corner of SEE.
    - Add OpenAI API integration for auto-generated descriptions.
    - Create a GUI for controlling the system.
    - Create posibility to customize the shortcuts.

🔵 TO CONSIDER
---------------------
    - Automatically alternate between object/dialog view depending on what it is. 
      If it's like SEE main window, objects would be more preferable if is's small dialog, then opposite.
    - Create a GUI panel for viewing all of the actions (Screens taken).
    - Somehow integrating flaUI to fetch more data from the objects.
    - If OpenAI turns out to be too expesive maybe going for DeepSeek run locally would be a good idea.
    - Think of new python libs that could be usefull here.
"""

