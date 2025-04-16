import os
import win32gui
import win32con
from datetime import datetime
from PIL import Image, ImageDraw
import mss
from pywinauto.uia_element_info import UIAElementInfo

class ScreenshotLogic:
    def __init__(self, sSaveDir):
        self.sSaveDir = sSaveDir
        os.makedirs(self.sSaveDir, exist_ok=True)

    def getWindowUnderMouse(self, bCaptureFullWindow):
        iPoint = win32gui.GetCursorPos()
        iHandle = win32gui.WindowFromPoint(iPoint)
        hRoot = win32gui.GetAncestor(iHandle, win32con.GA_ROOT)
        if not win32gui.IsWindowVisible(hRoot):
            hRoot = win32gui.GetForegroundWindow()
        target = hRoot if bCaptureFullWindow else iHandle
        tRect = win32gui.GetWindowRect(target)
        return tRect, iPoint

    def getSimplifiedWindowInfo(self, bCaptureFullWindow: bool) -> dict:
        iPoint = win32gui.GetCursorPos()
        iHandle = win32gui.WindowFromPoint(iPoint)
        hRoot = win32gui.GetAncestor(iHandle, win32con.GA_ROOT)

        if not win32gui.IsWindowVisible(hRoot):
            hRoot = win32gui.GetForegroundWindow()

        target = hRoot if bCaptureFullWindow else iHandle

        try:
            x, y = win32gui.GetCursorPos()
            element = UIAElementInfo.from_point(x, y)

            print("📋 UI Element Info:")
            print(f"Name: {element.name}")
            print(f"Control Type: {element.control_type}")
            print(f"Class Name: {element.class_name}")
            print(f"Automation ID: {element.automation_id}")

            return {
                "title": win32gui.GetWindowText(target),
                "className": win32gui.GetClassName(target),
                "elementName": element.name,
                "elementControlType": element.control_type,
                "elementClassName": element.class_name,
                "elementAutomationId": element.automation_id
            }

        except Exception as e:
            print(f"⚠️ pywinauto failed: {e}")
            return {
                "title": win32gui.GetWindowText(target),
                "className": win32gui.GetClassName(target),
                "elementError": str(e)
            }

    def saveScreenshotWithMarker(self, tRect, iX, iY, sPrefix):
        tRelClick = self._getRelativeClickPosition(tRect, iX, iY)
        iImage = self._captureWindowImage(tRect)
        self._drawClickMarker(iImage, tRelClick)
        sPath = self._buildScreenshotPath(sPrefix)
        iImage.save(sPath)
        print(f"[✔] Screenshot saved: {sPath}")
        return sPath

    def _getRelativeClickPosition(self, tRect, iClickX, iClickY):
        iLeft, iTop, _, _ = tRect
        return iClickX - iLeft, iClickY - iTop

    def _captureWindowImage(self, tRect):
        iLeft, iTop, iRight, iBottom = tRect
        width = iRight - iLeft
        height = iBottom - iTop
        with mss.mss() as sct:
            monitor = {"left": iLeft, "top": iTop, "width": width, "height": height}
            sct_img = sct.grab(monitor)
            return Image.frombytes("RGB", sct_img.size, sct_img.rgb)

    def _drawClickMarker(self, iImage, tRelClick):
        iX, iY = tRelClick
        d = ImageDraw.Draw(iImage)
        iRadius = 20
        d.ellipse(
            [(iX - iRadius, iY - iRadius), (iX + iRadius, iY + iRadius)],
            outline="red", width=5
        )
        d.line([(iX - 10, iY), (iX + 10, iY)], fill="red", width=3)
        d.line([(iX, iY - 10), (iX, iY + 10)], fill="red", width=3)

    def _buildScreenshotPath(self, sPrefix):
        sTimestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sFileName = f"{sPrefix}_{sTimestamp}.png"
        return os.path.join(self.sSaveDir, sFileName)
