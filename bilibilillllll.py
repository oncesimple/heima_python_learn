#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/11/10 12:05'
# import gevent.monkey
# gevent.monkey.patch_all()
# import requests

import requests, time, hashlib, urllib.request, re, json
from multiprocessing import Pool
import os, sys, threading
from tqdm import tqdm

def datas(url):
    start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + re.search(r'BV([0-9a-zA-Z]*)', url).group(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
    }
    html = requests.get('https://www.kanshenma.com/wp-content/uploads/2019/12/20191224_094354_000-683x1024.jpg',headers=headers)
    print(html.text)


def main():
    # BV1CK411A7DY
    datas(input('请输入视频地址或BV号:'))



if __name__ == '__main__':
    main()