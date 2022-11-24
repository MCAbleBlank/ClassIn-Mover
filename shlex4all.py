"""
## shlex for all

The standard lib `shlex` provides parsing only for Unix, this libarary is
intended to provide such parsing for all platforms. You can use `join`,
`split` and `quote` function.

On Windows, the parsing follows documents on https://docs.python.org/3.11/library/subprocess.html#converting-an-argument-sequence-to-a-string-on-windows and https://learn.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-commandlinetoargvw#remarks

On other platforms, the functions are same as `shlex`. 
"""

import sys
import re
from typing import Iterable

__all__ = ["join", "quote"]

if sys.platform != "win32":
    import shlex

    join = shlex.join
    split = shlex.split
    quote = shlex.quote

else:

    def quote(s: str):
        if type(s) != str:
            raise TypeError("s must be `str`")
        if " " not in s and "\t" not in s and '"' not in s:
            return s
        ret = s
        if '"' in ret:
            ret = ret.replace('"', '\\"')
        if " " in ret or "\t" in ret:
            ret = '"' + ret + '"'
        ret = re.sub('(\\\\+)\\\\"', '\\1\\1\\"', ret)
        return ret

    def join(s: Iterable):
        return " ".join(quote(i) for i in s)
