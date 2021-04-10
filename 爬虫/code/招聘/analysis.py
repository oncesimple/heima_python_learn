#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/3/27 15:55'
from lxml import etree
import re


def lxml_xpath(response, xpath):
    """
    xpath解析
    :param response: html文本
    :param xpath: xpath 语法
    :return: 列表
    """
    return etree.HTML(response).xpath(xpath)


def data_re(data,rule):
    """
    正则筛选
    :param data: 筛选的数据
    :param rule: 正则表达式
    :return: 列表
    """
    return re.findall(rule,data)

