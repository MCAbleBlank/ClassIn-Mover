/*
    ClassIn Mover - A program to move ClassIn classroom window in order to
    exit from focused learning mode.
    Copyright (C) 2020-2021  Weiqi Gao, Jize Guo

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

#include <cstdio>
#include <cstring>
#include <ctime>
#include <windows.h>
#include <tlhelp32.h>
#include <Psapi.h>
#pragma comment (lib, "Psapi.lib")
#pragma warning(disable:4996)

HWND ClassroomHwnd;
bool FoundWindow;
TCHAR title[1024];

BOOL CALLBACK RefreshWindow(HWND hwnd, LPARAM Title)
{
    PROCESSENTRY32 pe32;
    pe32.dwSize = sizeof pe32;
    time_t tmp = time(0);
    tm* now = localtime(&tmp);
    TCHAR caption[1024];
    memset(caption, 0, 1024);
    GetWindowText(hwnd, caption, 1024);
    DWORD pid;
    if (lstrlen(caption) && wcsstr(caption, L"Classroom_") != NULL && !FoundWindow)
    {
        char FormattedTime[9];
        strftime(FormattedTime, 9, "%H:%M:%S", now);
        GetWindowThreadProcessId(hwnd, &pid);
        HANDLE hProcessSnap = ::CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
        if (hProcessSnap == INVALID_HANDLE_VALUE)
        {
            SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED);
            printf("[%s] Failed to excute CreateToolhelp32Snapshot\n", FormattedTime);
            SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
            return TRUE;
        }
        BOOL bMore = ::Process32First(hProcessSnap, &pe32);
        bool flag = false;
        while (bMore)
        {
            if (DWORD(pe32.th32ProcessID) == pid)
            {
                flag = true;
                break;
            }
            bMore = ::Process32Next(hProcessSnap, &pe32);
        }
        TCHAR path[MAX_PATH];
        wcscpy(path, pe32.szExeFile);
        wcslwr(path);
        if (!flag || wcsstr(path, L"classin") == NULL)
        {
            CloseHandle(hProcessSnap);
            return TRUE;
        }
        wcscpy(title, caption);
        ClassroomHwnd = hwnd;
        FoundWindow = true;
        CloseHandle(hProcessSnap);
    }
    return TRUE;
}

bool IsProcessRunAsAdmin()
{
    SID_IDENTIFIER_AUTHORITY NtAuthority = SECURITY_NT_AUTHORITY;
    PSID AdministratorsGroup;
    BOOL b = AllocateAndInitializeSid(
        &NtAuthority,
        2,
        SECURITY_BUILTIN_DOMAIN_RID,
        DOMAIN_ALIAS_RID_ADMINS,
        0, 0, 0, 0, 0, 0,
        &AdministratorsGroup);
    if (b)
    {
        CheckTokenMembership(NULL, AdministratorsGroup, &b);
        FreeSid(AdministratorsGroup);
    }
    return b == TRUE;
}

long long CurrentTime() {
    SYSTEMTIME st;
    GetLocalTime(&st);
    time_t tmp = time(0);
    return tmp + st.wMilliseconds;
}

void GetWindowCmd(UINT showCmd, char* ReturnValue)
{
    switch (showCmd) {
    case (UINT)SW_MINIMIZE: strcpy(ReturnValue, "Minimized"); break;
    case (UINT)SW_SHOWMINIMIZED: strcpy(ReturnValue, "Minimized"); break;
    case (UINT)SW_MAXIMIZE: strcpy(ReturnValue, "Maximized"); break;
    case (UINT)SW_NORMAL: strcpy(ReturnValue, "Normal"); break;
    default: sprintf(ReturnValue, "%d", showCmd); break;
    }
}

#define SleepUntilNext(ms) Sleep((ms) - CurrentTime() % (ms))

int main()
{
    SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
    puts("ClassIn Mover v1.0.5");
    puts("Copyright (C) 2020-2022  Weiqi Gao, Jize Guo");
    puts("Visit https://github.com/CarlGao4/ClassIn-Mover for more information.\n");
    TCHAR szPath[MAX_PATH];
    ZeroMemory(szPath, MAX_PATH);
    ::GetModuleFileName(NULL, szPath, MAX_PATH);
    HINSTANCE res;
    if (!IsProcessRunAsAdmin())
    {
        res = ShellExecute(NULL, L"runas", szPath, NULL, NULL, SW_SHOW);
        if ((int)res > 32)
        {
            return 0;
        }
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN);
        printf("Warning : You do not have administrator's permission running this program. \n\n");
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), FOREGROUND_INTENSITY | FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE);
    }
    RECT rect;
    HWND hwnd = GetDesktopWindow();
    GetWindowRect(hwnd, &rect);
    WINDOWPLACEMENT wp;
    wp.length = sizeof(WINDOWPLACEMENT);
    int processes;
    while (true)
    {
        FoundWindow = false;
        EnumWindows(RefreshWindow, NULL);
        time_t tmp = time(0);
        tm* now = localtime(&tmp);
        char FormattedTime[9];
        strftime(FormattedTime, 9, "%H:%M:%S", now);
        if (!FoundWindow)
        {
            printf("[%s] Cannot find classroom window\n", FormattedTime);
            SleepUntilNext(1000);
            continue;
        }
        processes = 0;
        GetWindowPlacement(ClassroomHwnd, &wp);
        UINT firstStatus = wp.showCmd;
        while (CurrentTime() % 1000 <= 800)
        {
            GetWindowRect(ClassroomHwnd, &rect);
            SetWindowPos(ClassroomHwnd, HWND_NOTOPMOST, rect.left, rect.top,
                rect.right - rect.left, rect.bottom - rect.top, SWP_NOSENDCHANGING);
            GetWindowPlacement(ClassroomHwnd, &wp);
            if (wp.showCmd != SW_MAXIMIZE && wp.showCmd != SW_MINIMIZE && wp.showCmd != SW_SHOWMINIMIZED)
            {
                ShowWindow(ClassroomHwnd, SW_MINIMIZE);
                ShowWindow(ClassroomHwnd, SW_MAXIMIZE);
            }
            processes++;
            Sleep(50);
        }
        char StatusString[10];
        GetWindowCmd(firstStatus, StatusString);
        printf("[%s] Classroom window is found and processed %d times:\n           HWND=%I64d title=%ls status=%s\n",
            FormattedTime, processes, (long long)hwnd, title, StatusString);
        SleepUntilNext(1000);
    }
}
