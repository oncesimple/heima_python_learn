#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/4/21 19:24'
import requests
def reque(url):
    """
    请求json
    :param url: 请求api
    :return: 数据字典
    """
    data = requests.get(url).json()['data']
    return data


# 计算评论到底有多少页返回页数
def math11(data):
    """
    计算评论页数
    :param data: 数据字典
    :return: 页数
    """
    num = data['page']['count'] / data['page']['size']
    if type(num) == int:
        return num + 1
    else:
        return int(num) + 2


def replys(aid):
    """
    评论提取
    :param aid: oid
    :return: 数据列表
    """
    dic_list = []
    urls = f'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid={aid}'
    yehsu = math11(reque(urls))
    print(yehsu)
    for i in range(1, yehsu):
        # 拼接url
        url = f'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={i}&type=1&oid={aid}'
        data = reque(url)  # 请求url
        dic = pres(data)  # 数据的提取
        dic_list.append(pres(data))  # 数据整合成df然后放到列表里
    return dic_list


def pres(data):
    """
    评论提取
    :param data: 数据字典
    :return: 数据字典
    """
    data_list = data['replies']
    try:
        return {
            '用户id': [i['member']['mid'] for i in data_list],
            '用户昵称': [i['member']['uname'] for i in data_list],
            '性别': [i['member']['sex'] for i in data_list],
            '个性签名': [i['member']['sign'] for i in data_list],
            '评论': [i['content']['message'] for i in data_list],

        }
    except:
        return None

def main():
    print(replys('710256610'))


if __name__ == '__main__':
    main()
