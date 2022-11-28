LICENSE = """ClassIn Mover - A program to move ClassIn classroom window in order to exit from focused learning mode.
Visit https://carlgao4.github.io/ClassIn-Mover for more information. 

Copyright (C) 2020-2022  Weiqi Gao, Jize Guo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""

__version__ = "2.1.0.1"

import tkinter
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
import ctypes
import ctypes.wintypes
import struct
import time
import datetime
import math
import threading
import sys
import os
import platform
import locale
import shlex4all
import psutil
import PIL
import PIL.Image
import PIL.ImageTk
import pathlib
import pickle
import zlib
import base64
import urllib
import urllib.request
import json
import webbrowser
import logging

ClassInHwnd = []
ClassInTitle = []
ClassInPID = []
run = True
NoAdmin = False
downloading = False
icon = "c-rllZA=q)9LG^vra)9$9)zMi$wMi9rnIz_KG0Iy0s<wnk%@@wY88-y7~E7~iwFv)NUPDPyx7=YxoM0L!%V<;>I`Itn8mm#V=s)^1mnzNWbC^;X>O&ID|2&M{N`w`$Mt@n`#t@Ccddc0dR73TE=IAjfTyjkH`Z>mS&M6$Z1y^5SBTDDO&rLx*I1psPIjAfi!=3rGqr2Q`}KCGA>gIlJMGS{;O)C>>l>_%jrQGjPIEw0*NReu)@c@)1?|ovZ2;`ezS-VvuXg))<PS_?VWC2yP^nZoIXOzD68mzwTq>1jW@ct&WQar}p-{-@^Lad8dU|?VT3TvqYD!8<Qc_Z4Vq$!Jd|X`Ih7B9muV2q%v7(}))~#C?85tQC7RF#Of`WpWOr{@5v$NUR+4=eTX0zF7G-4+&FHf)6=jP^WwOX}WO(m4cWFVACBx11`kOF}Kgj_C{!{JaNH*VaRkdOe#*w|P=f-Qi&aeB^yU4LQVuK6&@$;qV000XCyFflPP(b3Us*RG}IqS;xJ#AGrp1OxApFbE&jGYFp>hRtS^Fr;TZU`Ww&5#gMCLQ4pfM=p7UiG*Rzi9V0PU|19eS?%E&Hw@J??!@+hq0fVw(i5V>AVz@6%F3GW8ETjo@(iq#F<Jr-tb;_S(`hsszyOc*%zPN+@S<UYbG*XP=YcD<gci*iub%N*O)PJs$ph<ZLVoobkDT!lCVzQg+M_Kmt?9W-o3(&w@}R3I3H|-1=L3d54@`r^-Sm9qjMt_ILs+LmLqi$fgoVss9yAt|5(xtmn4>O^_=Hcqh6(=)2?<%VW)0Tj^78UBLKcgqw6wIOq@=jGxU#Ym9(E(q<bfY#ga8IdO;1lhdGh3ELfF4}@gm{{(;f*7D}d?i>+>;RjE#-q9Cr|D^57Q8xdP5XXb`yhS4IQJ8tsM&4-d!Z^XJcfzzhrwEL*k=vxmR&LWW2PkvW4T0h`rott135k=I89N1gx!!wfv;Vg2dTr@zi=W@hHnrAr<#^m*VDF(G#XBU{MwL72cWF)=|J#S8%d;{+;6cX#*l<;!7fIYp~hty*$_M(v0Qc`a=e5k{BE$w{0!Iy#Cxr^485Hdy!Y11a~I;V%zNd+jssYC=)3UcI`%zaQ?R!l0~R;_W#_L_|<wFtlQ$BGKf5X>u_3(e%(>07iv*`0(L{3l~O4MuvxnuU)%#_wHS+I6xvuqHqhGbX-%21r}dPB$_<%1DDW3O%E5u0O0%4p}D!4ENz@jw6Da%O%)2Ik;CD+k!bS3G)R1m5V&i!xP?d_Ja~ZIBNG_HPvYW}6iU-CkEie5yU*dt;V4`LNHlp6lr%y<COvfiz`($onwl$Dt{^ny<Ku&agD#f~S%>4OK{97zVpz#398K<~XU~3nNjotq$;{;o#Pt1xh@=woJ?Y^FQD`eyu6&CSb`T&mMt2?I1U!dv`HItL`Y&G|y7$BVv9a3&16SKSdKKAuxHFnOFr7k({-o!vuA`!fB+==ODph`Rim0va$U7BQp;)QWm<kFuq1I^fz-|&D`jg&Y>lz6ho66>jGB9#yM@B}#v`8#D(&e=8Y{FoLuQ-^MrHGABqr(H!An|L`qr&|8tQ?<YG;gk~sxz63!o!hGOg>L|l;Dxe75I*WQkkl8Z=2p=S(FD?P9Q{o(sR?|7jbb(Sqj687c=`lZrAHgs8dv{P$W6jer#KHom!(MYB!xPkbT~N{?486v$FGj^N=0GuSw6%!)9~y^2<=#xXu?}o-eUfZr!#ETdAe;tFJHj96wc7UcIHtzGbVupy=Iiu8!ce>({?E7|VR{puNNrq7O626UF6aH0(J@miCPsx4Ms=aJtU+y3TfWpBNpzJv20YwA<x4e%j$U)zRtr?)Lc1%!|n%e=4<XJ=gb{kNP6#KspKR;U83GTs*s~x)#@I+S?{qXmeEB9HmAimbbKZR=j6ZYxGK`My1lGurtn_>wom<kuI;arM2Dn`wh&Te!)=l8I3C;F|DqC--nH@sOt!{r0_6-Ky<jX$F`#p(_J`m1o_<2*;`mt(e}yVMN>K`C<q<cUmhwFUm%r8btZEGOf#7bK3~}0;Q)^U^~GdjIYx%-4P_l2$7sF+!b*Y8AF?C`2M044p;#<nS0uvILAF3BJ=oHLc&XGnsZ1f2%KUg=_v+psI-R|0ZP5oins(JT4-5{S>+9cDyRU5X_J+p&uj|#Q!*SBSa}PoHJN~8~Kem)rIeJ{L@onu#`#;6XH8nMbDHm(~;tBlEZ~G4%vh8Rvn#)^S5B*2pY4;pIdGqG2H}CfUf1A@<&HDox^xKy"
lang = "en-us"
lang_data = {}


def has_admin():
    try:
        # only windows users with admin privileges can read the C:\windows\temp
        os.listdir(pathlib.Path(os.environ.get("SystemRoot", "C:\\windows")) / "temp")
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
        ctypes.create_unicode_buffer(shlex4all.join(p[1:])),
        0,
        5,
    )
    if res > 32:
        raise SystemExit
    NoAdmin = True


def GetText(t):
    global lang
    if lang == "en-us":
        return t
    try:
        return lang_data[lang][t]
    except:
        return t


def SetLang(targetlang):
    global lang
    lang = targetlang
    im.delete(1, tkinter.END)
    im.add_checkbutton(label=GetText("Auto patch new window"), variable=DoAutoPatch)
    im.add_command(
        label=GetText("Patch all"),
        command=lambda: list(AutoPatch(int(i.split(" ", 1)[0])) for i in WindowSelector.cget("values")),
    )
    im.add_command(label=GetText("Check updates"), command=startCheckUpdate)
    im.add_command(label=GetText("Exit"), command=w.destroy)

    MinimizeB.config(text=GetText("Minimize"))
    MaximizeB.config(text=GetText("Maximize"))
    NormalB.config(text=GetText("Normalize"))
    FullB.config(text=GetText("Full Screen"))
    TopB.config(text=GetText("Topmost"))
    NoTopB.config(text=GetText("No Topmost"))
    SwitchB.config(text=GetText("Switch To"))
    AutoB.config(text=GetText("Auto Patch"))
    DragF.config(text=GetText("Drag to move ClassIn window\nDouble click: move to center"))
    MoveF.config(text=GetText("Drag to resize ClassIn window\nDouble click: screen size"))
    WebsiteB.config(text=GetText("Website"))
    AboutB.config(text=GetText("About..."))
    ExitB.config(text=GetText("Exit"))

    w.title("ClassIn Mover v" + __version__ + (GetText(" - without Admin") if NoAdmin else ""))


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


def ScanWindow():
    global run
    last = set()
    count = 0
    while run:
        try:
            st = time.time()
            if not w.focus_get():
                I.attributes("-topmost", 1)
                w.attributes("-topmost", 1)
            count += 1
            CIHwnd = GetClassInHwnd()
            if len(CIHwnd) != 0:
                newvalues = []
                newset = set(i[1] for i in CIHwnd)
                if newset != last:
                    for i in CIHwnd:
                        newvalues.append(GetText("%d (Title=%s PID=%d)") % (i[1], i[2], i[0]))
                        if (i[1] not in last) and DoAutoPatch.get():
                            w.after(8500, lambda: AutoPatch(hwnd=i[1]))
                    WindowSelector.config(values=newvalues)
                    last = newset
                    if not WindowSelector.get() in newvalues:
                        WindowSelector.set(newvalues[0])
            elif len(WindowSelector.get()) != 0:
                WindowSelector.set("")
                WindowSelector.config(values=[])
            wait = math.ceil(st) - time.time()
            time.sleep(wait if wait >= 0 else 0)
        except:
            return


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
    ctypes.windll.user32.SetCursorPos(mx, my)


def MouseMoveR(event):
    MoveWindow(cx=event.x_root - mx, cy=event.y_root - my, relative=True)
    ctypes.windll.user32.SetCursorPos(mx, my)


def Center():
    if not (hwnd := GetWindow()):
        return
    rect = struct.pack("llll", *([0] * 4))
    ctypes.windll.user32.GetWindowRect(hwnd, rect)
    rect = struct.unpack("llll", rect)
    ctypes.windll.user32.MoveWindow(
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
        w.deiconify()
        root_shown = True


def GetWindow():
    s = WindowSelector.get()
    if len(s) == 0:
        return 0
    return int(s.split(" ", 1)[0])


def MoveWindow(hwnd=None, sw=None, InsertAfter=None, x=None, y=None, cx=None, cy=None, relative=False):
    if hwnd is None:
        hwnd = GetWindow()
    if not hwnd:
        return
    if sw is not None:
        ctypes.windll.user32.ShowWindow(hwnd, sw)
    if not relative:
        if InsertAfter is not None:
            rect = struct.pack("llll", *([0] * 4))
            ctypes.windll.user32.GetWindowRect(hwnd, rect)
            rect = struct.unpack("llll", rect)
            ctypes.windll.user32.SetWindowPos(
                hwnd,
                ctypes.wintypes.HWND(InsertAfter),
                rect[0] if x is None else x,
                rect[1] if y is None else y,
                rect[2] - rect[0] if cx is None else cx,
                rect[3] - rect[1] if cy is None else cy,
                (2 if x is None and y is None else 0) + (1 if cx is None and cy is None else 0),
            )
            I.attributes("-topmost", 1)
            w.attributes("-topmost", 1)
        else:
            rect = struct.pack("llll", *([0] * 4))
            ctypes.windll.user32.GetWindowRect(hwnd, rect)
            rect = struct.unpack("llll", rect)
            ctypes.windll.user32.MoveWindow(
                hwnd,
                rect[0] if x is None else x,
                rect[1] if y is None else y,
                rect[2] - rect[0] if cx is None else cx,
                rect[3] - rect[1] if cy is None else cy,
                1,
            )
    else:
        if InsertAfter is not None:
            rect = struct.pack("llll", *([0] * 4))
            ctypes.windll.user32.GetWindowRect(hwnd, rect)
            rect = struct.unpack("llll", rect)
            ctypes.windll.user32.SetWindowPos(
                hwnd,
                ctypes.wintypes.HWND(InsertAfter),
                rect[0] + (0 if x is None else x),
                rect[1] + (0 if y is None else y),
                rect[2] - rect[0] + (0 if cx is None else cx),
                rect[3] - rect[1] + (0 if cy is None else cy),
                (2 if x is None and y is None else 0) + (1 if cx is None and cy is None else 0),
            )
            I.attributes("-topmost", 1)
            w.attributes("-topmost", 1)
        else:
            rect = struct.pack("llll", *([0] * 4))
            ctypes.windll.user32.GetWindowRect(hwnd, rect)
            rect = struct.unpack("llll", rect)
            ctypes.windll.user32.MoveWindow(
                hwnd,
                rect[0] + (0 if x is None else x),
                rect[1] + (0 if y is None else y),
                rect[2] - rect[0] + (0 if cx is None else cx),
                rect[3] - rect[1] + (0 if cy is None else cy),
                1,
            )


def AutoPatch(hwnd=None):
    if hwnd is None:
        hwnd = GetWindow()
    MoveWindow(hwnd=hwnd, sw=6, InsertAfter=-2)
    w.after(100, lambda: MoveWindow(hwnd=hwnd, sw=3))
    clientarea = struct.pack("llll", *((0,) * 4))
    if ctypes.windll.user32.SystemParametersInfoW(0x30, 0, clientarea, 0):
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


def startCheckUpdate():
    global UpdateThread
    if not UpdateThread.is_alive():
        UpdateThread = threading.Thread(target=CheckUpdate, args=(True,))
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
    path = tkinter.filedialog.askdirectory(mustexist=True, title=GetText("Choose a folder to save the new version"))
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

    def setstatus(text):
        global Uwidth
        status.config(text=text)
        if wnd.winfo_width() > Uwidth:
            Uwidth = wnd.winfo_width()
            wnd.minsize(Uwidth, 0)

    def DownloadCallback(n, d, t):
        setstatus(
            GetText("(%d) Downloading %s to %s ... %.1f%% (%s/%s)")
            % (j + 1, i, path, 100 * n * d / t, HSize(n * d), HSize(t))
        )

    for i in urls:
        for j in range(3):
            if j:
                setstatus(GetText("Failed to download %s , retrying (%d)") % (i, j + 1))
            else:
                setstatus(GetText("Downloading %s to %s ...") % (i, path))
            try:
                urllib.request.urlretrieve(i, str(path), DownloadCallback)
            except:
                pass
            else:
                success = True
                break
        if success:
            tkinter.messagebox.showinfo(
                GetText("Download complete"), GetText("Download completed. Please open the latest version. ")
            )
            psutil.Process().terminate()
            return
    setstatus(GetText("Failed to download"))
    tkinter.messagebox.showerror(GetText("Download failed"), GetText("Failed to download the latest version. "))
    wnd.protocol("WM_DELETE_WINDOW", wnd.destroy)
    downloading = False


def CheckUpdate(ShowEvenLatest=False):
    try:
        res = urllib.request.urlopen("https://carlgao4.github.io/ClassIn-Mover/update.json")
        newversion = json.loads(res.read())
    except:
        if run:
            tkinter.messagebox.showwarning(GetText("Warning"), GetText("Failed to detect new version. "))
        return
    if newversion["version"] > __version__:
        U = tkinter.Toplevel(w)
        U.title(GetText("New version detected"))
        U.resizable(False, False)
        U.iconbitmap(str(pathlib.Path(__file__).parent / "ClassIn_Mover.ico"))
        U.grab_set()
        style = ctypes.windll.user32.GetWindowLongW(int(U.frame(), 16), -16)
        style &= ~0x00020000
        ctypes.windll.user32.SetWindowLongW(int(U.frame(), 16), -16, style)

        UpdateInfo = tkinter.Label(
            U,
            justify=tkinter.LEFT,
            text=GetText("New version %s detected\nFeatures:\n%s\n\nWe suggest you to update now. ")
            % (newversion["version"], newversion["feature"]),
        )
        UpdateInfo.pack(fill=tkinter.X, anchor="nw", padx=(40, 40), pady=(40, 20))
        UF = tkinter.Frame(U)
        ViewB = tkinter.ttk.Button(UF, text=GetText("View"), command=lambda: webbrowser.open(newversion["detail"]))
        DownloadB = tkinter.ttk.Button(
            UF,
            text=GetText("Download"),
            command=lambda: threading.Thread(
                target=DownloadNew, args=(newversion["download"], newversion["filename"], U)
            ).start(),
        )
        ViewB.grid(row=0, column=0, padx=(0, 10))
        DownloadB.grid(row=0, column=1, padx=(0, 0))
        UF.pack(anchor="e", padx=(0, 40), pady=(0, 40))

        U.focus_force()
    elif ShowEvenLatest:
        tkinter.messagebox.showinfo(
            GetText("Check update"), GetText("You are using the latest version of ClassIn Mover")
        )


def ShowText(
    master, text="", title="", showscr=True, model=True, width=80, height=15, font=("", 12), justify=tkinter.LEFT
):
    TL = tkinter.Toplevel(master)
    TL.attributes("-topmost", True)
    TL.resizable(False, False)
    Text = tkinter.Text(TL, width=width, height=height, font=font, wrap="word")
    TL.title(title)
    TL.iconbitmap(str(pathlib.Path(__file__).parent / "ClassIn_Mover.ico"))
    style = ctypes.windll.user32.GetWindowLongW(int(TL.frame(), 16), -16)
    style &= ~0x00020000
    ctypes.windll.user32.SetWindowLongW(int(TL.frame(), 16), -16, style)
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


if __name__ == "__main__":
    logfolder = pathlib.Path.home() / "AppData" / "Local" / "ClassIn-Mover" / "log"
    logfolder.mkdir(parents=True, exist_ok=True)
    log = open(
        str(logfolder / datetime.datetime.now().strftime("ClassIn-Mover-Log-%Y%m%d-%H%M%S.log")),
        mode="wt",
        encoding="utf8",
    )
    sys.stderr = log
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s (%(funcName)s %(lineno)d) %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=(logging.StreamHandler(log),),
    )

    logging.info("ClassIn Mover version: " + __version__)
    logging.info("Python version: " + sys.version)
    logging.info(platform.platform())

    w = tkinter.Tk()
    w.resizable(False, False)
    w.title("ClassIn Mover v" + __version__ + (GetText(" - without Admin") if NoAdmin else ""))
    w.iconbitmap(str(pathlib.Path(__file__).parent / "ClassIn_Mover.ico"))
    w.attributes("-topmost", 1)
    w.protocol("WM_DELETE_WINDOW", SwitchController)
    root_shown = False

    style = ctypes.windll.user32.GetWindowLongW(int(w.frame(), 16), -16)
    style &= ~0x00020000
    ctypes.windll.user32.SetWindowLongW(int(w.frame(), 16), -16, style)

    w.withdraw()

    WindowSelector = tkinter.ttk.Combobox(w, width=56, state="readonly")
    MinimizeB = tkinter.ttk.Button(w, text=GetText("Minimize"), command=lambda: MoveWindow(sw=6))
    MaximizeB = tkinter.ttk.Button(w, text=GetText("Maximize"), command=lambda: MoveWindow(sw=3))
    NormalB = tkinter.ttk.Button(w, text=GetText("Normalize"), command=lambda: MoveWindow(sw=1))
    FullB = tkinter.ttk.Button(
        w,
        text=GetText("Full Screen"),
        command=lambda: MoveWindow(x=0, y=0, cx=w.winfo_screenwidth(), cy=w.winfo_screenheight()),
    )
    TopB = tkinter.ttk.Button(w, text=GetText("Topmost"), command=lambda: MoveWindow(InsertAfter=-1))
    NoTopB = tkinter.ttk.Button(w, text=GetText("No Topmost"), command=lambda: MoveWindow(InsertAfter=-2))
    SwitchB = tkinter.ttk.Button(
        w,
        text=GetText("Switch To"),
        command=lambda: (ctypes.windll.user32.SetForegroundWindow(GetWindow()) if GetWindow() else None),
    )
    AutoB = tkinter.ttk.Button(w, text=GetText("Auto Patch"), command=AutoPatch)
    DragF = tkinter.LabelFrame(
        w,
        width=192,
        height=108,
        bd=0,
        bg="#cccccc",
        labelanchor="n",
        text=GetText("Drag to move ClassIn window\nDouble click: move to center"),
    )
    MoveF = tkinter.LabelFrame(
        w,
        width=192,
        height=108,
        bd=0,
        bg="#cccccc",
        labelanchor="n",
        text=GetText("Drag to resize ClassIn window\nDouble click: screen size"),
    )
    WebsiteB = tkinter.ttk.Button(
        w,
        text=GetText("Website"),
        command=lambda: webbrowser.open("https://carlgao4.github.io/ClassIn-Mover/app?version=" + __version__),
    )
    AboutB = tkinter.ttk.Button(
        w,
        text=GetText("About..."),
        command=lambda: ShowText(w, title=GetText("About ClassIn Mover ") + __version__, text=LICENSE),
    )
    ExitB = tkinter.ttk.Button(w, text=GetText("Exit"), command=w.destroy)

    WindowSelector.grid(row=0, column=0, columnspan=4, padx=(20, 20), pady=(20, 5))
    MinimizeB.grid(row=1, column=0, padx=(20, 5), pady=(5, 5))
    MaximizeB.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))
    NormalB.grid(row=1, column=2, padx=(5, 5), pady=(5, 5))
    FullB.grid(row=1, column=3, padx=(5, 20), pady=(5, 5))
    TopB.grid(row=2, column=0, padx=(20, 5), pady=(5, 5))
    NoTopB.grid(row=2, column=1, padx=(5, 5), pady=(5, 5))
    SwitchB.grid(row=2, column=2, padx=(5, 5), pady=(5, 5))
    AutoB.grid(row=2, column=3, padx=(5, 20), pady=(5, 5))
    DragF.grid(row=3, column=0, columnspan=2, padx=(20, 5), pady=(5, 5))
    MoveF.grid(row=3, column=2, columnspan=2, padx=(5, 20), pady=(5, 5))
    WebsiteB.grid(row=4, column=1, padx=(5, 5), pady=(5, 20))
    AboutB.grid(row=4, column=2, padx=(5, 5), pady=(5, 20))
    ExitB.grid(row=4, column=3, padx=(5, 20), pady=(5, 20))

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
    DoAutoPatch = tkinter.BooleanVar(I, value=True)
    im = tkinter.Menu(I, tearoff=False)
    lm = tkinter.Menu(im, tearoff=False)
    lm.add_command(label="English", command=lambda: SetLang("en-us"))
    for i in os.listdir(str(pathlib.Path(__file__).parent / "lang")):
        if not i.endswith(".json"):
            continue
        try:
            langname = i.rsplit(".", 1)[0]
            with open(pathlib.Path(__file__).parent / "lang" / i, encoding="utf8", mode="rt") as f:
                lang_data[langname] = json.loads(f.read())
            lm.add_command(label=lang_data[langname]["friendly_name"], command=lambda x=langname: SetLang(x))
        except:
            continue
    im.add_cascade(label="Language", menu=lm)
    im.add_checkbutton(label=GetText("Auto patch new window"), variable=DoAutoPatch)
    im.add_command(
        label=GetText("Patch all"),
        command=lambda: list(AutoPatch(int(i.split(" ", 1)[0])) for i in WindowSelector.cget("values")),
    )
    im.add_command(label=GetText("Check updates"), command=startCheckUpdate)
    im.add_command(label=GetText("Exit"), command=w.destroy)

    img = pickle.loads(zlib.decompress(base64.b85decode(icon)))
    imgTk = PIL.ImageTk.PhotoImage(img)
    il = tkinter.Label(I, bd=0, image=imgTk)
    il.place(x=0, y=0)
    I.protocol("WM_DELETE_WINDOW", lambda: 0)
    I.attributes("-topmost", 1)
    I.attributes("-alpha", 0.7)
    I.attributes("-transparentcolor", "#ff0000")
    I.bind("<Enter>", lambda _: I.attributes("-alpha", 0.7))
    I.bind("<Leave>", lambda _: I.attributes("-alpha", 0.3))
    I.bind("<ButtonPress-1>", MouseDownI)
    I.bind("<B1-Motion>", MouseMoveI)
    I.bind("<ButtonRelease-1>", MouseUpI)
    I.bind("<Button-3>", lambda e: im.tk_popup(e.x_root, e.y_root))

    SetLang(locale.getdefaultlocale()[0].lower().replace("_", "-"))

    ScanThread = threading.Thread(target=ScanWindow)
    ScanThread.start()

    UpdateThread = threading.Thread(target=CheckUpdate)
    UpdateThread.start()

    w.mainloop()
    run = False
    sys.exit(0)
