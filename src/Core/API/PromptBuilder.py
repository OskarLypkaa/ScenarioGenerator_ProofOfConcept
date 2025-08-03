class PromptBuilder:
    @staticmethod
    def buildPromptFromStep(dStep: dict) -> str:
        dBefore = dStep.get("Action Info before", {})
        dAfter = dStep.get("Action Info After", {})

        sBase = "[TASK] Based on the image(s) and metadata below, generate or improve the following two fields:\n- 'Taken Action'\n- 'Expected Result'\n"

        sMeta = f"""
[BEFORE]
Title: {dBefore.get('title')}
ClassName: {dBefore.get('className')}
ElementName: {dBefore.get('elementName')}
ControlType: {dBefore.get('elementControlType')}
AutomationId: {dBefore.get('elementAutomationId')}
Type of Action: {dBefore.get('type of action')}
drawingAreaSteps: {dBefore.get('drawingAreaSteps')}

[AFTER]
Title: {dAfter.get('title')}
ClassName: {dAfter.get('className')}
ElementName: {dAfter.get('elementName')}
ControlType: {dAfter.get('elementControlType')}
AutomationId: {dAfter.get('elementAutomationId')}
Type of Action: {dAfter.get('type of action')}
drawingAreaSteps: {dAfter.get('drawingAreaSteps')}
        """.strip()

        return f"{sBase}\n\n{sMeta}\n\nReturn only the improved 'Taken Action' and 'Expected Result'. If drawingAreaSteps has value, please use it in the generated strings."
