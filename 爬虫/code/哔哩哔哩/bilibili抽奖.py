#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/4/2 17:33'

import re, json
import requests
import pandas as pd
import time
import math
import hashlib, urllib.request, json
import os, sys, threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.130 Safari/537.36 '
}


def qq_index(name):
    '''

    :param name: 搜索名字
    :return: urls
    '''
    url = f'https://t.bilibili.com/topic/name/{name}/feed'
    r = requests.get(url, headers=headers)
    data = re.findall(r'("dynamic_id":"\d*)', r.text)
    urls = [i.replace('"dynamic_id":"',
                      f'https://api.vc.bilibili.com/topic_svr/v1/topic_svr/topic_history?topic_name={name}&offset_dynamic_id=')
            for i in data]
    return urls


def index_url_data(url):
    r = requests.get(url, headers=headers).json()
    return r['data']['cards'][0]['desc']['dynamic_id']


def url_data(url):
    r = requests.get(url, headers=headers)
    return r.json()['data']


def bag_data(V_id):
    if V_id == 0:
        return 0
    api = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={}'.format(V_id)
    api_data = url_data(api)
    try:
        json.loads(api_data['card']['card'])['item']['description']
    except:
        return 0
    try:
        description = json.loads(api_data['card']['card'])['item']['description']
        # describe.append(i['card']['item']['content'])
    except:
        description = json.loads(api_data['card']['card'])['item']['content']
        # describe.append(i['card']['item']['description'])
    return {
        '时间戳': api_data['card']['desc']['timestamp'],
        '转发者/发送者 ID': api_data['card']['desc']['user_profile']['info']['uid'],
        '转发者/发送者 昵称': api_data['card']['desc']['user_profile']['info']['uname'],
        '抽奖链接': 'https://t.bilibili.com/{}?tab=2'.format(V_id),
        '抽奖描述': description,
    }


def datas(name, data):
    return [{
        '抽奖id': [i['desc']['pre_dy_id'] for i in data['cards']]
    },
        f"https://api.vc.bilibili.com/topic_svr/v1/topic_svr/topic_history?topic_name={name}&offset_dynamic_id={data['offset']}"]


def pandas_data(dic):
    return pd.DataFrame(dic)


# def main():
#     datass = []
#     name = '互动抽奖'
#     urls = qq_index(name)
#     print(urls[0])
#     for i in urls:
#         for n in datas(name,url_data(i))[0]['抽奖id']:
#             datass.append(n)
#     df = pandas_data({'抽奖id':datass})
#     df.drop_duplicates('抽奖id', 'first', inplace=True)
#     urlss = df['抽奖id'].to_list()
#     dic_li = []
#     chang = len(urlss)
#     print('总共{}页'.format(chang))
#     for i in urlss:
#         cc =bag_data(i)
#         if cc == 0:
#             continue
#         dic_li.append(cc)
#         print('剩余{}页'.format(chang))
#         chang -= 1
#     print(dic_li)
#     dfss = pandas_data(dic_li)
#     dfss.drop_duplicates('抽奖链接', 'first', inplace=True)
#     dfsss = pd.to_datetime(dfss['时间戳'].to_list(), unit='s')
#     dfa = dfss.set_index(dfsss)
#     dfa.to_csv('bilibili抽奖.csv',encoding='utf-8')
#     print(dfa)
def main():
    V_ids = []
    name = '互动抽奖'
    urls = qq_index(name)
    i = 0
    data = url_data(urls[0])
    while i <= 4:
        for vid in datas(name, data)[0]['抽奖id']:
            if vid == 0:
                continue
            V_ids.append(vid)
        url = f"https://api.vc.bilibili.com/topic_svr/v1/topic_svr/topic_history?topic_name={name}&offset_dynamic_id={data['offset']}"
        data = url_data(url)
        i += 1
    lst2 = list(set(V_ids))
    print('总共{}页'.format(len(lst2)))
    V_ids.clear()
    for v_id in lst2:
        cc = bag_data(v_id)
        if cc == 0:
            continue
        V_ids.append(cc)
    dfss = pandas_data(V_ids)
    dfss.drop_duplicates('抽奖链接', 'first', inplace=True)
    dfsss = pd.to_datetime(dfss.时间戳, unit='s')
    dfa = dfss.set_index(dfsss)
    dfa.set_index(inplace=True)
    print(dfa)


if __name__ == '__main__':
    main()
