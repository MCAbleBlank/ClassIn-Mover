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

import json
import logging
import pathlib
import traceback

_threads_total = 0


def ShowThread(func):
    def ThreadTrace(*args, **kw):
        global _threads_total
        _threads_total += 1
        tid = _threads_total
        logging.debug("Thread %d (%s) started" % (tid, func.__name__))
        res = func(*args, **kw)
        logging.debug("Thread %d (%s) stopped" % (tid, func.__name__))
        return res

    return ThreadTrace


SettingsFile = pathlib.Path.home() / "AppData" / "Local" / "ClassIn-Mover" / "settings.json"
if SettingsFile.exists():
    try:
        with open(str(SettingsFile), mode="rt", encoding="utf8") as f:
            settings = json.loads(f.read())
        if type(settings) != dict:
            raise TypeError
    except:
        settings = {}
else:
    settings = {}


def SetSetting(attr, value):
    global settings, SettingsFile
    logging.debug('(%s) Set setting "%s" to %s' % (traceback.extract_stack()[-2].name, attr, str(value)))
    settings[attr] = value
    with open(str(SettingsFile), mode="wt", encoding="utf8") as f:
        f.write(json.dumps(settings, separators=(",", ":")))


def GetSetting(attr, default=None, autoset=True):
    global settings
    if attr in settings:
        return settings[attr]
    else:
        if autoset:
            SetSetting(attr, default)
        return default
