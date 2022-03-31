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
- Coming soon; I'm working on macOS right now

## Linux-Specific Features
So many things change depending on the distro, I'm not sure if I'll ever add Linux-specific features. If I do, they
will come after the Windows ones.

# Shortcut Commands
WIP :P