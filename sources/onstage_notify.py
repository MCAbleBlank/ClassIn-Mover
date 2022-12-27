# ClassIn Mover - A program to move ClassIn classroom window in order to
# exit from focused learning mode.

# Copyright (C) 2020-2022  Weiqi Gao, Jize Guo, Yiming Geng

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import ctypes
import logging
import re
import struct
import threading
import tkinter.messagebox

import hardwareUsageDetect
import shared


def filetime2timestamp_ms(filetime):
    return filetime // 10000 - 11644473600000


class on_stage_notify:
    notify_types = {0: "None", 1: "MsgBox", 2: "MsgBox model", 3: "Switch To", 4: "Close Window", 5: "Stop Program"}

    def __init__(self, notify_type, notify_in_classroom, GetText, WindowSelector):
        self.cam = hardwareUsageDetect.WebcamDetect()
        self.mic = hardwareUsageDetect.MicDetect()
        if self.cam.not_supported or self.mic.not_supported:
            self.not_supported = True
        else:
            self.not_supported = False
        logging.debug({"on-stage notify supported": not self.not_supported})
        self.cam_used = False
        self.mic_used = False
        self.multi_window_warned = False
        self.notify_type = notify_type
        self.GetText = GetText
        self.WindowSelector = WindowSelector
        self.notify_in_classroom = notify_in_classroom

    def __getitem__(self, __name):
        return self.notify_types[__name]

    def set_notify_type(self, notify_type):
        self.notify_type = notify_type
        shared.SetSetting("on-stage notify", notify_type)

    def set_notify_in_classroom(self, notify_in_classroom):
        self.notify_in_classroom = notify_in_classroom
        shared.SetSetting("notify-in-classroom", notify_in_classroom)

    def detect_and_notify(self):
        if not self.notify_type:
            return
        cam = self.cam.getActiveApps()
        mic = self.mic.getActiveApps()
        cam_using = None
        mic_using = None
        for i in cam:
            if i.lower().endswith("classin.exe"):
                cam_using = cam[i]
        for i in mic:
            if i.lower().endswith("classin.exe"):
                mic_using = mic[i]
        notify = (cam_using and not self.cam_used) or (mic_using and not self.mic_used)
        self.cam_used = cam_using is not None
        self.mic_used = mic_using is not None
        if notify:
            if not self.notify_in_classroom:
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                pid = struct.pack("l", (0))
                ctypes.windll.user32.GetWindowThreadProcessId(hwnd, pid)
                pid = struct.unpack("l", pid)[0]
                ProcessHandle = ctypes.windll.kernel32.OpenProcess(0x0410, 0, pid)
                if ProcessHandle != 0:
                    Name_Buffer = ctypes.create_unicode_buffer("", 260)
                    ctypes.windll.psapi.GetModuleFileNameExW(ProcessHandle, 0, Name_Buffer, 260)
                    ctypes.windll.kernel32.CloseHandle(ProcessHandle)
                    if Name_Buffer.value.lower().endswith("classin.exe"):
                        return
            if self.notify_type == 1:
                threading.Thread(
                    target=self._notify_msgbox, args=(cam_using is not None, mic_using is not None)
                ).start()
            elif self.notify_type == 2:
                threading.Thread(
                    target=self._notify_msgbox, args=(cam_using is not None, mic_using is not None, True)
                ).start()
            elif self.notify_type == 3:
                self._switch_to()
            elif self.notify_type == 4:
                self._close_window()
            elif self.notify_type == 5:
                self._stop_process()

    @shared.ShowThread
    def warn_multi_windows(self):
        if (not self.multi_window_warned) and (self.notify_type >= 3):
            # self.multi_window_warned = True
            tkinter.messagebox.showwarning(self.GetText("Warning"), self.GetText("multi window on-stage"))

    @shared.ShowThread
    def _notify_msgbox(self, cam=False, mic=False, model=False):
        if not (cam or mic):
            return
        if model:
            ctypes.windll.user32.MessageBoxW(
                ctypes.windll.user32.GetForegroundWindow(),
                ctypes.create_unicode_buffer(
                    (self.GetText("cam open") if cam else "") + "\n" + (self.GetText("mic open") if mic else "")
                ),
                ctypes.create_unicode_buffer("ClassIn Mover " + self.GetText("on-stage notify")),
                0x00001030,
            )
        else:
            ctypes.windll.user32.MessageBoxW(
                0,
                ctypes.create_unicode_buffer(
                    (self.GetText("cam open") if cam else "") + "\n" + (self.GetText("mic open") if mic else "")
                ),
                ctypes.create_unicode_buffer("ClassIn Mover " + self.GetText("on-stage notify")),
                0x00001030,
            )

    def _switch_to(self):
        s = self.WindowSelector.get()
        if len(s) == 0:
            return
        logging.info("Switching to %d" % int(re.findall("^\\d+", s)[0]))
        shared.SwitchWindow(int(re.findall("^\\d+", s)[0]))

    def _close_window(self):
        s = self.WindowSelector.get()
        if len(s) == 0:
            return
        ctypes.windll.user32.SendMessageW(int(re.findall("^\\d+", s)[0]), 0x10, 0, 0)

    def _stop_process(self):
        s = self.WindowSelector.get()
        if len(s) == 0:
            return
        h = ctypes.windll.kernel32.OpenProcess(0x1, 0, int(re.findall("[Pp][Ii][Dd]=(\\d+)", s)[0]))
        if not h:
            return
        ctypes.windll.kernel32.TerminateProcess(h, 1)
        ctypes.windll.kernel32.CloseHandle(h)
