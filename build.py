"""
Builds the HiddenHID Binaries
"""

import subprocess
from platform import system

os = system()

if os == "Darwin":
    subprocess.run('pyinstaller hiddenhid.py -F -n Finder --distpath ./bin --clean', shell=True, check=False)
