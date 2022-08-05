# WARNING: RUST VERSION IS STILL IN DEVELOPMENT

# HiddenHID

*HID attacks - supercharged.*

HiddenHID is an all-in-one HID framework, making HID attacks universal, easy to write, and completely invisible. While normal HID attacks open a terminal (or similar
app) - in plain sight - and type out commands manually, HiddenHID attacks launch HiddenHID and execute commands efficiently and invisibly.

## Features

- **Cross-platform**: Write one payload for every target, instead of separate, OS-dependant payloads.
- **Easy to Write**: HiddenHID payloads only need a few simple commands to run advanced attacks.
- **Invisible**: As the name suggests, HiddenHID is completely hidden from view. It's actually an invisible application with a text box.

## How it Works

Behind the scenes, HiddenHID is just an app with a text box (Don't believe me? Run the "show" and "hide" commands!). Unlike other apps, though, it renders completely
invisibly on the desktop, making it hard for a target to realize anything is happening.

## Programming notes

This Rust version of HiddenHID is more efficient, but the code may be harder to read for
new programmers or people who don't use Rust. Therefore, I'm preserving the (old) Python
version on the Python branch.

I switched to Rust because it compiles into much smaller binaries - between 1 and 3 mb instead of almost 10 in Python, and waiting for long downloads in an HID attack
doesn't work very well. Rust is also much faster than Python.
