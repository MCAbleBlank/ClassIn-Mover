# ![ClassIn-Mover icon 32x32](ClassIn_Mover_32.png) ClassIn-Mover ![GitHub all releases](https://img.shields.io/github/downloads/CarlGao4/Classin-mover/total)

A program to move `ClassIn` classroom window in order to exit from focused learning mode.

Supported `ClassIn` version: `3.0.2.130` to `3.0.5.1`, as well as `3.0.7.x` `4.x`. (`ClassIn` prior to `3.0.2.130` does not have focused learning mode at all)

Maybe the program will lose efficacy in the future versions.

## Components

### Classic

The program remained the old style of v1.0.0, except the modern UI by Tk. 

#### Usage

Run this program before entering the classroom, then get into the classroom as normal.

After that, the program will automatically detect the classroom window, and make it unable to occupy the whole screen.

If working well, the program should output one line of log each second, showing the current working status.

### Enhanced

The program will be started on the minimized status, which only a transparent icon is displayed. You can click it to open the main window, which can move, resize, and set z-order (or topmost) of your selected ClassIn window. 

Auto patch is enabled as default, which will automatically resize the window into normal state like other applications once a new ClassIn window has been detected. You can disable this feature by right-clicking the minimized icon. The button `Auto Patch` on the main window will not enable this feature, but just patch the selected window.

## Running the codes

As you may have noticed, the latest version uses Python, which means you can run the codes yourself. The dependencies are `Pillow` and `psutil`. After you have installed these two packages using `pip` or `conda`, you can directly run the program with a Python interpreter. 

**However, it is not recommended to run or modify the codes if you don't have coding experience. Use the releases instead.**

## Known issues

- **This program calls native API and thus can only work on Windows.**
