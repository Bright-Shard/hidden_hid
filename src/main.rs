// hide console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod app;
mod style;
mod brightscript;

use app::UI;

fn main() {
    let options = eframe::NativeOptions {
        transparent: true,
        decorated: false,
        always_on_top: true,
        ..Default::default()
    };
    eframe::run_native(
        "HiddenHID",
        options,
        Box::new(|ctx| Box::new(UI::new(ctx)))
    );
}