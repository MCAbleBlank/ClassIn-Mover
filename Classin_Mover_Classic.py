# ClassIn Mover - A program to move ClassIn classroom window in order to
# exit from focused learning mode.

# Copyright (C) 2020-2022  Weiqi Gao, Jize Guo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__version__ = "2.0.0c"

import tkinter
import tkinter.ttk
import ctypes
import ctypes.wintypes
import struct
import time
import datetime
import math
import threading
import sys
import os
import shlex
import psutil
import pathlib

ClassInHwnd = []
ClassInTitle = []
ClassInPID = []
run = True
NoAdmin = False


def has_admin():
    try:
        # only windows users with admin privileges can read the C:\windows\temp
        os.listdir(os.sep.join([os.environ.get("SystemRoot", "C:\\windows"), "temp"]))
    except:
        return os.environ["USERNAME"], False
    else:
        return os.environ["USERNAME"], True


if __name__ == "__main__" and not has_admin()[1]:
    p = psutil.Process().cmdline()
    res = ctypes.windll.shell32.ShellExecuteW(
        0,
        ctypes.create_unicode_buffer("runas"),
        ctypes.create_unicode_buffer(p[0]),
        ctypes.create_unicode_buffer(shlex.join(p[1:])),
        0,
        5,
    )
    if res > 32:
        raise SystemExit
    NoAdmin = True


@ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def EnumWindowCallback(hwnd, lParam):
    global ClassInHwnd, ClassInPID, ClassInTitle
    textlen = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    text = ctypes.create_unicode_buffer("", textlen + 20)
    ctypes.windll.user32.GetWindowTextW(hwnd, text, textlen + 20)
    Caption = text.value
    if not Caption.startswith("Classroom_"):
        return 1
    pid = struct.pack("l", (0))
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, pid)
    pid = struct.unpack("l", pid)[0]
    processHandle = ctypes.windll.kernel32.OpenProcess(0x0410, 0, pid)
    if processHandle == 0:
        return 1
    name_buffer = ctypes.create_unicode_buffer("", 260)
    ctypes.windll.psapi.GetModuleFileNameExW(processHandle, 0, name_buffer, 260)
    ctypes.windll.kernel32.CloseHandle(processHandle)
    if not name_buffer.value.lower().endswith("classin.exe"):
        return 1
    ClassInHwnd.append(hwnd)
    ClassInTitle.append(Caption)
    ClassInPID.append(pid)
    return 1


def GetClassInHwnd():
    global ClassInHwnd, ClassInPID, ClassInTitle
    ClassInHwnd = []
    ClassInTitle = []
    ClassInPID = []
    ctypes.windll.user32.EnumWindows(EnumWindowCallback, 0)
    return list(zip(ClassInPID, ClassInHwnd, ClassInTitle))


def GetWindowCmd(showCmd):
    if showCmd in [2, 6]:
        return "Minimized"
    elif showCmd == 3:
        return "Maximized"
    elif showCmd == 1:
        return "Normal"
    else:
        return str(showCmd)


def PatchWindow():
    global run
    try:
        while run:
            count = 0
            st = time.time()
            CIHwnd = GetClassInHwnd()
            if len(CIHwnd) == 0:
                AddText("[%s] Cannot find classroom window\n" % datetime.datetime.now().strftime("%H:%M:%S"))
                wait = math.ceil(st) - time.time()
                time.sleep(wait if wait >= 0 else 0)
                continue
            CIHwnd = CIHwnd[0]
            while math.ceil(st) - time.time() >= 0.2 or count == 0:
                wp = struct.pack(
                    "III ll ll llll llll", *([struct.calcsize("III ll ll llll llll")] + [0] * 14)
                )  # WINDOWPLACEMENT
                ctypes.windll.user32.GetWindowPlacement(CIHwnd[1], wp)
                showCmd = struct.unpack("III ll ll llll llll", wp)[2]
                if not showCmd in [2, 3, 6]:
                    ctypes.windll.user32.ShowWindow(CIHwnd[1], 6)
                    ctypes.windll.user32.ShowWindow(CIHwnd[1], 3)
                rect = struct.pack("llll", *([0] * 4))
                ctypes.windll.user32.GetWindowRect(CIHwnd[1], rect)
                rect = struct.unpack("llll", rect)
                ctypes.windll.user32.SetWindowPos(
                    CIHwnd[1], ctypes.wintypes.HWND(-2), rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1], 3
                )
                count += 1
                time.sleep(0.05)
            AddText(
                "[%s] Classroom window is found and processed %d times:\n           PID=%d HWND=%d title=%s status=%s\n"
                % (
                    datetime.datetime.now().strftime("%H:%M:%S"),
                    count,
                    CIHwnd[0],
                    CIHwnd[1],
                    CIHwnd[2],
                    GetWindowCmd(showCmd),
                )
            )
            wait = math.ceil(st) - time.time()
            time.sleep(wait if wait >= 0 else 0)
    except:
        return


if __name__ == "__main__":
    w = tkinter.Tk()
    LogText = tkinter.Text(w, width=100, height=30, font=("Courier", 12), state=tkinter.DISABLED)
    LogText.pack(fill=tkinter.Y, side=tkinter.LEFT)
    LogScr = tkinter.ttk.Scrollbar(w, orient=tkinter.VERTICAL, command=LogText.yview)
    LogText.config(yscrollcommand=LogScr.set)
    LogScr.pack(fill=tkinter.Y, side=tkinter.RIGHT)
    w.resizable(False, False)
    w.title("ClassIn Mover Classic v2.0.0")
    w.iconbitmap(str(pathlib.Path(__file__).parent/"ClassIn_Mover.ico"))

    def AddText(text):
        LogText.config(state=tkinter.NORMAL)
        End = LogScr.get()[1] == 1
        LogText.insert(tkinter.END, text)
        if End:
            LogText.see(tkinter.END)
        LogText.config(state=tkinter.DISABLED)

    AddText("ClassIn Mover Classic v2.0.0\n")
    AddText("Copyright (C) 2020-2022  Weiqi Gao, Jize Guo\n")
    AddText("Visit https://github.com/CarlGao4/ClassIn-Mover for more information.\n\n")

    if NoAdmin:
        AddText("You are running this program without Administrator privilege, the program maybe can't function\n\n")

    PatchThread = threading.Thread(target=PatchWindow)
    PatchThread.start()

    w.mainloop()
    run = False
    sys.exit(0)
