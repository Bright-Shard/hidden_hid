use eframe::egui::{self, Color32, style};

const INVISIBLE: Color32 = Color32::TRANSPARENT;
const ROUNDING: egui::Rounding = egui::Rounding {
    nw: 0f32,
    ne: 0f32,
    sw: 0f32,
    se: 0f32,
};
const STROKE: egui::Stroke = egui::Stroke {
    width: 0f32,
    color: INVISIBLE
};
const SHADOW: egui::epaint::Shadow = egui::epaint::Shadow {
    extrusion: 0f32,
    color: INVISIBLE
};
const WIDGETVISUALSTYLE: style::WidgetVisuals = style::WidgetVisuals {
        bg_fill: INVISIBLE,
        bg_stroke: STROKE,
        rounding: ROUNDING,
        fg_stroke: STROKE,
        expansion: 0f32,
};

pub const INVISIBLE_STYLE: egui::Visuals = egui::Visuals {
    dark_mode: false,
    override_text_color: Some(INVISIBLE),
    widgets: style::Widgets {
        noninteractive: WIDGETVISUALSTYLE,
        inactive: WIDGETVISUALSTYLE,
        hovered: WIDGETVISUALSTYLE,
        active: WIDGETVISUALSTYLE,
        open: WIDGETVISUALSTYLE,
    },
    selection: style::Selection {
        bg_fill: INVISIBLE,
        stroke: STROKE,
    },
    hyperlink_color: INVISIBLE,
    faint_bg_color: INVISIBLE,
    extreme_bg_color: INVISIBLE,
    code_bg_color: INVISIBLE,
    window_rounding: ROUNDING,
    window_shadow: SHADOW,
    popup_shadow: SHADOW,
    resize_corner_size: 0f32,
    text_cursor_width: 0f32,
    text_cursor_preview: false,
    clip_rect_margin: 0f32,
    button_frame: false,
    collapsing_header_frame: false,
};
