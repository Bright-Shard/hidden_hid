# Hidden HID by BrightShard
HiddenHID is a Tkinter program that makes an invisible window with a text box. Anything typed into the text box will
be run invisibly in a terminal via the Subprocess library - effectively, this makes an invisible terminal app!

As the name implies, HiddenHID is intended for HID attacks, so that terminal commands can be run without the user
seeing anything appear on their screen. It is cross-platform, but I'm adding platform-specific features that use the OS
to make HiddenHID even more hidden (see below).

HiddenHID also has several built-in "shortcut" commands. They help automate long tasks. See below for more info.

## macOS-Specific Features
- Binaries are named "Finder" and copy Finder's menus, making it look like the Finder app is open
- When HiddenHID launches, it makes all terminals invisible with AppleScript
- When HiddenHID closes, it force-quits all terminals with AppleScript

## Windows-Specific Features
- The app doesn't appear in the app/task bar, so there's no sign that HiddenHID is actually running (minus Task Manager)

## Linux-Specific Features
So many things change depending on the distro, I'm not sure if I'll ever add Linux-specific features. If I do, they
will come after the Windows ones.

# Shortcut Commands
When typing a command into HiddenHID, you can type a shortcut name instead to run that shortcut.
## macOS Shortcuts:
### Wallpaper
Format: `wallpaper <url>`, where `<url>` is the url of the image to set as the wallpaper.

This shortcut downloads the image, saves it to a file, sets it as the wallpaper, and then deletes the file.
### Volume
Format: `volume <amount>`, where amount is the volume (From 0 to 10)

This shortcut sets the computer's volume to the provided value.
### Mute
Format: `mute`

This shortcut sets the computer's volume to 0.
### Shell
Format: `shell <ip> <port>`, where `<ip>` is the attacker's IP and `<port>` is the port of the listener.

This shortcut spawns a reverse shell to the provided IP and port.
## Windows Shortcuts:
### Shell
Format: `shell <ip> <port>`, where `<ip>` is the attacker's IP and `<port>` is the port of the listener.

This shortcut spawns a reverse shell to the provided IP and port.