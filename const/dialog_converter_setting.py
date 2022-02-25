# RPY元素与sheet中每列的对应关系
from model.element import Text, Image, Transition, Audio

ElementColNumMapping = {
    'label': 0,
    'music': 1,
    'sound': 2,
    'scene': 3,
    'tachie_cmd': 4,
    'tachie': 5,
    'tachie_position': 6,
    'transition_1': 7,
    'voice': 8,
    'is_option': 9,
    'character': 10,
    'dialog': 11,
    'transition_2': 12,
    'jump_to_label': 13,
    'clear_page': 14,
    'pause': 15,
    'renpy_command': 16,
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
