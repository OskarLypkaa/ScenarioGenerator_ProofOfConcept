from Core.ScenarioRecorder import ScenarioRecorder

class DescriptionService:
    def __init__(self, recorder: ScenarioRecorder):
        self.recorder = recorder
        self.dClassNameMap = {
            "AfxFrameOrView140u": "drawingArea",
            "SysTreeView32": "TreeView Panel"
        }

    def generateDescriptions(self):
        steps = self.recorder.getSteps()

        for step in steps:
            iStepNumber = step["Step Number"]
            takenAction = self._describeTakenAction(step)
            expectedResult = self._describeExpectedResult(step)

            self.recorder.updateStep(
                iStepNumber=iStepNumber,
                sTakenAction=takenAction,
                sExpectedResult=expectedResult
            )

    def _getClassName(self, sRawClassName: str) -> str:
        return self.dClassNameMap.get(sRawClassName, sRawClassName)

    def _describeTakenAction(self, dStep: dict) -> str:
        dBefore = dStep.get("Action Info before", {})
        sActionType = dBefore.get("type of action", "")
        sElement = dBefore.get("elementName") or ""
        sClass = self._getClassName(dBefore.get("elementClassName", ""))
        sCtrlType = dBefore.get("elementControlType", "")
        sTyped = dStep.get("Taken Action", "")

        if "Typing" in sActionType:
            target = sElement or sClass or sCtrlType
            return f"Insert value '{sTyped}' inside {target}.".strip()

        if "Click" in sActionType:
            if sElement:
                return f"Click on element: {sElement}."
            elif sClass:
                return f"Click inside {sClass}."
            elif sCtrlType:
                return f"Click on {sCtrlType}."
            else:
                return "Click on unidentified UI element."

        return sActionType or "Unknown action"

    def _describeExpectedResult(self, dStep: dict) -> str:
        dAfter = dStep.get("Action Info After", {})
        if not dAfter:
            return self._fallbackExpectedResult(dStep)

        sClass = self._getClassName(dAfter.get("elementClassName", ""))
        sElement = dAfter.get("elementName") or ""
        sCtrlType = dAfter.get("elementControlType", "")
        sOCR = dAfter.get("ocrText", "").replace("\n", " ").strip()

        parts = []
        if sCtrlType:
            parts.append(f"{sCtrlType}")
        if sElement:
            parts.append(f"'{sElement}'")
        elif sClass:
            parts.append(f"in {sClass}")
        if sOCR:
            sShort = sOCR[:50] + "..." if len(sOCR) > 50 else sOCR
            parts.append(f"visible text: \"{sShort}\"")

        return " and ".join(parts).strip()

    def _fallbackExpectedResult(self, dStep: dict) -> str:
        """Generate a generic expected result if no Action Info After is provided."""
        sAction = self._describeTakenAction(dStep)

        if "Insert value" in sAction:
            return "Value appears inside the field."

        if "Click" in sAction:
            return "Expected reaction of the clicked element."

        return "Expected result after the action is completed."
