#!/usr/bin/env python
# -*- coding:utf-8 -*-
from collections import namedtuple

from tkinter.messagebox import showerror, showinfo

from const.parser_setting import EXCEL_PARSE_START_ROW, EXCEL_PARSE_START_COL, EXCEL_PARSE_CHARACTER_START_ROW, EXCEL_PARSE_CHARACTER_START_COL, EXCEL_PARSE_IMAGE_START_ROW, EXCEL_PARSE_IMAGE_START_COL
from corelib.exception import ParseFileException
from tools.excel import read_excel

# 解析结果(sheet粒度)，包含sheet和数据
SheetParseResult = namedtuple('ParseResult', ['name', 'row_values'])


class Parser(object):
    """
    Excel解析器
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def get_excel_wb(self):
        """
        解析文件
        :return RpyElement列表
        """
        try:
            wb = read_excel(self.file_path)
        except ParseFileException as err:
            showerror("error", err.msg)
            raise err
        return wb

    def get_parsed_sheets(self):
        """
        解析文件
        :return RpyElement列表
        """
        wb = self.get_excel_wb()
        result = []
        for sheet in wb.sheets():
            result.append(SheetParseResult(name=sheet.name, row_values=self.parse_sheet(sheet)))
        return result

    def parse_sheet(self, sheet):
        result = []
        for i in range(EXCEL_PARSE_START_ROW, sheet.nrows):
            data = [r.value for r in sheet.row(i)]
            if not any(data):
                continue
            if len(data) < EXCEL_PARSE_START_COL:
                # 补全数据
                data.extend(["" for i in range(EXCEL_PARSE_START_COL - len(data))])
            assert len(data) == EXCEL_PARSE_START_COL
            result.append(data)
        return result

    def get_character_parsed_sheets(self):
        wb = self.get_excel_wb()
        result = []
        for sheet in wb.sheets():
            result.append(SheetParseResult(name=sheet.name, row_values=self.character_parse_sheet(sheet)))
        return result
    
    def character_parse_sheet(self, sheet):
        result = []
        for i in range(EXCEL_PARSE_CHARACTER_START_ROW, sheet.nrows):
            # showinfo("row", i)
            data = [r.value for r in sheet.row(i)]
            if not any(data):
                continue
            if len(data) < EXCEL_PARSE_CHARACTER_START_COL:
                data.extend(["" for i in range(EXCEL_PARSE_CHARACTER_START_COL - len(data))])
            # assert len(data) == EXCEL_PARSE_CHARACTER_START_COL
            result.append(data)
        return result
    
    
    def get_image_parsed_sheets(self):
        wb = self.get_excel_wb()
        result = []
        for sheet in wb.sheets():
            result.append(SheetParseResult(name=sheet.name, row_values=self.image_parse_sheet(sheet)))
        return result
    
    def image_parse_sheet(self, sheet):
        result = []
        for i in range(EXCEL_PARSE_IMAGE_START_ROW, sheet.nrows):
            data = [r.value for r in sheet.row(i)]
            if not any(data):
                continue
            if len(data) < EXCEL_PARSE_IMAGE_START_COL:
                data.extend(["" for i in range(EXCEL_PARSE_IMAGE_START_COL - len(data))])
            # assert len(data) == EXCEL_PARSE_IMAGE_START_COL
            result.append(data)
        return result
