# RPY元素与sheet中每列的对应关系
from model.element import Text, Image, Transition, Audio

ElementColNumMapping = {
    'label': 0,
    'character_if_romance': 1,
    'condition': 2,
    'compare_value_1': 3,
    'compare_value_2': 4,
    'music': 5,
    'sound': 6,
    'scene': 7,
    'tachie_cmd': 8,
    'tachie': 9,
    'tachie_position': 10,
    'transition_1': 11,
    'voice': 12,
    'is_option': 13,
    'character': 14,
    'dialog': 15,
    'transition_2': 16,
    'character_romance': 17,
    'romance_point': 18,
    'jump_to_label': 19,
    'clear_page': 20,
    'pause': 21,
    'renpy_command': 22,
    'is_game_end': 23,
}

PositionMapping = {
    "Left": "custom_left",
    "Right": "custom_right",
    "Center": "custom_center",
    "HetrisCenter": "hetris_center",
}
# "truecenter": "truecenter",

BooleanMapping = {
    "Yes": True,
    "Yes If 2nd Playthrough": True,
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
