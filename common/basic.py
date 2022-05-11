#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:wangjie
# datetime:2020/8/3 3:04 下午
# software: PyCharm
import datetime
import math
import os
import random
import string
import configparser
import xlrd
import xlutils
import xlwt
import xlutils.copy
import time


#生成当前时间戳
def getNowTime():
    """
    生成当前时间戳
    :return:
    """
    time_stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    return time_stamp

#生成随机字符串（小写英文+数字）
def getRandomstr(number):
    """
    生成随机字符串（小写英文+数字）
    :param number:
    :return:
    """
    ran_str = ''.join(random.sample(string.ascii_lowercase + string.digits, number))
    return ran_str


#生成随机数字
def getRandomint(number):
    """
    生成随机数字
    :param number:
    :return:
    """
    ran_int = ''.join(random.sample(string.digits, number))
    return ran_int


#生成随机字符串（大、小写英文+数字）
def getRandomStr(number):
    """
    生成随机字符串（大、小写英文+数字）
    :param number:
    :return:
    """
    ran_Str = ''.join(random.sample(string.ascii_letters + string.digits, number))
    return ran_Str


#Excel读取方法
def read_excelInfo(path, sheetIndex):
    """
    Excel读取方法
    :param path:
    :param rb:
    :param sheet:
    :return:
    """
    workbook = xlrd.open_workbook(path, "rb")
    table = workbook.sheet_by_index(sheetIndex)
    return table


#创建Excel并写入
def write_excelInfo(path, sheetName, row, col, value):
    """
    创建Excel并写入
    :param path:
    :param sheetName:
    :param row:
    :param col:
    :param value:
    :return:
    """
    writebook = xlwt.Workbook(path, "rb")
    writesheet = writebook.add_sheet(sheetName)
    writesheet.write(row, col, value)
    writebook.save(path)


#编辑xlwt创建的Excel
def update_excelInfo(path, sheetIndex, row, col, value):
    """
    编辑xlwt创建的Excel
    :param path: 文件路径
    :param sheetIndex: 工作表序号（从0开始）
    :param row: 行数（从0开始）
    :param col: 列数（从0开始）
    :param value: 输入内容
    :return:
    """
    rb = xlrd.open_workbook(path)
    #复制工作薄
    wb = xlutils.copy.copy(rb)
    # 获取sheet对象，通过sheet_by_index()获取的sheet对象没有write()方法
    ws = wb.get_sheet(sheetIndex)
    # 写入数据
    ws.write(row, col, value)
    # 利用保存时同名覆盖达到修改excel文件的目的,注意未被修改的内容保持不变
    wb.save(path)


#将Excel中的内容输出为一个列表
def list_outputExcelInfo(dataPath, indexSheet, startRow, startCol):
    """
    将Excel中的内容输出为一个列表
    :param dataPath: 文件路径
    :param indexSheet: sheet表
    :param startRow: 开始行
    :param startCol: 开始列
    :return:
    """
    table = read_excelInfo(dataPath, indexSheet)
    rows = table.nrows  # 获取行数
    columns = table.ncols  # 获取列数
    list = []
    for i in range(startRow, rows):
        for j in range(startCol, columns):
            str = table.cell(i, j).value
            if str != '':
                list.append(str)
    return list


#获取相对路径
def get_path(path):
    """
    获取相对路径
    :param path:
    :return:
    """
    return os.path.abspath(os.path.join(path))


#获取相对路径
def get_filePath(filePath):
    """
    获取相对路径
    :param projectName: 根据需要将"seldomUnit"设置为相对的名字
    :param filePath: 目录名/文件名.后缀名
    :return:
    """
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("DjangoTest/") + len("DjangoTest/")]  # 获取项目的根路径
    dataPath = os.path.abspath(rootPath + filePath)  # 获取文件的路径
    return dataPath


#获取config配置
def get_config(name, key):
    """
    获取config配置
    :param name:
    :param key:
    :return:
    """
    config = configparser.ConfigParser()
    config.read(get_filePath("common/config.ini"))
    return config.get(name, key)


#指标值计算
def indexScore(x, x1, x2, y1, y2, weight):
    """
    指标值计算
    :param x: 入参
    :param x1: 入参最小区间
    :param x2: 入参最大区间
    :param y1: 得分最小区间
    :param y2: 得分最大区间
    :param weight: 指标权重
    :return: None
    """
    if x < x1:
        print("入参值", x, "不得小于入参最小区间", x1)
    # elif x > x2:
    #     print("入参值", x, "不得大于入参最大区间", x2)
    # elif x == x2:
    #     print("入参区间为左闭右开，入参值", x, "不能等于入参最大区间，", x2)
    #     print("该结果无法计算！")
    else:
        y = (y2 - y1) / (x2 - x1) * (x - x1) + y1
        source = y * weight
        #截取小数点后四位，不做四舍五入处理，处理逻辑为：先右移小数点4位，再移回来。
        n = 4
        sourceIntercept = math.floor(source*10**n)/(10**n)
        print("指标原分数为：", y)
        print("指标乘权后原分数为：", source)
        print("指标乘权后截取分数为：", sourceIntercept)