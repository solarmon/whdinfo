# whdinfo
whdinfo - a python based WHDLoad slave info analyser.

## Features

* Display the WHDLoad slave headers - as described at https://www.whdload.de/docs/autodoc.html#SlaveOverview
* Detect if a WHDLoad LHA file is actually an **installer** package (as opposed to a pre-built WHDLoad LHA package - like **Retroplays** WHDLoad LHA packages).  
* Detect if a **data** directory is present, but the **ws_CurrentDir** is not set in the slave header.
  * This is useful as some environments have trouble with loading this scenario - like on an **A500mini** (as of stock firmware **v1.1.1** or lower)
  * However, some WHDLoad packages do seem to load OK - like Sensible Soccer and Lemmings packages. 

## Requirements

* This is a python script, so requires a working **python environment**.
* There are several **python module dependencies**:

```
import os
import sys
import struct
import binascii

from pathlib import Path

import zipfile
from lhafile import LhaFile

import colorama
from colorama import Fore, Back, Style
```

## Usage:

`python whdinfo.py <path>`

Where `<path>` can be a path to a:
  
* **directory**
* **.lha** file
* **.slave** file

If a directory path, then it will be **recursively** processed.
