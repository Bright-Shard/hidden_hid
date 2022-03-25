"""
Builds the HiddenHID Binaries
"""

import PyInstaller.__main__ as pyinstaller
from platform import system

os = system()

if os == "Darwin":
    pyinstaller.run([
        'hiddenhid.py',
        '-F',
        '-n Finder',
        '--distpath ./bin',
        '--clean'
    ])
