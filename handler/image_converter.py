#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    将Excel中的数据转化为rpy中的对象
"""
from tkinter.messagebox import showerror, showinfo

from collections import namedtuple


from const.image_converter_setting import ElementColNumMapping

SheetConvertResult = namedtuple('SheetConvertResult', ['label', 'data'])

RowConvertResult = namedtuple('RowConvertResult',
                              ['variable',
                               'file_name',
                               ])


class ImageConverter(object):

    def __init__(self, parser):
        self.parser = parser
        self.variable = ''
        self.file_name = ''

    def generate_rpy_elements(self):
        result = []
        parsed_sheets = self.parser.get_image_parsed_sheets()
        for idx, parsed_sheet in enumerate(parsed_sheets):
            showinfo("hi parsed_sheet ", parsed_sheet.name)
            if parsed_sheet.name == "Image":
                # label = parsed_sheet.name
                label = "script"
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
            variable=self._converter_variable(),
            file_name=self._converter_file_name(),
        )

    def _converter_variable(self):
        variable = self.row[ElementColNumMapping.get('var')]
        if variable:
            self.converter.variable = variable
        return variable

    def _converter_file_name(self):
        name = self.row[ElementColNumMapping.get('name')]
        if name:
            self.converter.file_name = name
        return name