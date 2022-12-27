LICENSE = """ClassIn Mover - A program to move ClassIn classroom window in order to exit from focused learning mode.
Visit https://classin-mover.pages.dev for more information. 

Copyright (C) 2020-2022  Weiqi Gao, Jize Guo, Yiming Geng

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

__version__ = "2.2.0.1"

import base64
import ctypes
import ctypes.wintypes
import datetime
import json
import locale
import logging
import lzma
import math
import os
import pathlib
import pickle
import platform
import re
import struct
import sys
import threading
import time
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
import traceback
import urllib
import urllib.request
import webbrowser

import PIL.ImageTk
import psutil

import onstage_notify
import shared
import shlex4all

ClassInHwnd = []
ClassInTitle = []
ClassInPID = []
afters = []
run = True
settings = {}
reset = False
blogs = {}
NoAdmin = False
downloading = False
icon = "{Wp48S^xk9=GL@E0stWa8~^|S5YJf5;2U}bTwMS_0S<J)6G#OOiPpNM;*@Fj1BWIuCwWQy0mm_9O|kqdhwb(tj#Qr*3vsgDuvI(Ee6R+Api2XKpWV((sGFN%%b?5rcv_twUzDpR9?A0&+{;KR`GDmVu!~IoRpi#1^r^*bP=x>utk(&RFR4j{%+q=&AcwOj?0q6bMGbl!Im1>XaLNxyId|i*No_P%Hjd=6m_wVLX7N_*0e}8#y_@f{zg0_I^e%wPYX9Loz?FOUjo{Gl#$cV6DH68Ek#L~*&6@mvT;R-e{~rKeV4rnWA^?un$vE4EQw;h4XYhRiHK#C17<*;VXkbH30?evIrh@?ion41=%ZabgE-Apfu&17U{*H6`i^(5OV6G+8y_03C4Ftw{>aIhVwx)24=>h;6vZ-Fvho~j#{mRf(#(5emAFPH%`iN}4s3)A2mf@u7T<kyj(D{PsdF*+qTPqUo94t|70bv5x;M}{*(@}Bb4@2%cWFp`wCO48|Z{&@X6R?&23<(X)Pa72obcpH1Jcm#NuO2U<$J$mJc?~6A!28-gMVOl75?ZSyfNM(N+eSu16t$)A+|-SXr|mfALT&U%cEA$sZ(Pvz>DcENepc5~GqK$loH`CHXJo4d!LtJVKA~W3Bsi98W8MW<Fin|E_~f-tE%y-fzzO2lZ0>Jeu2d-!kYi0qZ!<u0%T+1<{x(v54(33JX6yV>?@v$Fo-##|Ew`5=WIOLAt9|gVJOjPmVG<HKV#$C;V{9J3Me(E$X1~It<VJj5+q8Dk0%{?Zcr{XL6QG12Rd+ppTsAp0;bbg@0yX_@4au;B*wF*(UHC$J?`>dnD1`h9y#1N_)kTxSTr0M+ANGAA)blJO<SWWz&c;J+uEmLh3bC(3sf%tX!bDnY+Icu?>D2@XyoEc>G<f%t?4GwH9uP&hx+B81a~OW35HV1BfgKoao`0l6@_dZ0ot7$vraGq4GcxJE<0Eut=ZLvMkr_HF{^4Xubh~nX3ik#rFO<BK&&dkC2VWI1f}3&Sh?U})A{Euh1432OgVj*1dC?rPV3O>3B78iIJZ<B4^ct=K)xX53YiMUuHq?BMx1oIOKhhUih=K^|6-yNs%CeU$e2%;!N^&b?098M3lv{J{1B@IRao6ljs6^*gM@;8FsU1Kp*SGX7EQtySHC6_po5}9JLmo<VV=PM2|HhOagZ!!wki83{*l4kQ#DCRM3>3Z<M?6x*mvOdN50%(}X<;NPiKo!$^Ou~_x<Fb)IL#YE5UXq%DdFb}253a}af+bIdUXneo~B5Y?-QSmaBLfw%q`GKE?>S3GeS;tO=vME|FMHD(Mf46xDBisY{1_RR?_d6*n5FND;N^ZG_+5*h>;@%2(Wa=@-}!j$?pqZ{(~th$4CAxAGsf_lqn;5Y<%Ko^5TYTbkDhlk}RE!x9IN~{&O1?Vl}uFmbZ%cA!!nFPP+gAQ1lLD$KF1F00H<2`!)ao><ndlvBYQl0ssI200dcD"
lang = "en-us"
lang_data = {}
user32 = ctypes.windll.user32
UpdateURL = [
    "http://update.classin-mover.rosa.ink/update.json",
    "https://carlgao4.github.io/ClassIn-Mover/update.json",
]


def has_admin():
    try:
        # only windows users with admin privileges can read the C:\windows\temp
        os.listdir(pathlib.Path(os.environ.get("SystemRoot", "C:\\windows")) / "temp")
    except:
        return os.environ["USERNAME"], False
    else:
        return os.environ["USERNAME"], True


def RestartAsAdmin():
    p = psutil.Process().cmdline()
    return (
        ctypes.windll.shell32.ShellExecuteW(
            0,
            ctypes.create_unicode_buffer("runas"),
            ctypes.create_unicode_buffer(p[0]),
            ctypes.create_unicode_buffer(shlex4all.join(p[1:])),
            0,
            5,
        )
        > 32
    )


if __name__ == "__main__" and not has_admin()[1]:
    if "--no-admin" not in sys.argv and "--startup" not in sys.argv:
        if RestartAsAdmin():
            raise SystemExit
    NoAdmin = True


def GetText(t):
    global lang
    try:
        return lang_data[lang][t]
    except:
        try:
            return lang_data["en-us"][t]
        except:
            return t


def SetLang(TargetLang):
    global lang
    lang = TargetLang
    shared.SetSetting("lang", lang)
    im.delete(1, tkinter.END)
    nm.delete(0, tkinter.END)
    if Notify.not_supported:
        nm.add_command(label=GetText("module can't initialize"), state=tkinter.DISABLED)
    else:
        nm.add_checkbutton(
            label=GetText("Notify in classroom"),
            variable=NotifyInClassroom,
            command=lambda: w.after(100, Notify.set_notify_in_classroom(NotifyInClassroom.get())),
        )
        nm.add_separator()
        for i in Notify.notify_types:
            nm.add_radiobutton(
                label=GetText(Notify[i]), variable=NotifyType, value=i, command=lambda x=i: Notify.set_notify_type(x)
            )
    if NoAdmin:
        im.add_command(label=GetText("Restart as admin"), command=lambda: w.destroy() if RestartAsAdmin() else None)
    im.add_cascade(label=GetText("Enter Alpha"), menu=eam)
    im.add_cascade(label=GetText("Leave Alpha"), menu=lam)
    im.add_cascade(label=GetText("on-stage notify"), menu=nm)
    im.add_checkbutton(label=GetText("Auto patch"), variable=DoAutoPatch, command=SwitchAutoPatchAll)
    im.add_command(
        label=GetText("Patch all"),
        command=lambda: list(AutoPatch(int(i.split(" ", 1)[0])) for i in WindowSelector.cget("values")),
    )
    if (pathlib.Path(__file__).parent / "msi_installed.conf").exists():
        im.add_checkbutton(label=GetText("StartUp"), variable=StartUp, command=lambda: w.after(100, SwitchStartUp))
    im.add_command(label=GetText("Check updates"), command=StartCheckUpdate)
    im.add_command(label=GetText("Exit"), command=w.destroy)

    w.after(100, RefreshPost)
    MinimizeB.config(text=GetText("Minimize"))
    MaximizeB.config(text=GetText("Maximize"))
    NormalB.config(text=GetText("Normalize"))
    FullB.config(text=GetText("Full"))
    TopB.config(text=GetText("Top"))
    NoTopB.config(text=GetText("Cancel Top"))
    SwitchB.config(text=GetText("Switch To"))
    AutoB.config(text=GetText("Auto Patch"))
    WatermarkB.config(text=GetText("Remove Watermark"))
    DragF.config(text=GetText("Move"))
    MoveF.config(text=GetText("Resize"))
    UsageB.config(text=GetText("Usage"))
    BlogB.config(text=GetText("Blogs"))
    WebsiteB.config(text=GetText("Website"))
    ResetB.config(text=GetText("Reset"))
    AboutB.config(text=GetText("About..."))
    ExitB.config(text=GetText("Exit"))

    w.title("ClassIn Mover v" + __version__ + (GetText(" - without Admin") if NoAdmin else ""))
    rw.title(GetText("Remove Watermark"))
    RWL.config(text=GetText("Input watermark"))


@ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
def EnumWindowCallback(hwnd, lParam):
    global ClassInHwnd, ClassInPID, ClassInTitle, run
    TextLen = user32.GetWindowTextLengthW(hwnd)
    text = ctypes.create_unicode_buffer("", TextLen + 20)
    user32.GetWindowTextW(hwnd, text, TextLen + 20)
    Caption = text.value
    if not Caption.startswith("Classroom_"):
        return 1 if run else 0
    pid = struct.pack("l", (0))
    user32.GetWindowThreadProcessId(hwnd, pid)
    pid = struct.unpack("l", pid)[0]
    ProcessHandle = ctypes.windll.kernel32.OpenProcess(0x0410, 0, pid)
    if ProcessHandle == 0:
        return 1 if run else 0
    Name_Buffer = ctypes.create_unicode_buffer("", 260)
    ctypes.windll.psapi.GetModuleFileNameExW(ProcessHandle, 0, Name_Buffer, 260)
    ctypes.windll.kernel32.CloseHandle(ProcessHandle)
    if not Name_Buffer.value.lower().endswith("classin.exe"):
        return 1 if run else 0
    ClassInHwnd.append(hwnd)
    ClassInTitle.append(Caption)
    ClassInPID.append(pid)
    return 1 if run else 0


def GetClassInHwnd():
    global ClassInHwnd, ClassInPID, ClassInTitle
    ClassInHwnd = []
    ClassInTitle = []
    ClassInPID = []
    user32.EnumWindows(EnumWindowCallback, 0)
    return list(zip(ClassInPID, ClassInHwnd, ClassInTitle))


@shared.ShowThread
def ScanWindow():
    global run, afters
    last = set()
    while run:
        try:
            st = time.time()
            CIHwnd = GetClassInHwnd()
            if len(CIHwnd) != 0:
                NewValues = []
                NewSet = set(i[1] for i in CIHwnd)
                if NewSet != last:
                    for i in CIHwnd:
                        NewValues.append(GetText("%d (Title=%s PID=%d)").format(pid=i[0], hwnd=i[1], title=i[2]))
                        if (i[1] not in last) and DoAutoPatch.get():
                            afters.append(w.after(8500, lambda: AutoPatch(hwnd=i[1])))
                    WindowSelector.config(values=NewValues)
                    last = NewSet
                    if not WindowSelector.get() in NewValues:
                        WindowSelector.set(NewValues[0])
                    if len(NewSet) >= 2 and not Notify.not_supported:
                        Notify.warn_multi_windows()
            elif len(WindowSelector.get()) != 0:
                WindowSelector.set("")
                WindowSelector.config(values=[])
            if not Notify.not_supported:
                Notify.detect_and_notify()
        except:
            logging.critical(traceback.format_exc())
        wait = math.ceil(st + 0.001) - time.time()
        time.sleep(wait if wait >= 0 else 0)


def KeepTopmost():
    try:
        if not w.focus_get():
            I.attributes("-topmost", 1)
            w.attributes("-topmost", 1)
    except:
        pass
    w.after(500, KeepTopmost)


def MouseDownI(event):
    global imx, imy, imxr, imyr
    imx = event.x
    imy = event.y
    imxr = event.x_root
    imyr = event.y_root


def MouseMoveI(event):
    I.geometry(f"+{event.x_root - imx}+{event.y_root - imy}")


def MouseUpI(event):
    if imxr == event.x_root and imyr == event.y_root:
        SwitchController()


def MouseDownM(event):
    global mx, my
    mx = event.x_root
    my = event.y_root


def MouseMoveM(event):
    MoveWindow(x=event.x_root - mx, y=event.y_root - my, relative=True)
    user32.SetCursorPos(mx, my)


def MouseMoveR(event):
    MoveWindow(cx=event.x_root - mx, cy=event.y_root - my, relative=True)
    user32.SetCursorPos(mx, my)


def Center():
    if not (hwnd := GetWindow()):
        return
    rect = struct.pack("llll", *([0] * 4))
    user32.GetWindowRect(hwnd, rect)
    rect = struct.unpack("llll", rect)
    user32.MoveWindow(
        hwnd,
        (w.winfo_screenwidth() - rect[2] + rect[0]) // 2,
        (w.winfo_screenheight() - rect[3] + rect[1]) // 2,
        rect[2] - rect[0],
        rect[3] - rect[1],
        1,
    )


def SwitchController():
    global root_shown
    if root_shown:
        w.withdraw()
        root_shown = False
    else:
        place = ""
        if I.winfo_rootx() + 24 <= w.winfo_screenwidth() // 2:
            place += f"+{I.winfo_rootx() + 56}"
        else:
            place += f"+{I.winfo_rootx() - 20 - w.winfo_width()}"
        if I.winfo_rooty() + 24 <= w.winfo_screenheight() // 2:
            place += f"+{max(0, I.winfo_rooty())}"
        else:
            place += f"+{max(0, I.winfo_rooty() - w.winfo_height())}"
        w.geometry(place)
        w.deiconify()
        w.after(100, RefreshPost)
        root_shown = True


def SwitchStartUp():
    shared.SetSetting("startup", StartUp.get())


def GetWindow():
    s = WindowSelector.get()
    if len(s) == 0:
        return 0
    return int(re.findall("^\\d+", s)[0])


def MoveWindow(hwnd=None, sw=None, InsertAfter=None, x=None, y=None, cx=None, cy=None, relative=False):
    if hwnd is None:
        hwnd = GetWindow()
    if not hwnd:
        return
    if sw is not None:
        user32.ShowWindow(hwnd, sw)
    logging.debug(
        {"hwnd": hwnd, "sw": sw, "InsertAfter": InsertAfter, "x": x, "y": y, "cx": cx, "cy": cy, "relative": relative}
    )
    rect = struct.pack("llll", *([0] * 4))
    user32.GetWindowRect(hwnd, rect)
    rect = struct.unpack("llll", rect)
    if not relative:
        logging.debug(
            [
                rect[0] if x is None else x,
                rect[1] if y is None else y,
                max(1, rect[2] - rect[0] if cx is None else cx),
                max(1, rect[3] - rect[1] if cy is None else cy),
            ]
        )
        if InsertAfter is not None:
            user32.SetWindowPos(
                hwnd,
                ctypes.wintypes.HWND(InsertAfter),
                rect[0] if x is None else x,
                rect[1] if y is None else y,
                max(1, rect[2] - rect[0] if cx is None else cx),
                max(1, rect[3] - rect[1] if cy is None else cy),
                (2 if x is None and y is None else 0) + (1 if cx is None and cy is None else 0),
            )
            I.attributes("-topmost", 1)
            w.attributes("-topmost", 1)
        else:
            user32.MoveWindow(
                hwnd,
                rect[0] if x is None else x,
                rect[1] if y is None else y,
                max(1, rect[2] - rect[0] if cx is None else cx),
                max(1, rect[3] - rect[1] if cy is None else cy),
                1,
            )
    else:
        logging.debug(
            [
                rect[0] + (0 if x is None else x),
                rect[1] + (0 if y is None else y),
                max(1, rect[2] - rect[0] + (0 if cx is None else cx)),
                max(1, rect[3] - rect[1] + (0 if cy is None else cy)),
            ]
        )
        if InsertAfter is not None:
            user32.SetWindowPos(
                hwnd,
                ctypes.wintypes.HWND(InsertAfter),
                rect[0] + (0 if x is None else x),
                rect[1] + (0 if y is None else y),
                max(1, rect[2] - rect[0] + (0 if cx is None else cx)),
                max(1, rect[3] - rect[1] + (0 if cy is None else cy)),
                (2 if x is None and y is None else 0) + (1 if cx is None and cy is None else 0),
            )
            I.attributes("-topmost", 1)
            w.attributes("-topmost", 1)
        else:
            user32.MoveWindow(
                hwnd,
                rect[0] + (0 if x is None else x),
                rect[1] + (0 if y is None else y),
                max(1, rect[2] - rect[0] + (0 if cx is None else cx)),
                max(1, rect[3] - rect[1] + (0 if cy is None else cy)),
                1,
            )


def SwitchAutoPatchAll():
    global afters
    if not (a := DoAutoPatch.get()):
        for i in afters:
            w.after_cancel(i)
        afters = []
    shared.SetSetting("autopatchnew", a)


def AutoPatch(hwnd=None):
    if hwnd is None:
        hwnd = GetWindow()
    MoveWindow(hwnd=hwnd, sw=6, InsertAfter=-2)
    w.after(100, lambda: MoveWindow(hwnd=hwnd, sw=3))
    clientarea = struct.pack("llll", *((0,) * 4))
    if user32.SystemParametersInfoW(0x30, 0, clientarea, 0):
        clientarea = struct.unpack("llll", clientarea)
        w.after(
            200,
            lambda: MoveWindow(
                hwnd=hwnd,
                x=clientarea[0],
                y=clientarea[1],
                cx=clientarea[2] - clientarea[0],
                cy=clientarea[3] - clientarea[1],
            ),
        )


def RemoveWatermark():
    if not (pathlib.Path(__file__).parent / "Watermark_Remover.exe").exists():
        if tkinter.messagebox.askyesno(GetText("Error"), GetText("No module")):
            __version__ = "0.0.0"
            threading.Thread(target=CheckUpdate, args=(True, True)).start()
        return
    rw.deiconify()
    w.after(100, lambda: RWL.config(wraplength=Watermark.winfo_width()))
    rw.focus_force()


def StartCheckUpdate():
    global UpdateThread
    if not UpdateThread.is_alive():
        UpdateThread = threading.Thread(target=CheckUpdate, args=(True, False))
        UpdateThread.start()


def HSize(size):
    s = size
    t = 0
    u = ["B", "KB", "MB", "GB", "TB", "PB"]
    while s >= 1024:
        s /= 1024
        t += 1
        if t >= 5:
            break
    return str(round(s, 3)) + u[t]


def DownloadNew(urls, filename, wnd):
    global downloading, Uwidth
    if downloading:
        return
    path = tkinter.filedialog.askdirectory(mustexist=True, title=GetText("Select the folder"))
    if len(path) == 0:
        return
    path = pathlib.Path(path) / filename
    wnd.protocol("WM_DELETE_WINDOW", lambda: None)
    success = False
    i = ""
    j = 0
    status = tkinter.Label(wnd, justify=tkinter.LEFT)
    status.pack(anchor="w")
    Uwidth = 0

    def SetStatus(text):
        global Uwidth
        status.config(text=text)
        if wnd.winfo_width() > Uwidth:
            Uwidth = wnd.winfo_width()
            wnd.minsize(Uwidth, 0)

    def DownloadCallback(n, d, t):
        SetStatus(
            GetText("Download progress").format(
                num=j + 1, url=i, path=str(path), percent=100 * n * d / t, downloaded=HSize(n * d), total=HSize(t)
            )
        )

    for i in urls:
        for j in range(3):
            if j:
                SetStatus(GetText("Retrying").format(url=i, num=j + 1))
            else:
                SetStatus(GetText("Download to").format(url=i, path=path))
            try:
                urllib.request.urlretrieve(i, str(path), DownloadCallback)
            except:
                pass
            else:
                success = True
                break
        if success:
            tkinter.messagebox.showinfo(GetText("Download complete"), GetText("Explanation of completion "))
            w.destroy()
            return
    SetStatus(GetText("Download failed"))
    tkinter.messagebox.showerror(GetText("Download failed"), GetText("New version failed"))
    wnd.protocol("WM_DELETE_WINDOW", wnd.destroy)
    downloading = False


def CheckUpdateFromURL(url):
    if not run:
        return
    try:
        res = urllib.request.urlopen(url)
        return json.loads(res.read())
    except:
        logging.critical(f"Failed to check update from {url}\n" + traceback.format_exc())
        return


@shared.ShowThread
def CheckUpdate(ShowEvenLatest=False, Force=False, func=None, no_blog=False):
    global blogs, lang_data
    NewVersion = None

    U = tkinter.Toplevel(w)
    U.title(GetText("Checking update"))
    U.resizable(False, False)
    U.iconbitmap(str(pathlib.Path(__file__).parent / "ClassIn_Mover.ico"))
    style = user32.GetWindowLongW(int(U.frame(), 16), -16)
    style &= ~0x00020000
    user32.SetWindowLongW(int(U.frame(), 16), -16, style)

    Checking = tkinter.Label(U, text=GetText("Checking update"))
    Checking.pack(padx=(100, 100), pady=(100, 100))
    if Force:
        U.grab_set()
        U.protocol("WM_DELETE_WINDOW", w.destroy)
    else:
        U.withdraw()
        U.protocol("WM_DELETE_WINDOW", w.destroy)
    for i in UpdateURL:
        NewVersion = CheckUpdateFromURL(i)
        if NewVersion is not None:
            break
    if NewVersion is None:
        if run:
            if Force:
                tkinter.messagebox.showerror(GetText("Error"), GetText("NO new version"))
                w.destroy()
            else:
                tkinter.messagebox.showwarning(GetText("Warning"), GetText("NO new version"))
                U.destroy()
                if callable(func):
                    func()
        return
    blogs = NewVersion["blogs"]
    if "post" in NewVersion:
        for key, value in NewVersion["post"].items():
            if key in lang_data:
                lang_data[key]["post"] = value
            else:
                lang_data[key] = {"post": value}
        WindowSelector.grid_configure(pady=(10, 5))
        w.after(100, RefreshPost)
    if NewVersion["version"] > __version__:
        U.title(GetText("New version detected"))
        U.deiconify()
        Checking.destroy()

        UpdateInfo = tkinter.Label(
            U,
            justify=tkinter.LEFT,
            text=GetText("Suggested updates").format(version=NewVersion["version"], features=NewVersion["feature"]),
        )
        UpdateInfo.pack(fill=tkinter.X, anchor="nw", padx=(40, 40), pady=(40, 20))
        UF = tkinter.Frame(U)
        ViewB = tkinter.ttk.Button(UF, text=GetText("View"), command=lambda: webbrowser.open(NewVersion["detail"]))
        DownloadB = tkinter.ttk.Button(
            UF,
            text=GetText("Download"),
            command=lambda: threading.Thread(
                target=DownloadNew, args=(NewVersion["download"], NewVersion["filename"], U)
            ).start(),
        )
        ViewB.grid(row=0, column=0, padx=(0, 10))
        DownloadB.grid(row=0, column=1, padx=(0, 0))
        UF.pack(anchor="e", padx=(0, 40), pady=(0, 40))

        U.focus_force()
    elif ShowEvenLatest:
        U.destroy()
        tkinter.messagebox.showinfo(GetText("Check update"), GetText("Updated"))
    elif len(blogs) != 0:
        NewBlog = False
        ViewedBlog = shared.GetSetting("viewedblog", [])
        for i in blogs:
            if i not in ViewedBlog:
                NewBlog = True
                break
        if NewBlog and not no_blog:
            OpenBlogs()
    if Force:
        U.destroy()
    if callable(func):
        func()


def ResetSettings():
    if tkinter.messagebox.askokcancel(GetText("Reset settings"), GetText("Reset settings description")):
        global reset
        reset = True
        w.destroy()


def SetEnterIconAlpha(a):
    I.unbind("<Enter>")
    I.bind("<Enter>", lambda _: I.attributes("-alpha", a))
    shared.SetSetting("enteralpha", int(a * 100))


def SetLeaveIconAlpha(a):
    I.unbind("<Leave>")
    I.bind("<Leave>", lambda _: I.attributes("-alpha", a))
    shared.SetSetting("leavealpha", int(a * 100))


def RefreshPost():
    Post.config(text=GetText("post"), wraplength=w.winfo_width() - 40)
    Post.grid(row=0, column=0, columnspan=4, padx=(20, 20), pady=(10, 0), sticky="w")


def ViewBlog(blog):
    global blogs
    shared.SetSetting("viewedblog", list(set(shared.GetSetting("viewedblog", [], False) + [blog])))
    webbrowser.open(blogs[blog]["url"] + "?version=" + __version__)


def OpenBlogs():
    global blogs
    if len(blogs) == 0:
        webbrowser.open("https://classin-mover.pages.dev/blogs?version=" + __version__)
        return
    _, BT, _ = ShowText(
        w,
        text="\n".join(blogs[i]["title"] for i in blogs),
        title=GetText("Blogs"),
        model=False,
        font=("微软雅黑", 14),
        width=60,
        height=9,
        spacing1=8,
        spacing2=2,
        background="#fcffff",
        selectbackground="#add6ff",
    )
    ViewedBlog = shared.GetSetting("viewedblog", [])
    for i, blogid in enumerate(blogs):
        tag = "blog%d" % i
        BT.tag_add(tag, "%d.0" % (i + 1), "%d.end" % (i + 1))
        BT.tag_config(tag, underline=True, lmargin1=8, lmargin2=8)
        if blogid in ViewedBlog:
            BT.tag_config(tag, foreground="purple")
        else:
            BT.tag_config(tag, foreground="blue")
        BT.tag_bind(tag, "<Enter>", lambda _: BT.config(cursor="hand2"), "+")
        BT.tag_bind(tag, "<Leave>", lambda _: BT.config(cursor="xterm"), "+")
        BT.tag_bind(tag, "<Button-1>", lambda _, blogid=blogid: ViewBlog(blogid), "+")


def ShowText(master, text="", title="", showscr=True, model=True, width=80, height=15, font=("", 12), **kw):
    TL = tkinter.Toplevel(master)
    TL.attributes("-topmost", True)
    TL.resizable(False, False)
    Text = tkinter.Text(TL, width=width, height=height, font=font, wrap="word", **kw)
    TL.title(title)
    TL.iconbitmap(str(pathlib.Path(__file__).parent / "ClassIn_Mover.ico"))
    TL.bind("<Escape>", lambda _: TL.destroy())
    style = user32.GetWindowLongW(int(TL.frame(), 16), -16)
    style &= ~0x00020000
    user32.SetWindowLongW(int(TL.frame(), 16), -16, style)
    if showscr:
        scr = tkinter.ttk.Scrollbar(TL, orient=tkinter.VERTICAL)
        scr.config(command=Text.yview)
        Text.config(yscrollcommand=scr.set)
        scr.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    Text.insert("0.0", text)
    Text.config(state=tkinter.DISABLED)
    Text.pack(side=tkinter.LEFT, fill=tkinter.Y)
    TL.focus_set()
    if model:
        TL.grab_set()
    return TL, Text, scr


def add_text(self: tkinter.Text, text, pos=tkinter.END, scr=None):
    try:
        end = scr.get()[-1] == 1.0
    except:
        end = False
    self.config(state=tkinter.NORMAL)
    self.insert(pos, text)
    self.config(state=tkinter.DISABLED)
    if end:
        self.see(tkinter.END)


if __name__ == "__main__":
    if not "--stderr-log" in sys.argv:
        LogFolder = pathlib.Path.home() / "AppData" / "Local" / "ClassIn-Mover" / "log"
        LogFolder.mkdir(parents=True, exist_ok=True)
        log = open(
            str(LogFolder / datetime.datetime.now().strftime("ClassIn-Mover-Log-%Y%m%d-%H%M%S.log")),
            mode="wt",
            encoding="utf8",
        )
        sys.stderr = log
    else:
        log = sys.stderr
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s (%(funcName)s %(lineno)d) %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=(logging.StreamHandler(log),),
    )

    if "--startup" in sys.argv and not shared.GetSetting("startup", False):
        raise SystemExit

    lang = shared.GetSetting("lang", locale.getdefaultlocale()[0].lower().replace("_", "-"))

    logging.info("ClassIn Mover version: " + __version__)
    logging.info("Python version: " + sys.version)
    logging.info(platform.platform())

    for i in os.listdir(str(pathlib.Path(__file__).parent / "lang")):
        if not i.endswith(".json"):
            continue
        try:
            langname = i.rsplit(".", 1)[0]
            with open(pathlib.Path(__file__).parent / "lang" / i, encoding="utf8", mode="rt") as f:
                lang_data[langname] = json.loads(f.read())
            lang_data[langname]["LangName"]
        except:
            logging.critical(f"Read file {i} failed\n" + traceback.format_exc())
            if langname in lang_data:
                del lang_data[langname]

    w = tkinter.Tk()
    w.resizable(False, False)
    w.title("ClassIn Mover v" + __version__ + (GetText(" - without Admin") if NoAdmin else ""))
    w.iconbitmap(str(pathlib.Path(__file__).parent / "ClassIn_Mover.ico"))
    w.attributes("-topmost", 1)
    w.protocol("WM_DELETE_WINDOW", SwitchController)
    root_shown = False

    style = user32.GetWindowLongW(int(w.frame(), 16), -16)
    style &= ~0x00020000
    user32.SetWindowLongW(int(w.frame(), 16), -16, style)

    w.withdraw()

    Post = tkinter.ttk.Label(w)
    WindowSelector = tkinter.ttk.Combobox(w, width=56, state="readonly")
    MinimizeB = tkinter.ttk.Button(w, text=GetText("Minimize"), command=lambda: MoveWindow(sw=6))
    MaximizeB = tkinter.ttk.Button(w, text=GetText("Maximize"), command=lambda: MoveWindow(sw=3))
    NormalB = tkinter.ttk.Button(w, text=GetText("Normalize"), command=lambda: MoveWindow(sw=1))
    FullB = tkinter.ttk.Button(
        w,
        text=GetText("Full"),
        command=lambda: MoveWindow(x=0, y=0, cx=w.winfo_screenwidth(), cy=w.winfo_screenheight()),
    )
    TopB = tkinter.ttk.Button(w, text=GetText("Top"), command=lambda: MoveWindow(InsertAfter=-1))
    NoTopB = tkinter.ttk.Button(w, text=GetText("Cancel Top"), command=lambda: MoveWindow(InsertAfter=-2))
    SwitchB = tkinter.ttk.Button(
        w,
        text=GetText("Switch To"),
        command=lambda: (user32.SetForegroundWindow(GetWindow()) if GetWindow() else None),
    )
    AutoB = tkinter.ttk.Button(w, text=GetText("Auto Patch"), command=AutoPatch)
    WatermarkB = tkinter.ttk.Button(w, text=GetText("Remove Watermark"), command=RemoveWatermark)
    DragF = tkinter.LabelFrame(
        w,
        width=192,
        height=108,
        bd=0,
        bg="#cccccc",
        labelanchor="n",
        text=GetText("Move"),
    )
    MoveF = tkinter.LabelFrame(
        w,
        width=192,
        height=108,
        bd=0,
        bg="#cccccc",
        labelanchor="n",
        text=GetText("Resize"),
    )
    UsageB = tkinter.ttk.Button(
        w,
        text=GetText("Usage"),
        command=lambda: webbrowser.open("https://classin-mover.pages.dev/usage?version=" + __version__),
    )
    BlogB = tkinter.ttk.Button(w, text=GetText("Blogs"), command=OpenBlogs)
    WebsiteB = tkinter.ttk.Button(
        w,
        text=GetText("Website"),
        command=lambda: webbrowser.open("https://classin-mover.pages.dev/app?version=" + __version__),
    )
    ResetB = tkinter.ttk.Button(w, text=GetText("Reset"), command=ResetSettings)
    AboutB = tkinter.ttk.Button(
        w,
        text=GetText("About..."),
        command=lambda: ShowText(w, title=GetText("About ") + __version__, text=LICENSE),
    )
    ExitB = tkinter.ttk.Button(w, text=GetText("Exit"), command=w.destroy)

    WindowSelector.grid(row=1, column=0, columnspan=4, padx=(20, 20), pady=(20, 5))
    MinimizeB.grid(row=2, column=0, padx=(20, 5), pady=(5, 5))
    MaximizeB.grid(row=2, column=1, padx=(5, 5), pady=(5, 5))
    NormalB.grid(row=2, column=2, padx=(5, 5), pady=(5, 5))
    FullB.grid(row=2, column=3, padx=(5, 20), pady=(5, 5))
    TopB.grid(row=3, column=0, padx=(20, 5), pady=(5, 5))
    NoTopB.grid(row=3, column=1, padx=(5, 5), pady=(5, 5))
    SwitchB.grid(row=3, column=2, padx=(5, 5), pady=(5, 5))
    AutoB.grid(row=3, column=3, padx=(5, 20), pady=(5, 5))
    WatermarkB.grid(row=4, column=0, columnspan=4, padx=(20, 20), pady=(5, 5))
    DragF.grid(row=5, column=0, columnspan=2, padx=(20, 5), pady=(5, 5))
    MoveF.grid(row=5, column=2, columnspan=2, padx=(5, 20), pady=(5, 5))
    UsageB.grid(row=6, column=1, padx=(5, 5), pady=(5, 5))
    BlogB.grid(row=6, column=2, padx=(5, 5), pady=(5, 5))
    WebsiteB.grid(row=6, column=3, padx=(5, 20), pady=(5, 5))
    ResetB.grid(row=7, column=1, padx=(5, 5), pady=(5, 20))
    AboutB.grid(row=7, column=2, padx=(5, 5), pady=(5, 20))
    ExitB.grid(row=7, column=3, padx=(5, 20), pady=(5, 20))

    DragF.bind("<ButtonPress-1>", MouseDownM)
    DragF.bind("<B1-Motion>", MouseMoveM)
    DragF.bind("<Double-Button-1>", lambda _: Center())
    MoveF.bind("<ButtonPress-1>", MouseDownM)
    MoveF.bind("<B1-Motion>", MouseMoveR)
    MoveF.bind("<Double-Button-1>", lambda _: MoveWindow(cx=w.winfo_screenwidth(), cy=w.winfo_screenheight()))
    I = tkinter.Toplevel()
    I.overrideredirect(True)
    I.geometry("48x48+96+96")
    I.resizable(False, False)
    DoAutoPatch = tkinter.BooleanVar(I, value=shared.GetSetting("autopatchnew", True))
    im = tkinter.Menu(I, tearoff=False)
    lm = tkinter.Menu(im, tearoff=False)
    for i in lang_data:
        lm.add_command(label=lang_data[i]["LangName"], command=lambda x=i: SetLang(x))
    EnterAlpha = tkinter.IntVar(I, value=shared.GetSetting("enteralpha", 70))
    eam = tkinter.Menu(im, tearoff=False)
    for i in range(30, 101, 5):
        eam.add_radiobutton(
            label="%d%%" % i, value=i, variable=EnterAlpha, command=lambda a=i: SetEnterIconAlpha(a / 100)
        )
    LeaveAlpha = tkinter.IntVar(I, value=shared.GetSetting("leavealpha", 30))
    lam = tkinter.Menu(im, tearoff=False)
    for i in range(30, 101, 5):
        lam.add_radiobutton(
            label="%d%%" % i, value=i, variable=LeaveAlpha, command=lambda a=i: SetLeaveIconAlpha(a / 100)
        )
    nm = tkinter.Menu(im, tearoff=False)
    NotifyType = tkinter.IntVar(I, value=shared.GetSetting("on-stage notify", 0))
    NotifyInClassroom = tkinter.BooleanVar(I, value=shared.GetSetting("notify-in-classroom", False))
    Notify = onstage_notify.on_stage_notify(NotifyType.get(), NotifyInClassroom.get(), GetText, WindowSelector)
    if Notify.not_supported:
        nm.add_command(label=GetText("module can't initialize"), state=tkinter.DISABLED)
    else:
        nm.add_checkbutton(
            label=GetText("Notify in classroom"),
            variable=NotifyInClassroom,
            command=lambda: Notify.set_notify_in_classroom(NotifyInClassroom.get()),
        )
        nm.add_separator()
        for i in Notify.notify_types:
            nm.add_radiobutton(
                label=GetText(Notify[i]), variable=NotifyType, value=i, command=lambda x=i: Notify.set_notify_type(x)
            )
    StartUp = tkinter.BooleanVar(I, value=shared.GetSetting("startup", False))

    im.add_cascade(label="Language", menu=lm)
    if NoAdmin:
        im.add_command(label=GetText("Restart as admin"), command=lambda: w.destroy() if RestartAsAdmin() else None)
    im.add_cascade(label=GetText("Enter Alpha"), menu=eam)
    im.add_cascade(label=GetText("Leave Alpha"), menu=lam)
    im.add_cascade(label=GetText("on-stage notify"), menu=nm)
    im.add_checkbutton(label=GetText("Auto patch"), variable=DoAutoPatch, command=SwitchAutoPatchAll)
    im.add_command(
        label=GetText("Patch all"),
        command=lambda: list(AutoPatch(int(i.split(" ", 1)[0])) for i in WindowSelector.cget("values")),
    )
    if (pathlib.Path(__file__).parent / "msi_installed.conf").exists():
        im.add_checkbutton(label=GetText("StartUp"), variable=StartUp, command=lambda: w.after(100, SwitchStartUp))
    im.add_command(label=GetText("Check updates"), command=StartCheckUpdate)
    im.add_command(label=GetText("Exit"), command=w.destroy)

    img = pickle.loads(lzma.decompress(base64.b85decode(icon)))
    imgTk = PIL.ImageTk.PhotoImage(img)
    il = tkinter.Label(I, bd=0, image=imgTk)
    il.place(x=0, y=0)
    I.protocol("WM_DELETE_WINDOW", lambda: None)
    I.attributes("-topmost", 1)
    I.attributes("-alpha", shared.GetSetting("enteralpha", 70) / 100)
    I.attributes("-transparentcolor", "#ff0000")
    I.bind("<Enter>", lambda _: I.attributes("-alpha", shared.GetSetting("enteralpha", 70) / 100))
    I.bind("<Leave>", lambda _: I.attributes("-alpha", shared.GetSetting("leavealpha", 30) / 100))
    I.bind("<ButtonPress-1>", MouseDownI)
    I.bind("<B1-Motion>", MouseMoveI)
    I.bind("<ButtonRelease-1>", MouseUpI)
    I.bind("<Button-3>", lambda e: im.tk_popup(e.x_root, e.y_root))

    rw = tkinter.Toplevel(w)
    rw.title(GetText("Remove Watermark"))
    rw.resizable(False, False)
    rw.iconbitmap(str(pathlib.Path(__file__).parent / "ClassIn_Mover.ico"))
    rw.attributes("-topmost", 1)
    rw.protocol("WM_DELETE_WINDOW", rw.withdraw)
    style = user32.GetWindowLongW(int(rw.frame(), 16), -16)
    style &= ~0x00020000
    user32.SetWindowLongW(int(rw.frame(), 16), -16, style)
    RWL = tkinter.ttk.Label(rw, text=GetText("Input watermark"))
    RWL.pack(anchor="w", padx=(20, 20), pady=(20, 5))
    Watermark = tkinter.ttk.Combobox(rw, width=40, values=shared.GetSetting("watermarks", []), font=("微软雅黑", 10))
    Watermark.pack(anchor="w", padx=(20, 20), pady=(5, 5))
    w.after(100, lambda: RWL.config(wraplength=Watermark.winfo_width()))
    TryRemoveB = tkinter.ttk.Button(rw, text=GetText("Try remove"))
    TryRemoveB.pack(pady=(5, 5))
    RWF = tkinter.ttk.Frame(rw)
    RWT = tkinter.Text(RWF, width=40, height=8, font=("微软雅黑", 10), wrap="word")
    RWscr = tkinter.ttk.Scrollbar(RWF, orient=tkinter.VERTICAL)
    RWscr.config(command=RWT.yview)
    RWT.config(yscrollcommand=RWscr.set)
    RWT.pack(fill=tkinter.Y, side=tkinter.LEFT)
    RWscr.pack(fill=tkinter.Y, side=tkinter.RIGHT)
    RWF.pack(padx=(20, 20), pady=(5, 20))
    rw.withdraw()

    try:
        from Remove_Watermark import WatermarkRemover
    except:
        StartRemove = lambda: add_text(RWT, "Remove watermark module not found\n", scr=RWscr)
    else:
        StartRemove = WatermarkRemover(Watermark, RWT, GetText, RWscr, WindowSelector).StartRemove

    TryRemoveB.config(command=StartRemove)
    Watermark.bind("<Return>", lambda _: StartRemove())

    ScanThread = threading.Thread(target=ScanWindow)
    ScanThread.start()

    UpdateThread = threading.Thread(target=CheckUpdate, kwargs={"no_blog": True} if "--startup" in sys.argv else {})
    UpdateThread.start()

    w.after(500, KeepTopmost)

    try:
        w.mainloop()
    except KeyboardInterrupt:
        pass
    logging.debug("Main window destroyed")
    run = False
    if reset:
        os.remove(str(shared.SettingsFile))
    sys.exit(0)
