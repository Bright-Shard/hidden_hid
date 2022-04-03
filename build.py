"""
Builds the HiddenHID Binaries with PyInstaller
"""

import subprocess
from platform import system

os = system()

if os == "Darwin":
    subprocess.run('pyinstaller hiddenhid.py -F -n Finder --distpath ./bin -y', shell=True, check=False)
    # subprocess.run('pyinstaller hiddenhid.py -F -n Finder --distpath ./bin -y -w -i ' +
    # '"/System/Library/CoreServices/Finder.app/Contents/Resources/Finder.icns"', shell=True, check=False)
elif os == "Windows":
    subprocess.run("pyinstaller hiddenhid.py -F -w --distpath ./bin")
else:
    print("Error: Unsupported platform: "+os)
