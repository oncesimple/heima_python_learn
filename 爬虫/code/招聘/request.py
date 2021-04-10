#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/3/27 15:41'
import requests
import pandas as pd
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.130 Safari/537.36 '
}


def requests_json(url,):
    return requests.get(url, headers=headers).json()


def reuquests_text(url):
    return requests.get(url, headers=headers).text


def write_csv(dic, file):
    """
    pandas写入csv文件
    :param dic: 数据
    :param file: 文件名称
    :return:
    """
    df = pd.DataFrame(dic)
    df.to_csv(file, encoding='utf-8')
    print("数据写入完成")
