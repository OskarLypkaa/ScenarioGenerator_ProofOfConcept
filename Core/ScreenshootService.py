from pynput import mouse, keyboard
import threading
import Utils.config
from Core.ScreenshootLogic import ScreenshootLogic


class ScreenshotService:
    def __init__(self, sSaveDir=Utils.config.SCREENSHOOTS_DIR):
        self.logic = ScreenshootLogic(sSaveDir)
        self.bCaptureFullWindow = False
        self.bBlockClickScreens = True
        self.mMouseListener = None
        self.mKeyboardListener = None
        self.pressedKeys = set()

    def _onClick(self, iX, iY, bButton, bPressed):
        if not bPressed:
            return
        tRect, _ = self.logic.getWindowUnderMouse(self.bCaptureFullWindow)
        if bButton.name == "left" and self.bBlockClickScreens:
            self.logic.saveScreenshotWithMarker(tRect, iX, iY, "Before")

    def _onKeyPress(self, key):
        self.pressedKeys.add(key)

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
                threading.Thread(
                    target=self._triggerCapture,
                    args=("After",),
                    daemon=True
                ).start()

        # Usuń puszczony klawisz z zestawu
        if key in self.pressedKeys:
            self.pressedKeys.remove(key)

    def _triggerCapture(self, prefix):
        tRect, (iMouseX, iMouseY) = self.logic.getWindowUnderMouse(self.bCaptureFullWindow)
        self.logic.saveScreenshotWithMarker(tRect, iMouseX, iMouseY, prefix)

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
