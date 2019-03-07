#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import configparser

#读写配置文件类
class Config():
    def __init__(self, file='config\config.ini'):
        self.file = file
        self.config = configparser.ConfigParser()
        self.config.read(file, encoding="utf-8")  # utf-8-sig

    # 读取
    def get(self, section='', key=''):
        try:
            return self.config[section][key]
        except configparser.DuplicateSectionError:
            return False

    # 设置
    def set(self, section='', key='', value=''):
        try:
            list = self.config.sections()
            if (section in list):
                pass
            else:
                self.config.add_section(section)

            self.config.set(section, key, value)

        except configparser.DuplicateSectionError:
            pass

        # 写入
        self.config.write(open(self.file, "w", encoding="utf-8"))


if __name__ == '__main__':
    pass
