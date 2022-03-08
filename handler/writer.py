#!/usr/bin/env python
# -*- coding:utf-8 -*-
SIDE_CHARACTER_TEMPLATE = "image side {role_name} = \"{path}\"\n"


class RpyFileWriter(object):

    @classmethod
    def write_file(cls, output_dir, res, role_name_mapping, role_side_character_mapping):
        pass
        # output_path = output_dir + "/" + res.label + '.rpy'
        # with open(output_path, 'w', encoding='utf-8') as f:
        #     for k, v in role_name_mapping.items():
        #         f.write(v.render() + "\n")
        #     f.write("define narrator_nvl = Character(None, kind=nvl)\n")
        #     f.write("define narrator_adv = Character(None, kind=adv)\n")
        #     f.write("define config.voice_filename_format = \"audio/{filename}\"\n")
        #     for k, v in role_side_character_mapping.items():
        #         f.write(SIDE_CHARACTER_TEMPLATE.format(role_name=k, path=v))
        #     f.write("\nlabel {}:\n".format(res.label))
        #     last_voice = None
        #     current_menus = []
        #     for rpy_element in res.data:
        #         if rpy_element.menu:
        #             current_menus.append(rpy_element.menu)
        #             continue
        #         if current_menus:
        #             f.write("menu:\n" + "\n".join(
        #                 [MENU_TEMPLATE.format(label=m.label, target=m.target) for m in current_menus]))
        #             current_menus.clear()
        #             continue
        #         if rpy_element.music:
        #             f.write(rpy_element.music.render() + '\n')
        #         if rpy_element.character:
        #             for ch in rpy_element.character:
        #                 f.write(ch.render() + '\n')
        #         if rpy_element.background:
        #             f.write(rpy_element.background.render() + '\n')
        #         if rpy_element.sound:
        #             f.write(rpy_element.sound.render() + '\n')
        #         if rpy_element.transition:
        #             f.write(rpy_element.transition.render() + '\n')
        #         if rpy_element.voice:
        #             f.write(rpy_element.voice.render() + '\n')
        #         if rpy_element.text:
        #             if last_voice and last_voice.sustain:
        #                 f.write("voice sustain\n")
        #             f.write(rpy_element.text.render() + '\n')
        #         if rpy_element.change_page:
        #             f.write(rpy_element.change_page.render() + '\n')
        #         last_voice = rpy_element.voice
        #     if current_menus:
        #         # fix menu在最后一行
        #         f.write("menu:\n" + "\n".join(
        #             [MENU_TEMPLATE.format(label=m.label, target=m.target) for m in current_menus]))
                
                

CHAR_TEMPLATE = "define {variable} = Character('{name}', color=\"{color}\", image=\"{image}\", what_suffix=\"{what_suffix}\")"

class CharacterRpyFileWriter(object):

    @classmethod
    def write_file(cls, output_dir, res):
        output_path = output_dir + "/" + res.label + '.rpy'
        with open(output_path, 'w', encoding='utf-8') as f:
            for rpy_element in res.data:
                char_renpy_code = CHAR_TEMPLATE.format(variable=rpy_element.variable, name=rpy_element.name, color=rpy_element.color, image=rpy_element.image, what_suffix=rpy_element.what_suffix) + '\n'
                f.write(char_renpy_code)
         
         
IMAGE_TEMPLATE = "image {variable} = \"{file_name}\""

class ImageRpyFileWriter(object):
    
    @classmethod
    def write_file(cls, output_dir, res):
        output_path = output_dir + "/" + res.label + '.rpy'
        with open(output_path, 'a', encoding='utf-8') as f:
            for rpy_element in res.data:
                image_renpy_code = IMAGE_TEMPLATE.format(variable=rpy_element.variable, file_name=rpy_element.file_name) + '\n'
                f.write(image_renpy_code)
        
        
class CustomCodeRpyFileWriter(object):
    
    @classmethod
    def write_file(cls, output_dir, res):
        output_path = output_dir + "/" + res.label + '.rpy'
        with open(output_path, 'a', encoding='utf-8') as f:
            for rpy_element in res.data:
                custom_renpy_code = rpy_element.code + '\n'
                f.write(custom_renpy_code)
        
        
LABEL_TEMPLATE = "label {label}:\n" 
PAUSE_TEMPLATE = "    with Pause({duration})\n" 
JUMP_TEMPLATE = "    jump {target}\n" 
MENU_TEMPLATE = "    menu:\n"
OPTION_TEMPLATE = "        \"{option}\":\n"
class DialogRpyFileWriter(object):
    
    @classmethod
    def write_file(cls, output_dir, res):
        output_path = output_dir + "/" + res.label + '.rpy'
        with open(output_path, 'a', encoding='utf-8') as f:
            index = 2
            for rpy_element in res.data:
                addition_indent = ""
                f.write('    # Row ' + str(index) + '\n')
                if rpy_element.label:
                    custom_renpy_code = LABEL_TEMPLATE.format(label=rpy_element.label)
                    f.write(custom_renpy_code)
                if rpy_element.show_menu:
                    custom_renpy_code = MENU_TEMPLATE
                    f.write(custom_renpy_code)
                if rpy_element.is_option:
                    custom_renpy_code = OPTION_TEMPLATE.format(option=rpy_element.dialog.text)
                    f.write(custom_renpy_code)
                    addition_indent = "        "    
                if rpy_element.music:
                    f.write(addition_indent + rpy_element.music.render() + '\n')
                if rpy_element.sound:
                    f.write(addition_indent + rpy_element.sound.render() + '\n')
                if rpy_element.scene:
                    f.write(addition_indent + rpy_element.scene.render() + '\n')
                if rpy_element.tachie:
                    f.write(addition_indent + rpy_element.tachie.render() + '\n')
                if rpy_element.transition_1:
                    f.write(addition_indent + rpy_element.transition_1.render() + '\n')
                if rpy_element.voice:
                    f.write(addition_indent + rpy_element.voice.render() + '\n')
                if rpy_element.dialog and not rpy_element.is_option:
                    f.write(addition_indent + rpy_element.dialog.render() + '\n')
                if rpy_element.jump_to_label:
                    custom_renpy_code = addition_indent + JUMP_TEMPLATE.format(target=rpy_element.jump_to_label)
                    f.write(custom_renpy_code)
                if rpy_element.clear_page:
                    f.write(addition_indent + rpy_element.clear_page.render() + '\n')
                if rpy_element.pause > 0:
                    custom_renpy_code = addition_indent + PAUSE_TEMPLATE.format(duration=rpy_element.pause)
                    f.write(custom_renpy_code)
                if rpy_element.renpy_command:
                    f.write(addition_indent + rpy_element.renpy_command.render() + '\n')
                index += 1