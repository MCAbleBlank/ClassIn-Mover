LICENSE = """ClassIn Mover - A program to move ClassIn classroom window in order to
exit from focused learning mode.

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

__version__ = "2.0.0"

import tkinter
import tkinter.ttk
import ctypes
import ctypes.wintypes
import struct
import time
import math
import threading
import sys
import os
import shlex
import psutil
import PIL
import PIL.Image
import PIL.ImageTk
import subprocess
import pathlib
import pickle
import zlib
import base64

ClassInHwnd = []
ClassInTitle = []
ClassInPID = []
run = True
NoAdmin = False
icon = "c-rllZA=q)9LG^vra)9$9)zMi$wMi9rnIz_KG0Iy0s<wnk%@@wY88-y7~E7~iwFv)NUPDPyx7=YxoM0L!%V<;>I`Itn8mm#V=s)^1mnzNWbC^;X>O&ID|2&M{N`w`$Mt@n`#t@Ccddc0dR73TE=IAjfTyjkH`Z>mS&M6$Z1y^5SBTDDO&rLx*I1psPIjAfi!=3rGqr2Q`}KCGA>gIlJMGS{;O)C>>l>_%jrQGjPIEw0*NReu)@c@)1?|ovZ2;`ezS-VvuXg))<PS_?VWC2yP^nZoIXOzD68mzwTq>1jW@ct&WQar}p-{-@^Lad8dU|?VT3TvqYD!8<Qc_Z4Vq$!Jd|X`Ih7B9muV2q%v7(}))~#C?85tQC7RF#Of`WpWOr{@5v$NUR+4=eTX0zF7G-4+&FHf)6=jP^WwOX}WO(m4cWFVACBx11`kOF}Kgj_C{!{JaNH*VaRkdOe#*w|P=f-Qi&aeB^yU4LQVuK6&@$;qV000XCyFflPP(b3Us*RG}IqS;xJ#AGrp1OxApFbE&jGYFp>hRtS^Fr;TZU`Ww&5#gMCLQ4pfM=p7UiG*Rzi9V0PU|19eS?%E&Hw@J??!@+hq0fVw(i5V>AVz@6%F3GW8ETjo@(iq#F<Jr-tb;_S(`hsszyOc*%zPN+@S<UYbG*XP=YcD<gci*iub%N*O)PJs$ph<ZLVoobkDT!lCVzQg+M_Kmt?9W-o3(&w@}R3I3H|-1=L3d54@`r^-Sm9qjMt_ILs+LmLqi$fgoVss9yAt|5(xtmn4>O^_=Hcqh6(=)2?<%VW)0Tj^78UBLKcgqw6wIOq@=jGxU#Ym9(E(q<bfY#ga8IdO;1lhdGh3ELfF4}@gm{{(;f*7D}d?i>+>;RjE#-q9Cr|D^57Q8xdP5XXb`yhS4IQJ8tsM&4-d!Z^XJcfzzhrwEL*k=vxmR&LWW2PkvW4T0h`rott135k=I89N1gx!!wfv;Vg2dTr@zi=W@hHnrAr<#^m*VDF(G#XBU{MwL72cWF)=|J#S8%d;{+;6cX#*l<;!7fIYp~hty*$_M(v0Qc`a=e5k{BE$w{0!Iy#Cxr^485Hdy!Y11a~I;V%zNd+jssYC=)3UcI`%zaQ?R!l0~R;_W#_L_|<wFtlQ$BGKf5X>u_3(e%(>07iv*`0(L{3l~O4MuvxnuU)%#_wHS+I6xvuqHqhGbX-%21r}dPB$_<%1DDW3O%E5u0O0%4p}D!4ENz@jw6Da%O%)2Ik;CD+k!bS3G)R1m5V&i!xP?d_Ja~ZIBNG_HPvYW}6iU-CkEie5yU*dt;V4`LNHlp6lr%y<COvfiz`($onwl$Dt{^ny<Ku&agD#f~S%>4OK{97zVpz#398K<~XU~3nNjotq$;{;o#Pt1xh@=woJ?Y^FQD`eyu6&CSb`T&mMt2?I1U!dv`HItL`Y&G|y7$BVv9a3&16SKSdKKAuxHFnOFr7k({-o!vuA`!fB+==ODph`Rim0va$U7BQp;)QWm<kFuq1I^fz-|&D`jg&Y>lz6ho66>jGB9#yM@B}#v`8#D(&e=8Y{FoLuQ-^MrHGABqr(H!An|L`qr&|8tQ?<YG;gk~sxz63!o!hGOg>L|l;Dxe75I*WQkkl8Z=2p=S(FD?P9Q{o(sR?|7jbb(Sqj687c=`lZrAHgs8dv{P$W6jer#KHom!(MYB!xPkbT~N{?486v$FGj^N=0GuSw6%!)9~y^2<=#xXu?}o-eUfZr!#ETdAe;tFJHj96wc7UcIHtzGbVupy=Iiu8!ce>({?E7|VR{puNNrq7O626UF6aH0(J@miCPsx4Ms=aJtU+y3TfWpBNpzJv20YwA<x4e%j$U)zRtr?)Lc1%!|n%e=4<XJ=gb{kNP6#KspKR;U83GTs*s~x)#@I+S?{qXmeEB9HmAimbbKZR=j6ZYxGK`My1lGurtn_>wom<kuI;arM2Dn`wh&Te!)=l8I3C;F|DqC--nH@sOt!{r0_6-Ky<jX$F`#p(_J`m1o_<2*;`mt(e}yVMN>K`C<q<cUmhwFUm%r8btZEGOf#7bK3~}0;Q)^U^~GdjIYx%-4P_l2$7sF+!b*Y8AF?C`2M044p;#<nS0uvILAF3BJ=oHLc&XGnsZ1f2%KUg=_v+psI-R|0ZP5oins(JT4-5{S>+9cDyRU5X_J+p&uj|#Q!*SBSa}PoHJN~8~Kem)rIeJ{L@onu#`#;6XH8nMbDHm(~;tBlEZ~G4%vh8Rvn#)^S5B*2pY4;pIdGqG2H}CfUf1A@<&HDox^xKy"


def has_admin():
    try:
        # only windows users with admin privileges can read the C:\windows\temp
        os.listdir(os.sep.join([os.environ.get("SystemRoot", "C:\\windows"), "temp"]))
    except:
        return os.environ["USERNAME"], False
    else:
        return os.environ["USERNAME"], True


# if __name__ == "__main__" and not has_admin()[1]:
#     p = psutil.Process().cmdline()
#     res = ctypes.windll.shell32.ShellExecuteW(
#         0,
#         ctypes.create_unicode_buffer("runas"),
#         ctypes.create_unicode_buffer(p[0]),
#         ctypes.create_unicode_buffer(shlex.join(p[1:])),
#         0,
#         5,
#     )
#     if res > 32:
#         raise SystemExit
#     NoAdmin = True


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
    last = ""
    count = 0
    while run:
        try:
            st = time.time()
            if not count % 30:
                I.attributes("-topmost", 1)
                w.attributes("-topmost", 1)
            if not w.focus_get():
                w.attributes("-topmost", 1)
            count += 1
            CIHwnd = GetClassInHwnd()
            if len(CIHwnd) != 0:
                newvalues = []
                newset = " ".join(sorted(str(i[1]) for i in CIHwnd))
                if newset != last:
                    for i in CIHwnd:
                        newvalues.append("%d (Title=%s PID=%d)" % (i[1], i[2], i[0]))
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
    global root_shown
    if imxr == event.x_root and imyr == event.y_root:
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
    return int(s.split(" ", 2)[0])


def MoveWindow(sw=None, InsertAfter=None, x=None, y=None, cx=None, cy=None):
    CIW = GetWindow()
    if sw is not None:
        ctypes.windll.user32.ShowWindow(CIW, sw)
    if InsertAfter is not None:
        rect = struct.pack("llll", *([0] * 4))
        ctypes.windll.user32.GetWindowRect(CIW, rect)
        rect = struct.unpack("llll", rect)
        ctypes.windll.user32.SetWindowPos(
            CIW,
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
        ctypes.windll.user32.GetWindowRect(CIW, rect)
        rect = struct.unpack("llll", rect)
        ctypes.windll.user32.MoveWindow(
            CIW,
            rect[0] if x is None else x,
            rect[1] if y is None else y,
            rect[2] - rect[0] if cx is None else cx,
            rect[3] - rect[1] if cy is None else cy,
            1,
        )


def AutoPatch():
    MoveWindow(sw=6, InsertAfter=-2)
    time.sleep(0.1)
    MoveWindow(sw=3)


if __name__ == "__main__":
    w = tkinter.Tk()
    w.resizable(False, False)
    w.title("ClassIn Mover v2.0.0")
    w.iconbitmap(str(pathlib.Path(__file__).parent / "ClassIn_Mover.ico"))
    w.attributes("-topmost", 1)
    root_shown = False

    style = ctypes.windll.user32.GetWindowLongW(int(w.frame(), 16), -16)
    style &= ~0x00020000
    style = ctypes.windll.user32.SetWindowLongW(int(w.frame(), 16), -16, style)

    w.withdraw()

    WindowSelector = tkinter.ttk.Combobox(w, width=56, state="readonly")
    MinimizeB = tkinter.ttk.Button(w, text="Minimize", command=lambda: MoveWindow(sw=6))
    MaximizeB = tkinter.ttk.Button(w, text="Maximize", command=lambda: MoveWindow(sw=3))
    NormalB = tkinter.ttk.Button(w, text="Normalize", command=lambda: MoveWindow(sw=1))
    FullB = tkinter.ttk.Button(
        w, text="Full Screen", command=lambda: MoveWindow(x=0, y=0, cx=w.winfo_screenwidth(), cy=w.winfo_screenheight())
    )
    TopB = tkinter.ttk.Button(w, text="Topmost", command=lambda: MoveWindow(InsertAfter=-1))
    NoTopB = tkinter.ttk.Button(w, text="No Topmost", command=lambda: MoveWindow(InsertAfter=-2))
    SwitchB = tkinter.ttk.Button(
        w, text="Switch To", command=lambda: ctypes.windll.user32.SetForegroundWindow(GetWindow())
    )
    AutoB = tkinter.ttk.Button(w, text="Auto Patch", command=AutoPatch)

    WindowSelector.grid(row=0, column=0, columnspan=4, padx=(20, 20), pady=(20, 5))
    MinimizeB.grid(row=1, column=0, padx=(20, 5), pady=(5, 5))
    MaximizeB.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))
    NormalB.grid(row=1, column=2, padx=(5, 5), pady=(5, 5))
    FullB.grid(row=1, column=3, padx=(5, 20), pady=(5, 5))
    TopB.grid(row=2, column=0, padx=(20, 5), pady=(5, 5))
    NoTopB.grid(row=2, column=1, padx=(5, 5), pady=(5, 5))
    SwitchB.grid(row=2, column=2, padx=(5, 5), pady=(5, 5))
    AutoB.grid(row=2, column=3, padx=(5, 20), pady=(5, 5))

    I = tkinter.Toplevel()
    I.overrideredirect(True)
    I.geometry("48x48+96+96")
    I.resizable(False, False)
    im = tkinter.Menu(I, tearoff=False)
    im.add_command(label="Exit", command=w.destroy)

    img = pickle.loads(zlib.decompress(base64.b85decode(icon)))
    imgTk = PIL.ImageTk.PhotoImage(img)
    il = tkinter.Label(I, bd=0, image=imgTk)
    il.place(x=0, y=0)
    I.protocol("WM_DELETE_WINDOW", lambda: 0)
    I.attributes("-topmost", 1)
    I.attributes("-alpha", 0.3)
    I.attributes("-transparentcolor", "#ff0000")
    I.bind("<Enter>", lambda _: I.attributes("-alpha", 0.7))
    I.bind("<Leave>", lambda _: I.attributes("-alpha", 0.3))
    I.bind("<ButtonPress-1>", MouseDownI)
    I.bind("<B1-Motion>", MouseMoveI)
    I.bind("<ButtonRelease-1>", MouseUpI)
    I.bind("<Button-3>", lambda e: im.tk_popup(e.x_root, e.y_root))

    ScanThread = threading.Thread(target=ScanWindow)
    ScanThread.start()

    w.mainloop()
    run = False
    sys.exit(0)
