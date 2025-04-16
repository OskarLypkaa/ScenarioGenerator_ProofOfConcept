from pynput import mouse, keyboard
import threading
import Utils.Config
from Core.Screenshot.ScreenshotLogic import ScreenshotLogic
from Core.ScenarioRecorder import ScenarioRecorder
from datetime import datetime
from threading import Timer

class ScreenshotService:
    def __init__(self, sSaveDir=Utils.Config.SCREENSHOTS_DIR):
        self.logic = ScreenshotLogic(sSaveDir)
        self.bCaptureFullWindow = False
        self.bBlockClickScreens = True
        self.mMouseListener = None
        self.mKeyboardListener = None
        self.pressedKeys = set()
        self.recorder = ScenarioRecorder()
        self.bBeforeCaptured = False  

        # Typing tracking
        self.sTypedBuffer = ""
        self.lastKeyTime = None
        self.typingTimer = None
        self.typingDelay = 2.0  # seconds

    def _onClick(self, iX, iY, bButton, bPressed):
        if not bPressed:
            return

        tRect, _ = self.logic.getWindowUnderMouse(self.bCaptureFullWindow)

        if bButton.name == "left" and self.bBlockClickScreens:
            sPath = self.logic.saveScreenshotWithMarker(tRect, iX, iY, "Before")

            dInfo = self.logic.getSimplifiedWindowInfo(self.bCaptureFullWindow)
            dInfo["type of action"] = "Click"

            self.recorder.addStep(
                dActionInfoBefore=dInfo,
                sTakenActionPic=sPath
            )

    def _onKeyPress(self, key):
        self.pressedKeys.add(key)

        if hasattr(key, 'char') and key.char is not None:
            self.sTypedBuffer += key.char
            self._resetTypingTimer()

        elif key == keyboard.Key.space:
            self.sTypedBuffer += ' '
            self._resetTypingTimer()

        elif key == keyboard.Key.backspace:
            self.sTypedBuffer = self.sTypedBuffer[:-1]
            self._resetTypingTimer()

        elif key == keyboard.Key.enter:
            self.sTypedBuffer += '\n'
            self._finalizeTypingAction()

    def _onKeyRelease(self, key):
        if key == keyboard.Key.f11:
            self.bCaptureFullWindow = not self.bCaptureFullWindow
            print(f"🪟 Full window capture mode: {'ON' if self.bCaptureFullWindow else 'OFF'}")

        elif key == keyboard.Key.f12:
            self.bBlockClickScreens = not self.bBlockClickScreens
            print(f"🚑 Left-click screenshots mode: {'ON' if self.bBlockClickScreens else 'OFF'}")

        elif keyboard.Key.ctrl_l in self.pressedKeys or keyboard.Key.ctrl_r in self.pressedKeys:
            if keyboard.Key.shift in self.pressedKeys:
                threading.Thread(
                    target=self._triggerCapture,
                    args=("Before",),
                    daemon=True
                ).start()
            elif keyboard.Key.alt_l in self.pressedKeys or keyboard.Key.alt_r in self.pressedKeys:
                if self.bBeforeCaptured:  
                    threading.Thread(
                        target=self._triggerCapture,
                        args=("After",),
                        daemon=True
                    ).start()
                else:
                    print("[⚠] Cannot capture 'After' without a prior 'Before'.")

        if key in self.pressedKeys:
            self.pressedKeys.remove(key)

    def _resetTypingTimer(self):
        self.lastKeyTime = datetime.now()

        if self.typingTimer:
            self.typingTimer.cancel()

        self.typingTimer = Timer(self.typingDelay, self._finalizeTypingAction)
        self.typingTimer.start()

    def _finalizeTypingAction(self):
        sText = self.sTypedBuffer.strip()
        if not sText:
            return

        tRect, (iMouseX, iMouseY) = self.logic.getWindowUnderMouse(self.bCaptureFullWindow)
        sPath = self.logic.saveScreenshotWithMarker(tRect, iMouseX, iMouseY, "Typed")

        dInfo = self.logic.getSimplifiedWindowInfo(self.bCaptureFullWindow)
        dInfo["type of action"] = f"Typing: {sText}"

        self.recorder.addStep(
            dActionInfoBefore=dInfo,
            sTakenAction=sText,
            sTakenActionPic=sPath
        )

        print(f"[✔] Typing action saved: {sText}")

        self.sTypedBuffer = ""
        self.typingTimer = None

    def _triggerCapture(self, prefix):
        tRect, (iMouseX, iMouseY) = self.logic.getWindowUnderMouse(self.bCaptureFullWindow)
        sPath = self.logic.saveScreenshotWithMarker(tRect, iMouseX, iMouseY, prefix)

        if prefix == "Before":
            dInfo = self.logic.getSimplifiedWindowInfo(self.bCaptureFullWindow)
            dInfo["type of action"] = "Click"
            self.recorder.addStep(
                dActionInfoBefore=dInfo,
                sTakenActionPic=sPath
            )
            self.bBeforeCaptured = True  

        elif prefix == "After":
            dInfo = self.logic.getSimplifiedWindowInfo(self.bCaptureFullWindow)
            dInfo["type of action"] = "Screenshot"

            lastStep = len(self.recorder.getSteps())
            if lastStep > 0:
                self.recorder.updateStep(
                    iStepNumber=lastStep,
                    sExpectedResultPic=sPath,
                    dActionInfoAfter=dInfo
                )
            self.bBeforeCaptured = False 

    def startListener(self):
        print("▶ Listening for mouse and hotkeys...")
        self.mMouseListener = mouse.Listener(on_click=self._onClick)
        self.mMouseListener.start()
        self.mKeyboardListener = keyboard.Listener(
            on_press=self._onKeyPress,
            on_release=self._onKeyRelease
        )
        self.mKeyboardListener.start()

    def stopListener(self):
        if self.mMouseListener:
            self.mMouseListener.stop()
        if self.mKeyboardListener:
            self.mKeyboardListener.stop()
        print("⏹ Listeners stopped.")
