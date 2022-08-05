use eframe::egui;
use crate::style;
use crate::brightscript;

#[derive(Default)]
pub struct UI {
    text: String
}

impl UI {
    pub fn new(ctx: &eframe::CreationContext<'_>) -> Self {
        ctx.egui_ctx.set_visuals(style::INVISIBLE_STYLE);
        Self {
            text: String::from("")
        }
    }
}

impl eframe::App for UI {
    fn update(&mut self, ctx: &egui::Context, app: &mut eframe::Frame) {
        egui::Area::new("Finder")
            .show(ctx, |ui| {
                let cmdbar = ui.text_edit_singleline(&mut self.text);

                // If the command bar has lost focus, enter was pressed, so handle the command
                // It also loses focus when the app starts, but then we're just handling a blank command (aka doing nothing)
                if !cmdbar.has_focus() {
                    // Conver the command to an &str for pattern matching
                    let cmd = self.text.as_str();

                    // If the command isn't blank
                    if cmd != "" {
                        // Handle the command
                        match self.text.as_str() {
                            // These commands require access to the context/app variables,
                            // so they're handled here instead of the normal handler
                            "exit" => app.quit(),
                            "show" => ctx.set_visuals(egui::Visuals::dark()),
                            "hide" => ctx.set_visuals(style::INVISIBLE_STYLE),
                            _ => {
                                // If the command starts with $, run it in a shell
                                if cmd.chars().nth(0).unwrap() == '$' {
                                    brightscript::run_in_shell(&self.text);
                                // Otherwise treat it as BrightScript
                                } else {
                                    brightscript::parse(&self.text)
                                }
                            }
                        }

                        // Reset the text
                        self.text = String::from("");
                    }
                }


                // Make the command bar focus again, so it can be typed in
                cmdbar.request_focus();
            });
    }
    fn clear_color(&self, _: &egui::Visuals) -> egui::Rgba {
        return egui::Rgba::TRANSPARENT
    }
 }