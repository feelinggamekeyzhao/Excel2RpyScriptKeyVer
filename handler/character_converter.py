#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    将Excel中的数据转化为rpy中的对象
"""
from tkinter.messagebox import showerror, showinfo

from collections import namedtuple


from const.character_converter_setting import ElementColNumMapping

SheetConvertResult = namedtuple('SheetConvertResult', ['label', 'data'])

RowConvertResult = namedtuple('RowConvertResult',
                              ['variable',
                               'name',
                               'color',
                               'image',
                               'what_suffix'
                               ])


class CharacterConverter(object):

    def __init__(self, parser):
        self.parser = parser
        self.variable = ''
        self.name = ''
        self.color = ''
        self.image = ''
        self.what_suffix = ''

    def generate_rpy_elements(self):
        result = []
        parsed_sheets = self.parser.get_character_parsed_sheets()
        for idx, parsed_sheet in enumerate(parsed_sheets):
            showinfo("hi parsed_sheet ", parsed_sheet.name)
            if parsed_sheet.name == "Character":
                label = parsed_sheet.name
                # showinfo("hi 2.3", "hihi 2.3")
                result.append(SheetConvertResult(label=label, data=self.parse_by_sheet(parsed_sheet.row_values)))
                # showinfo("hi", "hihi 2.7")
        return result

    def parse_by_sheet(self, values):
        # showinfo("hi", "hihi 2.4")
        result = []
        for row_value in values:
            result.append(self.parse_by_row_value(row_value))
        return result

    def parse_by_row_value(self, row):
        # showinfo("hi", "hihi 2.5")
        row_converter = RowConverter(row, self)
        return row_converter.convert()


class RowConverter(object):

    def __init__(self, row, converter):
        self.row = row
        self.converter = converter

    def convert(self):
        # showinfo("hi", "hihi 2.6")
        return RowConvertResult(
            variable=self._converter_variable(),
            name=self._converter_name(),
            color=self._converter_color(),
            image=self._converter_image(),
            what_suffix=self._converter_what_suffix(),
        )

    def _converter_variable(self):
        variable = self.row[ElementColNumMapping.get('var')]
        showinfo("variable", variable)
        if variable:
            self.converter.variable = variable
        return variable

    def _converter_name(self):
        # showinfo("hi", "hihi 2.312")
        name = self.row[ElementColNumMapping.get('name')]
        showinfo("name", name)
    
        if name:
            self.converter.name = name
        return name

    def _converter_color(self):
        color = self.row[ElementColNumMapping.get('color')]
        showinfo("color", color)
        
        if color:
            self.converter.color = color
        return color

    def _converter_image(self):
        image = self.row[ElementColNumMapping.get('image')]
        showinfo("image", image)
        
        if image:
            self.converter.image = image
        return image

    def _converter_what_suffix(self):
        what_suffix = self.row[ElementColNumMapping.get('what_suffix')]
        if what_suffix:
            self.converter.what_suffix = what_suffix
        return what_suffix