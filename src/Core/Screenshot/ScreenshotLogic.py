import os
import win32gui
import win32con
from datetime import datetime
from PIL import Image, ImageDraw
import mss
from pywinauto.uia_element_info import UIAElementInfo
import psutil
import win32gui
import win32process
from utilities.logger import log

class ScreenshotLogic:
    def __init__(self, sSaveDir):
        self.sSaveDir = sSaveDir
        os.makedirs(self.sSaveDir, exist_ok=True)

    def get_process_pid(self, process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                return proc.info['pid']
        return None

    def find_popup_windows_of_process(self, process_name):
        popups = []
        pid = self.get_process_pid(process_name)
        if pid is None:
            log.warning(f"Process '{process_name}' not found")
            return []
        
        def enumHandler(hwnd, lParam):
            try:
                _, win_pid = win32process.GetWindowThreadProcessId(hwnd)
                className = win32gui.GetClassName(hwnd)
                if win_pid == pid and className == "#32768":
                    popups.append(hwnd)
            except Exception:
                pass  
        win32gui.EnumWindows(enumHandler, None)
        return popups
    
    def saveWindowScreenshot(self, hwnd, sPrefix="Popup"):
        try:
            tRect = win32gui.GetWindowRect(hwnd)
            iLeft, iTop, iRight, iBottom = tRect
            width = iRight - iLeft
            height = iBottom - iTop
            if width <= 0 or height <= 0:
                log.warning(f"Window hwnd={hwnd} has invalid dimensions")
                return None

            with mss.mss() as sct:
                monitor = {"left": iLeft, "top": iTop, "width": width, "height": height}
                sct_img = sct.grab(monitor)
                iImage = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
                sPath = self._buildScreenshotPath(sPrefix)
                iImage.save(sPath)
                log.info(f"Popup screenshot saved: {sPath}")
                return sPath
        except Exception as e:
            log.error(f"Failed to save popup screenshot: {e}")
            return None

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
            if not win32gui.IsWindow(target):
                raise Exception("Invalid window handle")

            x, y = win32gui.GetCursorPos()
            element = UIAElementInfo.from_point(x, y)
            sDrawingAreaSteps = ""
            if win32gui.GetClassName(target) == "AfxFrameOrView140u" and element.control_type == "Pane":
                sDrawingAreaSteps = self.getStatusBarText()
                return {
                    "elementName": "Drawing Area",
                    "drawingAreaSteps": sDrawingAreaSteps
                }
            return {
                "title": win32gui.GetWindowText(target),
                "className": win32gui.GetClassName(target),
                "elementName": element.name,
                "elementControlType": element.control_type,
                "elementClassName": element.class_name,
                "elementAutomationId": element.automation_id
            }

        except Exception as e:
            log.warning(f"pywinauto failed: {e}")
            return {
                "title": "",
                "className": "",
                "elementError": str(e)
            }


    def saveScreenshotWithMarker(self, tRect, iX, iY, sPrefix):
        tRelClick = self._getRelativeClickPosition(tRect, iX, iY)
        iImage = self._captureWindowImage(tRect)
        self._drawClickMarker(iImage, tRelClick)
        sPath = self._buildScreenshotPath(sPrefix)
        iImage.save(sPath)
        log.info(f"Screenshot saved: {sPath}")
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
        markerColor = "red"

        d.ellipse(
            [(iX - iRadius, iY - iRadius), (iX + iRadius, iY + iRadius)],
            outline=markerColor, width=3
        )

        crossLen = 6
        d.line([(iX - crossLen, iY), (iX + crossLen, iY)], fill=markerColor, width=2)
        d.line([(iX, iY - crossLen), (iX, iY + crossLen)], fill=markerColor, width=2)


    def _buildScreenshotPath(self, sPrefix):
        sTimestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sFileName = f"{sPrefix}_{sTimestamp}.png"
        return os.path.join(self.sSaveDir, sFileName)


    def get_all_windows_of_process(self, process_name):
        import win32gui, win32process, psutil
        pid = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                pid = proc.info['pid']
                break
        if pid is None:
            return []
        result = []
        def enumHandler(hwnd, lParam):
            try:
                _, win_pid = win32process.GetWindowThreadProcessId(hwnd)
                if win_pid == pid and win32gui.IsWindowVisible(hwnd):
                    result.append(hwnd)
            except Exception:
                pass
        win32gui.EnumWindows(enumHandler, None)
        return result


    def saveFullScreenScreenshot(self, sPrefix="FullScreen"):
        sTimestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sFileName = f"{sPrefix}_{sTimestamp}.png"
        sPath = os.path.join(self.sSaveDir, sFileName)
        with mss.mss() as sct:
            monitor = sct.monitors[0]  
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
            img.save(sPath)
        log.info(f"Full screen screenshot saved: {sPath}")
        return sPath


    def isWindowVisible(self, hwnd):
        import win32gui
        return win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd)

    def getWindowInfo(self, hwnd):
        import win32gui
        info = {}
        try:
            info["hwnd"] = hwnd
            info["className"] = win32gui.GetClassName(hwnd)
            info["title"] = win32gui.GetWindowText(hwnd)
        except Exception as e:
            info["error"] = str(e)
        return info

    def saveWindowScreenshot(self, hwnd, sPrefix="Popup"):
        try:
            import win32gui, mss, os
            from PIL import Image
            tRect = win32gui.GetWindowRect(hwnd)
            iLeft, iTop, iRight, iBottom = tRect
            width = iRight - iLeft
            height = iBottom - iTop
            if width <= 0 or height <= 0:
                log.warning(f"Window hwnd={hwnd} has invalid dimensions")
                return None

            with mss.mss() as sct:
                monitor = {"left": iLeft, "top": iTop, "width": width, "height": height}
                sct_img = sct.grab(monitor)
                iImage = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
                sPath = self._buildScreenshotPath(sPrefix)
                iImage.save(sPath)
                log.info(f"Popup screenshot saved: {sPath}")
                return sPath
        except Exception as e:
            log.error(f"Failed to save popup screenshot: {e}")
            return None

    def saveFullScreenScreenshot(self, sPrefix="FullScreen"):
        import os
        import mss
        from PIL import Image
        from datetime import datetime
        import win32api

        sTimestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sFileName = f"{sPrefix}_{sTimestamp}.png"
        sPath = os.path.join(self.sSaveDir, sFileName)

        
        mouse_x, mouse_y = win32api.GetCursorPos()

        with mss.mss() as sct:
            found_monitor = None
           
            for monitor in sct.monitors[1:]:
                if (monitor["left"] <= mouse_x < monitor["left"] + monitor["width"] and
                    monitor["top"] <= mouse_y < monitor["top"] + monitor["height"]):
                    found_monitor = monitor
                    break

            if found_monitor is None:
                
                found_monitor = sct.monitors[0]

            sct_img = sct.grab(found_monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
            img.save(sPath)
        log.info(f"Full screen screenshot saved: {sPath}")
        return sPath


    def get_all_windows_of_process(self, process_name):
        import win32gui, win32process, psutil
        pid = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                pid = proc.info['pid']
                break
        if pid is None:
            return []
        result = []
        def enumHandler(hwnd, lParam):
            try:
                _, win_pid = win32process.GetWindowThreadProcessId(hwnd)
                if win_pid == pid and win32gui.IsWindowVisible(hwnd):
                    result.append(hwnd)
            except Exception:
                pass
        win32gui.EnumWindows(enumHandler, None)
        return result


    def getStatusBarText(self):
        from pywinauto import Application
        import re

        try:
            app = Application(backend="win32").connect(path="SEE.exe")
            main = None
            for win in app.windows():
                if "SEE Electrical Expert" in win.window_text():
                    main = win
                    break
            if not main:
                log.warning("Main window not found")
                return ""
    
            statusbar = None
            for child in main.children():
                if child.friendly_class_name() == "StatusBar" or child.class_name() == "msctls_statusbar32":
                    statusbar = child
                    break
            if not statusbar:
                log.warning("Status bar not found")
                return ""

            parts = statusbar.texts()
            log.debug(f"StatusBar (pywinauto): {parts}")

            steps = []
            for part in parts:
                match = re.match(r'([0-9]+\.[0-9]+)\s*step', part)
                if match:
                    steps.append(match.group(1))
            if steps:
                return f"[{', '.join(steps)}]"
            else:
                return ""

        except Exception as e:
            log.error(f"pywinauto statusbar error: {e}")
            return ""


