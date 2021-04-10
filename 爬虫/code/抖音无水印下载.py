#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/7/4 21:07'

import re
import requests

"""
TODO 声明
脚本仅仅提供学习使用，拿来盗别人视频，或者商业用途，后果自负作者不会承担任何责任。。
"""


def request(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) > AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 > Chrome/37.0.0.0 Mobile Safari/537.36 > "
                      "MicroMessenger/6.0.2.56_r958800.520 NetType/WIFI",
    }
    response = requests.get(url, headers=headers)
    return response


def main():
    url = input('请输入抖音视频链接：')
    new_url = request(re.findall("(http.*/)", url)[0]).url
    id_url = f'https://www.iesdouyin.com/web/api/v2/' \
             f'aweme/iteminfo/?item_ids={new_url.split("/")[5]}'
    data_json = request(id_url).json()
    data = {
        "mp3": data_json['item_list'][0]['music']['play_url']['uri'],
        "mp4": data_json['item_list'][0]['video']['play_addr']['url_list'][0].replace("wm", ""),
        "name": data_json['item_list'][0]['desc']
    }
    fileName = re.sub('[\/:*?"<>|]', '-', data['name'])
    with open(f'{fileName}.mp4', 'wb') as f:
        f.write(request(data['mp4']).content)
        print("下载完成")


if __name__ == '__main__':
    main()
