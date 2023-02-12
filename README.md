# [![ClassIn-Mover icon 32x32](ClassIn_Mover_32.png) ClassIn-Mover ![GitHub all releases](https://img.shields.io/github/downloads/CarlGao4/Classin-mover/total)](https://classin-mover.pages.dev/)

[简体中文](https://classin-mover.pages.dev/zh-cn)

[Download latest version](https://classin-mover.pages.dev/)

ClassIn-Mover is a program designed to move the ClassIn classroom window and exit from the focused learning mode. The program supports ClassIn versions 3.0.2.130 to 3.0.5.1, as well as 3.0.7.x and 4.x. Please note that ClassIn versions prior to 3.0.2.130 do not have the focused learning mode feature.

The program is available in both English and Simplified Chinese. You can download the latest version from [here](https://classin-mover.pages.dev/).

## Features
ClassIn-Mover is available in two variants: Classic and Enhanced.

### Classic
This version retains the traditional style of v1.0.0, but with a modern UI powered by Tk. To use the program, simply run it before entering the ClassIn classroom and then enter the classroom as normal. The program will automatically detect the ClassIn window and prevent it from occupying the entire screen. If the program is working correctly, it will output a log line once a second indicating the current status.

### Enhanced
This version of ClassIn-Mover starts in a minimized state, with only a transparent icon visible. You can click the icon to open the main window, which allows you to move, resize, and set the z-order or topmost priority of the selected ClassIn window. Auto patching is enabled by default, which automatically resizes the ClassIn window to a normal size once it has been detected. You can disable this feature by right-clicking the minimized icon. The "Auto Patch" button in the main window will not enable this feature, but instead simply patch the selected window.

## Running the Code
ClassIn-Mover is written in Python, so you can run the code yourself if you have coding experience. The program requires the Pillow and psutil packages, which can be installed using pip or conda. Once these packages are installed, you can run the program using a Python interpreter.

Please note that it is not recommended to run or modify the code if you do not have coding experience. Instead, it is recommended to use the released versions of ClassIn-Mover.

## Limitations
ClassIn-Mover relies on native API calls and is only compatible with Windows.

## Donate
Thank you for your interest in supporting this project! Your donation will help us continue to improve and maintain this program.

![WeChat](img/wechat.png)

![AliPay](img/alipay.jpg)

Thank you for your support!
