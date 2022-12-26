# Modified from https://gist.github.com/cobryan05/8e191ae63976224a0129a8c8f376adc6

import logging
import traceback
import winreg


class WebcamDetect:
    REG_KEY = winreg.HKEY_CURRENT_USER
    WEBCAM_REG_SUBKEY = (
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam\\NonPackaged"
    )
    WEBCAM_TIMESTAMP_VALUE_NAME = "LastUsedTimeStop"
    WEBCAM_TIMESTAMP_VALUE_NAME_START = "LastUsedTimeStart"

    def __init__(self):
        self.not_supported = False
        try:
            self._regKey = winreg.OpenKey(self.REG_KEY, self.WEBCAM_REG_SUBKEY)
        except:
            logging.critical(traceback.format_exc())
            self.not_supported = True

    def getActiveApps(self):
        activeApps = {}
        # Enumerate over the subkeys of the webcam key
        subkeyCnt, valueCnt, lastModified = winreg.QueryInfoKey(self._regKey)
        for idx in range(subkeyCnt):
            subkeyName = winreg.EnumKey(self._regKey, idx)
            subkeyFullName = f"{self.WEBCAM_REG_SUBKEY}\\{subkeyName}"

            # Open each subkey and check the 'stopped' timestamp value. A value of 0 implies the camera is in use.
            subkey = winreg.OpenKey(self.REG_KEY, subkeyFullName)
            stoppedTimestamp, _ = winreg.QueryValueEx(subkey, self.WEBCAM_TIMESTAMP_VALUE_NAME)
            if 0 == stoppedTimestamp:
                activeApps[subkeyName.replace("#", "\\")] = winreg.QueryValueEx(
                    subkey, self.WEBCAM_TIMESTAMP_VALUE_NAME_START
                )[0]

        return activeApps

    def isActive(self):
        return len(self.getActiveApps()) > 0


class MicDetect:
    REG_KEY = winreg.HKEY_CURRENT_USER
    MIC_REG_SUBKEY = (
        "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone\\NonPackaged"
    )
    MIC_TIMESTAMP_VALUE_NAME = "LastUsedTimeStop"
    MIC_TIMESTAMP_VALUE_NAME_START = "LastUsedTimeStart"

    def __init__(self):
        self.not_supported = False
        try:
            self._regKey = winreg.OpenKey(self.REG_KEY, self.MIC_REG_SUBKEY)
        except:
            logging.critical(traceback.format_exc())
            self.not_supported = True

    def getActiveApps(self):
        activeApps = {}
        # Enumerate over the subkeys of the microphone key
        subkeyCnt, valueCnt, lastModified = winreg.QueryInfoKey(self._regKey)
        for idx in range(subkeyCnt):
            subkeyName = winreg.EnumKey(self._regKey, idx)
            subkeyFullName = f"{self.MIC_REG_SUBKEY}\\{subkeyName}"

            # Open each subkey and check the 'stopped' timestamp value. A value of 0 implies the microphone is in use.
            subkey = winreg.OpenKey(self.REG_KEY, subkeyFullName)
            stoppedTimestamp, _ = winreg.QueryValueEx(subkey, self.MIC_TIMESTAMP_VALUE_NAME)
            if 0 == stoppedTimestamp:
                activeApps[subkeyName.replace("#", "\\")] = winreg.QueryValueEx(
                    subkey, self.MIC_TIMESTAMP_VALUE_NAME_START
                )[0]

        return activeApps

    def isActive(self):
        return len(self.getActiveApps()) > 0
