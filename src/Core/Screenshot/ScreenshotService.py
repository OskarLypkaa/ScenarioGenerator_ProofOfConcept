import ctypes
import ctypes.wintypes
import threading
import time
from Core.Screenshot.ScreenshotLogic import ScreenshotLogic
from Core.ScenarioRecorder import ScenarioRecorder
import Utils.Config

user32 = ctypes.windll.user32

WH_MOUSE_LL = 14
WM_LBUTTONDOWN = 0x0201

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", ctypes.wintypes.POINT),
        ("mouseData", ctypes.wintypes.DWORD),
        ("flags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong),
    ]

class ScreenshotService:
    def __init__(self, sSaveDir=Utils.Config.SCREENSHOTS_DIR):
        self.logic = ScreenshotLogic(sSaveDir)
        self.recorder = ScenarioRecorder()
        self.bCaptureFullWindow = False
        self.hookThread = None
        self.hookId = None
        self.mouseProcPtr = None

    def _lowLevelMouseProc(self, nCode, wParam, lParam):
        if nCode == 0 and wParam == WM_LBUTTONDOWN:
            mouseStruct = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
            iMouseX = mouseStruct.pt.x
            iMouseY = mouseStruct.pt.y

            # --- BEFORE ---
            tRect, _ = self.logic.getWindowUnderMouse(self.bCaptureFullWindow)
            sBefore = self.logic.saveScreenshotWithMarker(tRect, iMouseX, iMouseY, "Before")
            dInfoBefore = self.logic.getSimplifiedWindowInfo(self.bCaptureFullWindow)
            dInfoBefore["type of action"] = "Click"

            before_windows = set(self.logic.get_all_windows_of_process("SEE.exe"))
            print(dInfoBefore.get("Action Info before", {}).get("elementName", ""))
            if dInfoBefore.get("elementName", "").startswith("Open") and not dInfoBefore.get("elementControlType", "").startswith("MenuItem"):
                time.sleep(5.0)
            else:
                time.sleep(1.0)




            after_windows = set(self.logic.get_all_windows_of_process("SEE.exe"))

            new_windows = list(after_windows - before_windows)
            closed_windows = list(before_windows - after_windows)

            if not new_windows and not closed_windows:
                tRect, _ = self.logic.getWindowUnderMouse(self.bCaptureFullWindow)
                sAfter = self.logic.saveScreenshotWithMarker(tRect, iMouseX, iMouseY, "After")
                dInfoAfter = self.logic.getSimplifiedWindowInfo(self.bCaptureFullWindow)
                dInfoAfter["type of action"] = "Element is clicked"
                self.recorder.addStep(
                    dActionInfoBefore=dInfoBefore,
                    sTakenActionPic=sBefore,
                    dActionInfoAfter=dInfoAfter,
                    sExpectedResultPic=sAfter
                )
                print(f"[✔] Captured BEFORE and AFTER for click at ({iMouseX}, {iMouseY})")
            
            if new_windows:
                if self.logic.isWindowVisible(new_windows[0]):
                    sWindow = self.logic.saveWindowScreenshot(new_windows[0], sPrefix="NewWindow")
                    dInfo = self.logic.getWindowInfo(new_windows[0])
                    dInfo["type of action"] = "New window is displayed"
                    self.recorder.addStep(
                        dActionInfoBefore=dInfoBefore,
                        sTakenActionPic=sBefore,
                        dActionInfoAfter=dInfo,
                        sExpectedResultPic=sWindow
                    )
                    print(f"[✔] Screenshot saved for NEW window: hwnd={new_windows[0]}")
            elif closed_windows:
                sScreen = self.logic.saveFullScreenScreenshot(sPrefix="ClosedWindow")
                dInfo = {
                    "type of action": "Window is closed",
                    "closed_hwnd": closed_windows[0]
                }
                self.recorder.addStep(
                    dActionInfoBefore=dInfoBefore,
                    sTakenActionPic=sBefore,
                    dActionInfoAfter=dInfo,
                    sExpectedResultPic=sScreen
                )
                print(f"[✔] Screenshot saved for CLOSED window: hwnd={closed_windows[0]}")

            

        return user32.CallNextHookEx(
            None,
            ctypes.c_int(nCode),
            ctypes.wintypes.WPARAM(wParam),
            ctypes.wintypes.LPARAM(lParam)
        )


    def _installHook(self):
        CMPFUNC = ctypes.WINFUNCTYPE(
            ctypes.c_int, ctypes.c_int, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM
        )
        self.mouseProcPtr = CMPFUNC(self._lowLevelMouseProc)
        self.hookId = user32.SetWindowsHookExW(WH_MOUSE_LL, self.mouseProcPtr, 0, 0)

        if not self.hookId:
            raise Exception("❌ Failed to install mouse hook.")

        msg = ctypes.wintypes.MSG()
        while True:
            user32.GetMessageW(ctypes.byref(msg), 0, 0, 0)

    def startListener(self):
        print("▶ Listening for mouse clicks (Windows Hook)...")
        self.hookThread = threading.Thread(target=self._installHook, daemon=True)
        self.hookThread.start()

    def stopListener(self):
        if self.hookId:
            user32.UnhookWindowsHookEx(self.hookId)
            print("⏹ Mouse hook removed.")
