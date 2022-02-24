# RPY元素与sheet中每列的对应关系
from model.element import Text, Image, Transition, Audio

ElementColNumMapping = {
    'label': 0,
    'music': 1,
    'sound': 2,
    'background': 3,
    'voice': 4,
    'tachie': 5,
    'tachie_position': 6,
    'is_option': 7,
    'character': 8,
    'dialog': 9,
    'hide_tachie_afterward': 10,
    'hide_tachie_at_pos': 11,
    'transition': 12,
    'special_effect': 13,
    'jump_to_label': 14,
    'clear_page': 15,
    'pause': 16,
    'renpy_command': 17,
}

PositionMapping = {
    "Left": "custom_left",
    "Right": "custom_right",
    "Center": "custom_center",
    "HetrisCenter": "hetris_center",
}
# "truecenter": "truecenter",

BooleanMapping = {
    "Yes": True
}

ImageCmdMapping = {
    "hide": "hide",
}

TransitionMapping = {
    "dissolve": "dissolve",
    "fade": "fade",
    "flash": "Fade(0.1,0.0,0.5,color=\"#FFFFFF\")",
    "pixellate": "pixellate",
    "hpunch": "hpunch",
    "vpunch": "vpunch",
    "blinds": "blinds",
    "squares": "squares",
    "wipeleft": "wipeleft",
    "slideleft": "slideleft",
    "slideawayleft": "slideawayleft",
    "pushright": "pushright",
}


ReplaceCharacterMapping = {
    "%": "\\%",  # % --> \%
    "\"": "\\\"",  # " -> \"
    "\'": "\\\'",  # ' -> \'
    "{": "{{",  # { -> {{
    "[": "[[",  # [ -> [[
}
