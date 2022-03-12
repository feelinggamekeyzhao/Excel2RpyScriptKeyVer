#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    将Excel中的数据转化为rpy中的对象
"""
from collections import namedtuple
from corelib.exception import RenderException

from const.dialog_converter_setting import ElementColNumMapping, PositionMapping, ImageCmdMapping, TransitionMapping, \
    ReplaceCharacterMapping, BooleanMapping
from model.element import Dialog, Image, Transition, Audio, Command, Voice, Menu, Romance

SheetConvertResult = namedtuple('SheetConvertResult', ['label', 'data'])

RowConvertResult = namedtuple('RowConvertResult',
                              ['label',  
                               'music',
                               'sound',
                               'scene',
                               'voice',
                               'tachie',
                               'transition_1',
                               'show_menu',
                               'is_option',
                               'character',
                               'dialog',
                               'romance_point',
                               'jump_to_label',  
                               'clear_page',
                               'pause',
                               'renpy_command',
                               ])



class DialogConverter(object):

    def __init__(self, parser):
        self.parser = parser
        self.label = ''
        self.music = ''
        self.sound = ''
        self.scene = ''
        self.voice = ''
        self.tachie = ''
        self.tachie_cmd = ''
        self.tachie_position = ''
        self.show_menu = False
        self.is_option = False
        self.character = ''
        self.current_character = ''
        self.dialog = ''
        self.transition_1 = ''
        self.transition_2 = ''
        self.romance_point = ''
        self.jump_to_label = ''
        self.clear_page = ''
        self.pause = 0
        self.renpy_command = ''

    def generate_rpy_elements(self):
        result = []
        parsed_sheets = self.parser.get_parsed_sheets()
        for idx, parsed_sheet in enumerate(parsed_sheets):
            label = "script"
            if parsed_sheet.name != "Character" and parsed_sheet.name != "Image" and parsed_sheet.name != "CustomCode":
                # print(parsed_sheet.name)
                result.append(SheetConvertResult(label=label, data=self.parse_by_sheet(parsed_sheet.row_values)))
        return result

    def parse_by_sheet(self, values):
        result = []
        for row_value in values:
            result.append(self.parse_by_row_value(row_value))
        return result

    def parse_by_row_value(self, row):
        row_converter = RowConverter(row, self)
        return row_converter.convert()


class RowConverter(object):

    def __init__(self, row, converter):
        self.row = row
        self.converter = converter

    def convert(self):
        return RowConvertResult(
            label=self._converter_label(),
            music=self._converter_music(),
            sound=self._converter_sound(),
            scene=self._converter_scene(),
            voice=self._converter_voice(),
            tachie=self._converter_tachie(),
            transition_1=self._converter_transition_1(),
            show_menu=self._converter_show_menu(),
            is_option=self._converter_is_option(),
            character=self._converter_character(),
            dialog=self._converter_dialog(),
            jump_to_label=self._converter_jump_to_label(),
            clear_page=self._converter_clear_page(),
            pause=self._converter_pause(),
            renpy_command=self._converter_renpy_command(),
            romance_point=self._converter_romance_point(),
        )
        
    def _converter_label(self):
        label = self.row[ElementColNumMapping.get('label')]
        if label:
            self.converter.label = label
        return label
        
    def _converter_music(self):
        music = self.row[ElementColNumMapping.get('music')]
        if not music:
            return None
        cmd = "stop_music" if music == "stop" else "play"
        return Audio(music, cmd)
    
    def _converter_sound(self):
        sound = self.row[ElementColNumMapping.get('sound')]
        if not sound:
            return None
        if sound.startswith('loop'):
            return Audio(sound.replace('loop', ''), 'loop')
        else:
            cmd = "stop_sound" if sound == "stop" else "sound"
            return Audio(sound, cmd)
    
    def _converter_scene(self):
        scene = self.row[ElementColNumMapping.get('scene')]
        if not scene:
            return None
        return Image(scene, "scene")
    
    def _converter_voice(self):
        voice_str = str(self.row[ElementColNumMapping.get('voice')]).strip()
        if not voice_str:
            return None
        if voice_str.split(" ")[-1] == "sustain":
            voice_name = voice_str.split(" ")[0]
            return Voice(voice_name, sustain=True)
        else:
            return Voice(voice_str)
        
    def _converter_tachie(self):
        tachie_str = str(self.row[ElementColNumMapping.get('tachie')]).strip()
        if not tachie_str:
            return None
        self.converter.tachie = tachie_str
        tachie_cmd_str = str(self.row[ElementColNumMapping.get('tachie_cmd')]).strip()
        tachie_cmd = 'hide' if tachie_cmd_str == 'Hide' else 'show' 
        pos_str = self._converter_tachie_position()
        pos = PositionMapping.get("Center") if not pos_str else pos_str
        return Image(tachie_str, tachie_cmd, pos)
        
    def _converter_tachie_position(self):
        if not self.converter.tachie:
            return None
        tachie_position = ""
        tachie_position_str = str(self.row[ElementColNumMapping.get('tachie_position')]).strip()
        if not tachie_position_str:
            return None
        if PositionMapping.get(tachie_position_str) is not None:
            tachie_position = PositionMapping.get(tachie_position_str)
        else:
            raise ValueError("Invalid tachie_position:{}".format(tachie_position_str))
        self.converter.tachie_position = tachie_position
        return tachie_position
    
    def _converter_show_menu(self):
        is_option_str = self.row[ElementColNumMapping.get('is_option')]
        is_option = BooleanMapping.get(is_option_str, False)
        if is_option and not self.converter.is_option:
            show_menu = True
        else:
            show_menu = False
        self.converter.show_menu = show_menu
        return show_menu
        
    def _converter_is_option(self):
        is_option_str = self.row[ElementColNumMapping.get('is_option')]
        is_option = BooleanMapping.get(is_option_str, False)
        self.converter.is_option = is_option
        return is_option


    def _converter_character(self):
        character = self.row[ElementColNumMapping.get('character')]
        if character:
            self.converter.character = character
            self.converter.current_character = character
        elif not self.converter.is_option:
            if self.converter.current_character:
                character = self.converter.current_character
                self.converter.character = character
        return character

    def _converter_dialog(self):
        text = str(self.row[ElementColNumMapping.get('dialog')]).replace("\n", "\\n")
        if not text:
            return None
        replace_index_char = []
        for idx, t in enumerate(text):
            if ReplaceCharacterMapping.get(t):
                replace_index_char.append((idx, t))

        if replace_index_char:
            new_text_list = list(text)
            for idx, char in replace_index_char:
                new_text_list[idx] = ReplaceCharacterMapping.get(char)
            text = ''.join(new_text_list)
        dialog_transition_style = self._converter_transition_2()
        return Dialog(text, self.converter.current_character, dialog_transition_style)

  
    def _converter_transition_1(self):
        transition = self.row[ElementColNumMapping.get('transition_1')]
        if not transition:
            return None
        t_style = TransitionMapping.get(transition, transition)
        return Transition(t_style)
  
    def _converter_transition_2(self):
        transition = self.row[ElementColNumMapping.get('transition_2')]
        if not transition:
            return None
        t_style = TransitionMapping.get(transition, transition)
        return t_style
  
    def _converter_romance_point(self):
        character_romance = self.row[ElementColNumMapping.get('character_romance')]
        romance_point = self.row[ElementColNumMapping.get('romance_point')]
        if not romance_point:
            return None
        return Romance(character_romance, int(romance_point))
  
    def _converter_jump_to_label(self):
        jump_to_label = self.row[ElementColNumMapping.get('jump_to_label')]
        if not jump_to_label:
            self.converter.jump_to_label = jump_to_label
        return jump_to_label

    def _converter_clear_page(self):
        clear_page = self.row[ElementColNumMapping.get('clear_page')]
        if not clear_page:
            return None
        return Command("    nvl clear")

    def _converter_pause(self):
        pause_str = self.row[ElementColNumMapping.get('pause')]
        if not pause_str:
            return 0
        pause = float(pause_str)
        if(pause > 0):
            self.converter.pause = pause
            return pause
        else:
            return 0

    def _converter_renpy_command(self):
        cmd = self.row[ElementColNumMapping.get('renpy_command')]
        self.converter.renpy_command = cmd
        return Command("    {cmd}".format(cmd=cmd))
