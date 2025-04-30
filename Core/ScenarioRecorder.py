import json
import os
from typing import Optional

class ScenarioRecorder:
   def __init__(self, sPath: Optional[str] = None):
      self.aSteps = [] 
      if sPath:
         self.sPath = sPath
         if os.path.exists(sPath):
            self._load()
         else:
            self._save()

   def _load(self):
      with open(self.sPath, "r", encoding="utf-8") as f:
         self.aSteps = json.load(f)

   def _save(self):
      with open(self.sPath, "w", encoding="utf-8") as f:
         json.dump(self.aSteps, f, indent=4, ensure_ascii=False)

   def _getNextStepNumber(self) -> int:
      return len(self.aSteps) + 1

   def addStep(
      self,
      dActionInfoBefore: dict,
      sTakenAction: str = "",
      sTakenActionPic: Optional[str] = None,
      dActionInfoAfter: Optional[dict] = None,
      sExpectedResult: str = "",
      sExpectedResultPic: Optional[str] = None
   ):
      iStep = self._getNextStepNumber()

      dStep = {
         "Step Number": iStep,
         "Action Info before": dActionInfoBefore,
         "Taken Action": sTakenAction,
         "Taken Action Picture": sTakenActionPic,
         "Action Info After": dActionInfoAfter or {},
         "Expected Result": sExpectedResult,
         "Expected Result Picture": sExpectedResultPic
      }

      self.aSteps.append(dStep)
      self._save()

   def updateStep(
      self,
      iStepNumber: int,
      sTakenAction: Optional[str] = None,
      sExpectedResult: Optional[str] = None,
      sTakenActionPic: Optional[str] = None,
      sExpectedResultPic: Optional[str] = None,
      dActionInfoAfter: Optional[dict] = None
   ):
      for dStep in self.aSteps:
         if dStep["Step Number"] == iStepNumber:
            if sTakenAction is not None:
               dStep["Taken Action"] = sTakenAction
            if sExpectedResult is not None:
               dStep["Expected Result"] = sExpectedResult
            if sTakenActionPic is not None:
               dStep["Taken Action Picture"] = sTakenActionPic
            if sExpectedResultPic is not None:
               dStep["Expected Result Picture"] = sExpectedResultPic
            if dActionInfoAfter is not None:
               dStep["Action Info After"] = dActionInfoAfter
            break
      self._save()

   def getSteps(self) -> list:
      return self.aSteps

   def clearAll(self):
      self.aSteps = []
      self._save()
