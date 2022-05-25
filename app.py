#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64
import webbrowser
from tkinter import Tk, Text, PhotoImage, Menu, messagebox, END
from tkinter.messagebox import showerror, showinfo
from tkinter.ttk import Frame, Style, Entry, Combobox, Button, Label
from tkinter import filedialog

import requests

from const import CURRENT_VERSION
from corelib.exception import ConvertException, SaveFileException
from handler.converter import Converter
from handler.dialog_converter import DialogConverter
from handler.character_converter import CharacterConverter
from handler.image_converter import ImageConverter, CustomCodeConverter
from handler.parser import Parser
from handler.writer import RpyFileWriter, CharacterRpyFileWriter, ImageRpyFileWriter, CustomCodeRpyFileWriter, DialogRpyFileWriter
from tools.image_data import *


class Application_ui(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Excel轉化Rpy工具_Key版 v1.0.3')
        self.master.geometry('600x343')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()
        self.bkg_gif = PhotoImage(data=base64.b64decode(back_ground_gif_data))
        self.background_label = Label(self.top, image=self.bkg_gif)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.Text = Text(self.top, font=('宋体', 9))
        self.Text.place(relx=0.066, rely=0.07, relwidth=0.869, relheight=0.563)

        self.saveAddr = Entry(self.top, font=('宋体', 9))
        self.saveAddr.place(relx=0.355, rely=0.84, relwidth=0.409, relheight=0.052)

        self.ComboList = ['源文檔目錄', '自定義目錄']
        self.Combo = Combobox(self.top, values=self.ComboList, font=('宋体', 9), state='readonly')
        self.Combo.place(relx=0.184, rely=0.84, relwidth=0.146, relheight=0.058)
        self.Combo.set(self.ComboList[0])
        self.Combo.bind('<<ComboboxSelected>>', self.comboEvent)

        self.style.configure('InputButton.TButton', font=('宋体', 9))
        self.InputButton = Button(self.top, text='瀏覽', command=self.InputButton_Cmd, style='InputButton.TButton')
        self.InputButton.place(relx=0.184, rely=0.7, relwidth=0.133, relheight=0.073)

        self.Haruhi_gif = PhotoImage(data=base64.b64decode(haruhi_gif_data))
        self.style.configure('ConvertButton.TButton', font=('宋体', 9))
        self.ConvertButton = Button(self.top, image=self.Haruhi_gif, command=self.ConvertButton_Test_Cmd,
                                    style='ConvertButton.TButton')
        self.ConvertButton.place(relx=0.788, rely=0.7, relwidth=0.146, relheight=0.236)

        self.style.configure('OutputLabel.TLabel', anchor='w', font=('宋体', 9))
        self.OutputLabel = Label(self.top, text='保存目錄：', style='OutputLabel.TLabel')
        self.OutputLabel.place(relx=0.066, rely=0.84, relwidth=0.107, relheight=0.05)

        self.style.configure('InputLabel.TLabel', anchor='w', font=('宋体', 9))
        self.InputLabel = Label(self.top, text='輸入設置：', style='InputLabel.TLabel')
        self.InputLabel.place(relx=0.066, rely=0.723, relwidth=0.107, relheight=0.05)

        menubar = Menu(self.top)
        filemenu = Menu(menubar, tearoff=0)  # tearoff意为下拉
        menubar.add_cascade(label='幫助', menu=filemenu)
        filemenu.add_command(label='影片教程', command=self.open_help_url)
        # filemenu.add_command(label='檢查更新', command=self.check_for_update)

        self.top.config(menu=menubar)

class Application(Application_ui):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。

    def __init__(self, master=None):
        Application_ui.__init__(self, master)

    def convert(self, output_dir, res, role_name_mapping, role_side_character_mapping):
        try:
            RpyFileWriter.write_file(output_dir, res, role_name_mapping, role_side_character_mapping)
        except FileNotFoundError:
            raise SaveFileException("保存目錄不存在")

    def checkEqual(self, iterator):
        iterator = iter(iterator)
        try:
            first = next(iterator)
        except StopIteration:
            return False
        return all(first == rest for rest in iterator)

    def getFileName(self, path):
        return path.split('/')[-1].split('.')[0]

    def getTlist(self):
        Tlist = self.Text.get('1.0', 'end').split('\n')
        Tlist = [value.strip() for value in Tlist]
        Tlist = [value for value in Tlist if value]
        return Tlist

    def getOriPath(self):
        paths = list()
        for path in self.getTlist():
            paths.append('/'.join(path.split('/')[0:-1]))
        if self.checkEqual(paths):
            return paths[0]
        else:
            showerror("獲取錯誤", "未設置輸入或源文檔不在同一目錄下！")
            return ''

    def comboEvent(self, *arg):
        if self.Combo.get() == '源文檔目錄':
            if self.saveAddr.get():
                self.saveAddr.delete('0', 'end')
            self.saveAddr.insert('0', self.getOriPath())
        elif self.Combo.get() == '自定義目錄':
            file_path = filedialog.askdirectory(title=u'保存文檔到檔案夾')
            if self.saveAddr.get():
                self.saveAddr.delete('0', 'end')
            self.saveAddr.insert('0', file_path)

    def InputButton_Cmd(self, event=None):
        file_paths = filedialog.askopenfilenames(title=u'選擇文檔',
                                                 filetypes=[("Excel-2007 file", "*.xlsx"), ("Excel-2003 file", "*.xls"),
                                                            ("all", "*.*")])
        for line in file_paths:
            self.Text.insert(END, line + '\n')
        self.comboEvent()

    def ConvertButton_Cmd(self, event=None):
        success_flag = True
        for path in self.getTlist():
            try:
                parser = Parser(path)
                conveter = Converter(parser)
                convert_results = conveter.generate_rpy_elements()
                print(conveter.side_characters)
                for res in convert_results:
                    self.convert(self.saveAddr.get(), res, conveter.role_name_mapping, conveter.side_characters)
            except ConvertException as err:
                success_flag = False
                showerror("轉換錯誤", err.msg)
        if success_flag:
            showinfo("轉換成功", "轉換完成")
            self.saveAddr.delete('0', 'end')
            self.Text.delete('0.0', 'end')
            
    def ConvertButton_Test_Cmd(self, event=None):
        success_flag = True
        for path in self.getTlist():
            try:
                parser = Parser(path)
                conveter = CharacterConverter(parser)
                convert_results = conveter.generate_rpy_elements()
                for res in convert_results:
                    self.convert_character(self.saveAddr.get(), res)
                
                conveter = ImageConverter(parser)
                convert_results = conveter.generate_rpy_elements()
                for res in convert_results:
                    self.convert_image(self.saveAddr.get(), res)
                
                conveter = CustomCodeConverter(parser)
                convert_results = conveter.generate_rpy_elements()
                for res in convert_results:
                    self.convert_custom_code(self.saveAddr.get(), res)
                
                conveter = DialogConverter(parser)
                convert_results = conveter.generate_rpy_elements()
                for res in convert_results:
                    self.convert_dialog(self.saveAddr.get(), res)
            except ConvertException as err:
                success_flag = False
                showerror("轉換錯誤", err.msg)
        if success_flag:
            showinfo("轉換成功", "轉換完成")
            self.saveAddr.delete('0', 'end')
            self.Text.delete('0.0', 'end')
            
    def convert_character(self, output_dir, res):
        try:
            CharacterRpyFileWriter.write_file(output_dir, res)
        except FileNotFoundError:
            raise SaveFileException("保存目錄不存在")
            
    def convert_image(self, output_dir, res):
        try:
            ImageRpyFileWriter.write_file(output_dir, res)
        except FileNotFoundError:
            raise SaveFileException("保存目錄不存在")
            
    def convert_custom_code(self, output_dir, res):
        try:
            CustomCodeRpyFileWriter.write_file(output_dir, res)
        except FileNotFoundError:
            raise SaveFileException("保存目錄不存在")
            
    def convert_dialog(self, output_dir, res):
        try:
            DialogRpyFileWriter.write_file(output_dir, res)
        except FileNotFoundError:
            raise SaveFileException("保存目錄不存在")
        
    def open_url(self, url):
        webbrowser.open(url, new=0)

    def open_help_url(self, event=None):
        self.open_url("https://www.bilibili.com/video/BV1gZ4y1K7Y9")

    def check_for_update(self, event=None):
        try:
            resp = requests.get("https://api.github.com/repos/HaruhiFanClub/Excel2RpyScript/releases/latest", timeout=2).json()
        except Exception as ex:
            self.Text.insert(END, "檢查更新失敗：{}\n請直接到https://github.com/HaruhiFanClub/Excel2RpyScript/releases查看最新版本\n")
            showinfo("網絡連接失敗", "\n檢查更新失敗!\n".format(ex))
            return
        if resp['tag_name'] == CURRENT_VERSION:
            showinfo("檢測成功", "當前已是最新版本!")
        else:
            confirm_download = self.showConfirmModal("检查到新版本", "当前版本：{0}  最新版本：{1}, 是否前往{2}下载？"
                                                     .format(CURRENT_VERSION, resp['tag_name'], resp['html_url']))
            if confirm_download:
                self.open_url(resp['html_url'])

    def showConfirmModal(self, title, message):
        return messagebox.askokcancel(title, message)

if __name__ == "__main__":
    top = Tk()
    top.iconphoto(False, PhotoImage(data=base64.b64decode(haruhi_gif_data)))
    Application(top).mainloop()
    try:
        top.destroy()
    except:
        pass
