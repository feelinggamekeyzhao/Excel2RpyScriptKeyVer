#!/usr/bin/env python
# -*- coding:utf-8 -*-
from tkinter.messagebox import showerror, showinfo

CHAR_TEMPLATE = "define {variable} = Character('{name}', color=\"{color}\", image=\"{image}\", what_suffix=\"{what_suffix}\")"

class CharacterRpyFileWriter(object):

    @classmethod
    def write_file(cls, output_dir, res):
        showinfo("hi", "hihi 4")
        output_path = output_dir + "/" + res.label + '.rpy'
        with open(output_path, 'w', encoding='utf-8') as f:
            for rpy_element in res.data:
                showinfo("rpy_element", rpy_element.name)
                print(rpy_element.name)
                print(rpy_element.color)
                print(rpy_element.image)
                # showinfo("rpy_element", rpy_element.color)
                # showinfo("rpy_element", rpy_element.image)
                # showinfo("rpy_element", rpy_element.what_suffix)
                char_renpy_code = CHAR_TEMPLATE.format(variable=rpy_element.variable, name=rpy_element.name, color=rpy_element.color, image=rpy_element.image, what_suffix=rpy_element.what_suffix) + '\n'
                showinfo("char_renpy_code", char_renpy_code)
                
                f.write(char_renpy_code)
         